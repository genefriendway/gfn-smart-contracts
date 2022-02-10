// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IReservePool {

    struct Slot {
        address investor;
        uint256 availableNumberOfLIFE;
    }

    struct PoolPointer {
        uint256 firstIndex;
        uint256 lastIndex;
        uint256 balanceOfPool;
        bool isActive;
    }

    event CreatePool(string poolId);
    event JoinPool(
        address indexed investor,
        string indexed poolId,
        uint256 numberOfLIFE
    );
    event ExitPool(
        address indexed investor,
        string indexed poolId,
        uint256 numberOfLIFE
    );
    event RequestCoInvestors(
        address indexed geneticProfileOwner,
        string indexed requestedPoolId,
        uint256 requestedNumerOfLIFE
    );

    function createPool(string memory poolId) external;
    function joinPool(
        address investor,
        string memory poolId,
        uint256 numberOfLIFE
    ) external;
    function exitPool(
        address investor,
        string memory poolId,
        uint256 numberOfLIFE
    ) external;
    function requestCoInvestors(
        address geneticProfileOwner,
        string memory requestedPoolId,
        uint256 requestedNumerOfLIFE
    ) external;
    function getStatusOfPool(string memory poolId) external returns (bool);
    function getBalanceOfPool(string memory poolId) external returns (uint256);
    function getBalanceOfInvestor(
        address investor,
        string memory poolId
    ) external returns (uint256);
}
