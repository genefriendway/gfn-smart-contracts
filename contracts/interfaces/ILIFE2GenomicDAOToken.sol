// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/**
 * @dev Interface of the DAOTokenLock
 */

interface ILIFE2GenomicDAOToken {
    // Events
    event LifeExchangedToGenomicDaoToken(
        uint256 amountLife,
        uint256 amountGenomicDaoToken,
        address indexed from,
        address indexed to
    );
    event LifeWithdrawn(uint256 amount, address indexed to);

    // Functions
    function exchangeLifeToGenomicDaoToken(
        uint256 amountLife,
        uint256 amountGenomicDaoToken,
        address from,
        address to
    ) external;

    function withdrawLife(uint256 amount, address to) external;
}
