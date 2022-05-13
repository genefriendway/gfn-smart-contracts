// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

/**
 * @dev Interface of the IGenomicDAOToken2LIFE
 */

interface IGenomicDAOToken2LIFE {
    // Events
    event GenomicDaoTokenExchangedToLife(
        uint256 amountGenomicDaoToken,
        uint256 amountLife,
        address indexed fromLifeSource,
        address indexed to
    );

    event SwapExactTokensForTokensByKyberSwap(
        uint256 amountGenomicDAOTokenIn,
        uint256 amountLIFEOutMin,
        address addressReceiveLIFE,
        address[] bridgeTokens,
        address[] poolsPath,
        address kyberSwapRouter
    );

    event GenomicDaoTokenWithdrawnToBuyLife(uint256 amount, address indexed to);

    // Functions
    function exchangeGenomicDaoTokenToLife(
        uint256 amountGenomicDaoToken,
        uint256 amountLife,
        address fromLifeSource,
        address to
    ) external;

    function swapExactTokensForTokensByKyberSwap(
        uint256 amountGenomicDAOTokenIn,
        uint256 amountLIFEOutMin,
        address addressReceiveLIFE,
        address[] memory bridgeTokens,
        address[] memory poolsPath,
        address kyberSwapRouter
    ) external;

    function withdrawGenomicDaoTokenToBuyLife(uint256 amount, address to) external;
}
