// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/**
 * @dev Interface of the DAOTokenLock
 */

interface IDAOTokenLock {
    // Events
    event LifeSoldToBuyDaoToken(uint256 amount);
    event DaoTokenSoldToBuyLife(uint256 amount);

    // Functions
    function sellLifeToBuyDaoToken(address to, uint256 amount) external;

    function sellDaoTokenToBuyLife(address to, uint256 amount) external;
}
