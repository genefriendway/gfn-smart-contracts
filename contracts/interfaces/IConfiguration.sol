// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

interface IConfiguration {

    function findNumberOfLIFEToMint(
        uint256 totalGNFTTokens
    ) external view returns (uint256);

    function getRevenueDistributionRatios(
        uint256 totalInvestedLIFEOfInvestors,
        uint256 totalAccumulatedRevenue,
        uint256 newRevenue
    ) external view returns (uint256[4] memory);

}
