// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/**
 * @dev Interface of the DAOTokenLock
 */

interface IDAOToken2LIFE {
    // Events
    event LifeSoldToBuyDaoToken(uint256 amount);
    event GenomicDaoTokenSoldToBuyLife(uint256 amount);

    // Functions
    function sellLifeToBuyGenomicDaoToken(address to, uint256 amount) external;

    function sellGenomicDaoTokenToBuyLife(address to, uint256 amount) external;
}
