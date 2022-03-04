// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "./interfaces/IContractRegistry.sol";
import "./interfaces/IReservePool.sol";
import "./interfaces/IReservePool.sol";
import "./interfaces/IParticipantWallet.sol";
import "./interfaces/IRevenueSharingArrangement.sol";
import "./mixins/RevenueSharingArrangementRetriever.sol";
import "./mixins/InvestorWalletRetriever.sol";
import "./mixins/ReservePoolWalletRetriever.sol";
import "./mixins/GeneFriendNetworkWalletRetriever.sol";
import "./mixins/AccessibleRegistry.sol";


contract ReservePool is
    AccessibleRegistry,
    IReservePool,
    RevenueSharingArrangementRetriever,
    InvestorWalletRetriever,
    ReservePoolWalletRetriever,
    GeneFriendNetworkWalletRetriever
{

    using SafeERC20 for IERC20;

    uint8 private maxLengthPoolId = 128;
    // poolId -> index -> Slot struct
    mapping(string => mapping(uint256 => Slot)) public pools;
    // poolId -> PoolInfo struct
    mapping(string => PoolInfo) poolInfo;
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
            poolInfo[poolId].isActive == true,
            'ReservePool: Pool Id is not active'
        );
        _;
    }

    constructor(IContractRegistry _registry) AccessibleRegistry(_registry){}

    function createPool(
        string memory poolId
    )
        external
        override
        onlyGFNOperator
        validPoolId(poolId)
    {
        // retrieve poolInfo of Pool,
        // if not existing pool => system will initialize by default values
        PoolInfo storage _poolInfo = poolInfo[poolId];

        // validate: the pool Id must be existed and activated
        require(_poolInfo.isActive == false, 'ReservePool: Pool Id was created');

        // activate PoolId
        _poolInfo.isActive = true;

        emit CreatePool(poolId);
    }

    function joinPool(
        address investor,
        string memory poolId,
        uint256 numberOfLIFE
    )
        external
        override
        onlyGFNOperator
        activePoolId(poolId)
    {
        // validate: number of LIFE that investor want to invest into the pool
        require(
            numberOfLIFE > 0,
            "ReservePool: Investing LIFE amount must be greater than zero"
        );

        IParticipantWallet investorWallet = IParticipantWallet(
            _getInvestorWalletAddress(registry)
        );

        require(
            numberOfLIFE <= investorWallet.getBalanceOfParticipant(investor),
            "ReservePool: investor has no enough LIFE to join pool in InvestorWallet"
        );

        // retrieve PoolInfo by PoolId
        PoolInfo storage _poolInfo = poolInfo[poolId];

        // append a new slot to pools
        pools[poolId][_poolInfo.lastSlotIndex] = Slot(investor, numberOfLIFE);

        // update balance of Pool and last Index in the _poolInfo
        _poolInfo.balanceOfPool += numberOfLIFE;
        _poolInfo.lastSlotIndex += 1;

        // increase total invested LIFE of investor by new number of LIFE
        balanceOfInvestors[investor][poolId] += numberOfLIFE;

        // transfer LIFE of investor from InvestorWallet to ReservePoolWallet
        investorWallet.transferToAnotherParticipantWallet(
            investor,
            _getReservePoolWalletAddress(registry),
            investor,
            numberOfLIFE
        );

        emit JoinPool(investor, poolId, numberOfLIFE);
    }

    function requestCoInvestors(
        address geneticProfileOwner,
        string memory requestedPoolId,
        uint256 requestedNumerOfLIFE
    )
        external
        override
        onlyGFNOperator
        activePoolId(requestedPoolId)
    {
        // retrieve PoolInfo by PoolId
        PoolInfo storage _poolInfo = poolInfo[requestedPoolId];

        // validate requestedNumerOfLIFE
        require(
            requestedNumerOfLIFE > 0, 
            "ReservePool: requested number of LIFE must be greater than zero"
        );
        require(
            requestedNumerOfLIFE <= _poolInfo.balanceOfPool, 
            "ReservePool: requested pool does not have enough number of LIFE"
        );

        uint256 remainingRequestedNumberOfLIFE = requestedNumerOfLIFE;
        do {
            // loop through each slot of the requested pool, 
            // start from the first slot
            Slot storage currentSlot = pools[requestedPoolId][_poolInfo.firstSlotIndex];
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
                delete pools[requestedPoolId][_poolInfo.firstSlotIndex];
                // move the _poolInfo to the next slot
                _poolInfo.firstSlotIndex += 1;
            }
        } while (remainingRequestedNumberOfLIFE > 0
            && _poolInfo.firstSlotIndex < _poolInfo.lastSlotIndex);

        // decrease balance of pool after finding out co-investor
        _poolInfo.balanceOfPool -= requestedNumerOfLIFE;

        emit RequestCoInvestors(
            geneticProfileOwner, requestedPoolId, requestedNumerOfLIFE
        );
    }
    function _makeRevenueSharingArrangement(
        address geneticProfileOwner,
        address investor,
        uint256 investedNumberOfLIFE
    ) private {

        // Make Arrangement between Investors and GPOwner
        IRevenueSharingArrangement arrangement = IRevenueSharingArrangement(
            _getRevenueSharingArrangementAddress(registry)
        );
        arrangement.makeArrangementBetweenGeneticProfileOwnerAndInvestor(
            geneticProfileOwner, investor, investedNumberOfLIFE
        );

        // transfer LIFE of Investor from RPWallet to GFN Wallet
        IParticipantWallet  reserve_pool_wallet = IParticipantWallet(
            _getReservePoolWalletAddress(registry)
        );
        reserve_pool_wallet.transferExternally(
            investor,
            _getGeneFriendNetworkWalletAddress(registry),
            investedNumberOfLIFE
        );
    }

    function exitPool(
        address investor,
        string memory poolId,
        uint256 exitedNumberOfLIFE
    )
        external
        override
        onlyGFNOperator
        activePoolId(poolId)
    {
        uint256 currentNumberOfLIFE = balanceOfInvestors[investor][poolId];
        require(
            exitedNumberOfLIFE > 0,
            "ReservePool: Exited number of LIFE must be greater than zero"
        );
        require(
            exitedNumberOfLIFE <= currentNumberOfLIFE,
            "ReservePool: Exited number of LIFE exceeds current balance"
        );

        _decreaseBalanceOfInvestor(investor, poolId, exitedNumberOfLIFE);

        // transfer LIFE of Investor from RPWallet to InvestorWallet
        IParticipantWallet  reserve_pool_wallet = IParticipantWallet(
            _getReservePoolWalletAddress(registry)
        );
        reserve_pool_wallet.transferToAnotherParticipantWallet(
            investor,
            _getInvestorWalletAddress(registry),
            investor,
            exitedNumberOfLIFE
        );

        emit ExitPool(investor, poolId, exitedNumberOfLIFE);
    }

    function _decreaseBalanceOfInvestor(
        address investor,
        string memory poolId,
        uint256 numberOfLIFE
    ) private {
        // retrieve PoolInfo by PoolId
        PoolInfo storage _poolInfo = poolInfo[poolId];

        uint256 remainingNumberOfLIFE = numberOfLIFE;
        Slot storage _slot;
        for (uint256 index = _poolInfo.firstSlotIndex; index < _poolInfo.lastSlotIndex; index++) {
            _slot = pools[poolId][index];
            if (_slot.investor == investor) {
                if (remainingNumberOfLIFE < _slot.availableNumberOfLIFE) {
                    _slot.availableNumberOfLIFE -= remainingNumberOfLIFE;
                    remainingNumberOfLIFE = 0;
                } else {
                    remainingNumberOfLIFE -= _slot.availableNumberOfLIFE;
                    _slot.availableNumberOfLIFE = 0;
                }

                if (remainingNumberOfLIFE == 0) break;
            }
        }

        _poolInfo.balanceOfPool -= numberOfLIFE;
        balanceOfInvestors[investor][poolId] -= numberOfLIFE;
    }

    function getStatusOfPool(string memory poolId) external override view returns (bool) {
        return poolInfo[poolId].isActive;
    }

    function getBalanceOfPool(string memory poolId) external override view returns (uint256) {
        return poolInfo[poolId].balanceOfPool;
    }

    function getBalanceOfInvestor(
        address investor,
        string memory poolId
    ) external override view returns (uint256) {
        return balanceOfInvestors[investor][poolId];
    }

}
