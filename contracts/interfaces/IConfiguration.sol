// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

interface IConfiguration {

    event SetBaseGNFTTokenURI(string baseURI);
    event SetOperator(
        address indexed contractAddress,
        address indexed oldOperator,
        address indexed newOperator
    );

    function setOperator(address contractAddress, address newOperator) external;
    function setBaseGNFTTokenURI(string memory baseURI) external;

    function getBaseGNFTTokenURI() external view returns (string memory);
    function getOperator(address contractAddress) external view returns (address);

    function findNumberOfLIFEToMint(
        uint256 totalGNFTTokens
    ) external view returns (uint256);

    function getRevenueDistributionRatios(
        uint256 totalInvestedLIFEOfInvestors,
        uint256 totalAccumulatedRevenue,
        uint256 newRevenue
    ) external view returns (uint256[4] memory);

}
