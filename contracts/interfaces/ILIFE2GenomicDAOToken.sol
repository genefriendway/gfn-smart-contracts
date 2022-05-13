// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/**
 * @dev Interface of the ILIFE2GenomicDAOToken
 */

interface ILIFE2GenomicDAOToken {
    // Events
    event LifeExchangedToGenomicDaoToken(
        uint256 amountLife,
        uint256 amountGenomicDaoToken,
        address indexed fromGenomicDaoTokenSource,
        address indexed to
    );
    event LifeWithdrawnToBuyGenomicDaoToken(uint256 amount, address indexed to);

    // Functions
    function exchangeLifeToGenomicDaoToken(
        uint256 amountLife,
        uint256 amountGenomicDaoToken,
        address fromGenomicDaoTokenSource,
        address to
    ) external;

    function withdrawLifeToBuyPCSP(uint256 amount, address to) external;
}
