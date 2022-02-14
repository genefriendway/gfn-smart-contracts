// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "./interfaces/IReservePool.sol";
import "./interfaces/IContractRegistry.sol";
import "./interfaces/IRevenueSharingArrangement.sol";
import "./mixins/RevenueSharingArrangementRetriever.sol";


contract ReservePool is
    Ownable,
    IReservePool,
    RevenueSharingArrangementRetriever
{

    using SafeERC20 for IERC20;
    IContractRegistry public registry;

    uint8 private maxLengthPoolId = 128;
    // poolId -> index -> Slot struct
    mapping(string => mapping(uint256 => Slot)) public pools;
    // poolId -> PoolPointer struct
    mapping(string => PoolPointer) pointers;
    // investor -> (poolId -> LIFE amount)
    mapping(address => mapping(string => uint256)) public balanceOfInvestors;


    modifier validPoolId(string memory poolId) {
        require(
            bytes(poolId).length > 0 && bytes(poolId).length <= maxLengthPoolId,
            "ReservePool: Length of Pool Id is invalid");
        _;
    }

    modifier activePoolId(string memory poolId) {
        require(
            pointers[poolId].isActive == true,
            'ReservePool: Pool Id is not active'
        );
        _;
    }

    constructor(address gfnOwner, IContractRegistry _registry) {
        registry = _registry;
        transferOwnership(gfnOwner);
    }

    function createPool(
        string memory poolId
    ) external override onlyOwner validPoolId(poolId) {
        // retrieve pointer of pool,
        // if not existing pool => system will initialize by default values
        PoolPointer storage pointer = pointers[poolId];

        // validate: the pool Id must be existed and activated
        require(pointer.isActive == false, 'ReservePool: Pool Id was created');

        // activate PoolId
        pointer.isActive = true;

        emit CreatePool(poolId);
    }

    function joinPool(
        address investor,
        string memory poolId,
        uint256 numberOfLIFE
    ) external override onlyOwner activePoolId(poolId) {
        // validate: number of LIFE that investor want to invest into the pool
        require(
            numberOfLIFE > 0,
            "ReservePool: Investing LIFE amount must be greater than zero"
        );

        // retrieve PoolPointer by PoolId
        PoolPointer storage pointer = pointers[poolId];

        // append a new slot to pools
        pools[poolId][pointer.lastIndex] = Slot(investor, numberOfLIFE);

        // update balance of Pool and last Index in the pointer
        pointer.balanceOfPool += numberOfLIFE;

        pointer.lastIndex += 1;

        // increase total invested LIFE of investor by new number of LIFE
        balanceOfInvestors[investor][poolId] += numberOfLIFE;

        emit JoinPool(investor, poolId, numberOfLIFE);
    }

    function requestCoInvestors(
        address geneticProfileOwner,
        string memory requestedPoolId,
        uint256 requestedNumerOfLIFE
    ) external override onlyOwner activePoolId(requestedPoolId) {
        // retrieve PoolPointer by PoolId
        PoolPointer storage pointer = pointers[requestedPoolId];

        // validate requestedNumerOfLIFE
        require(
            requestedNumerOfLIFE > 0, 
            "ReservePool: requested number of LIFE must be greater than zero"
        );
        require(
            requestedNumerOfLIFE <= pointer.balanceOfPool, 
            "ReservePool: requested pool does not have enough number of LIFE"
        );

        uint256 remainingRequestedNumberOfLIFE = requestedNumerOfLIFE;
        do {
            // loop through each slot of the requested pool, 
            // start from the first slot
            Slot storage currentSlot = pools[requestedPoolId][pointer.firstIndex];
            // if available number of LIFE of current slot is over
            // requested number of LIFE
            if (currentSlot.availableNumberOfLIFE > remainingRequestedNumberOfLIFE) {
                // decrease corresponding number of LIFE in the current slot
                currentSlot.availableNumberOfLIFE -= remainingRequestedNumberOfLIFE;
                // decrease corresponding balance of Investor in requested pool
                balanceOfInvestors[currentSlot.investor][requestedPoolId] -= remainingRequestedNumberOfLIFE;
                // make Revenue Sharing Arrangement between geneticProfileOwner and Investor
                _makeRevenueSharingArrangement(
                    geneticProfileOwner,
                    currentSlot.investor,
                    remainingRequestedNumberOfLIFE
                );
                // the current Slot has enough number of LIFE that genetic profile
                // owner requested => stop checking other slots and break the loop
                remainingRequestedNumberOfLIFE = 0;
            } else {
                // if available number of LIFE of current slot is less than
                // or equal to requested number of LIFE

                // calculate the remaining requested number of lIFE
                remainingRequestedNumberOfLIFE -= currentSlot.availableNumberOfLIFE;
                // decrease corresponding balance of Investor in requested pool
                balanceOfInvestors[currentSlot.investor][requestedPoolId] -= currentSlot.availableNumberOfLIFE;
                // make Revenue Sharing Arrangement between geneticProfileOwner and Investor
                _makeRevenueSharingArrangement(
                    geneticProfileOwner,
                    currentSlot.investor,
                    currentSlot.availableNumberOfLIFE
                );
                // the current slot run out of available LIFE, clear it
                delete pools[requestedPoolId][pointer.firstIndex];
                // move the pointer to the next slot
                pointer.firstIndex += 1;
            }
        } while (remainingRequestedNumberOfLIFE > 0);

        // decrease balance of pool after finding out co-investor
        pointer.balanceOfPool -= requestedNumerOfLIFE;

        emit RequestCoInvestors(
            geneticProfileOwner, requestedPoolId, requestedNumerOfLIFE
        );
    }
    function _makeRevenueSharingArrangement(
        address geneticProfileOwner,
        address investor,
        uint256 investedNumberOfLIFE
    ) private {
        IRevenueSharingArrangement arrangement = IRevenueSharingArrangement(
            _getRevenueSharingArrangementAddress(registry)
        );
        arrangement.makeCollaborationBetweenGeneticProfileOwnerAndInvestor(
            geneticProfileOwner, investor, investedNumberOfLIFE
        );
    }

    function exitPool(
        address investor,
        string memory poolId,
        uint256 exitedNumberOfLIFE
    ) external override onlyOwner activePoolId(poolId) {
        uint256 currentNumberOfLIFE = balanceOfInvestors[investor][poolId];
        require(exitedNumberOfLIFE > 0, "ReservePool: Exited number of LIFE must be greater than zero");
        require(exitedNumberOfLIFE <= currentNumberOfLIFE, "ReservePool: Exited number of LIFE exceeds current balance");

        _updateBalanceOfInvestor(investor, poolId, exitedNumberOfLIFE);

        emit ExitPool(investor, poolId, exitedNumberOfLIFE);
    }

    function _updateBalanceOfInvestor(
        address investor,
        string memory poolId,
        uint256 numberOfLIFE
    ) private {
        // retrieve PoolPointer by PoolId
        PoolPointer storage pointer = pointers[poolId];

        uint256 numberOfLIFETemp = numberOfLIFE;
        Slot storage _slot;
        for (uint256 index = pointer.firstIndex; index < pointer.lastIndex; index++) {
            _slot = pools[poolId][index];
            if (_slot.investor == investor) {
                if (numberOfLIFETemp < _slot.availableNumberOfLIFE) {
                    _slot.availableNumberOfLIFE -= numberOfLIFETemp;
                } else {
                    numberOfLIFETemp -= _slot.availableNumberOfLIFE;
                    _slot.availableNumberOfLIFE = 0;
                }

                if (numberOfLIFETemp == 0) break;
            }
        }

        pointer.balanceOfPool -= numberOfLIFE;
        balanceOfInvestors[investor][poolId] -= numberOfLIFE;
    }

    function getStatusOfPool(string memory poolId) external override view returns (bool) {
        return pointers[poolId].isActive;
    }

    function getBalanceOfPool(string memory poolId) external override view returns (uint256) {
        return pointers[poolId].balanceOfPool;
    }

    function getBalanceOfInvestor(
        address investor,
        string memory poolId
    ) external override view returns (uint256) {
        return balanceOfInvestors[investor][poolId];
    }

}
