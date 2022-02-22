// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

interface IConfiguration {

    event SetBaseGNFTTokenURI(string uri);

    function getBaseGNFTTokenURI() external view returns (string memory);

    function findNumberOfLIFEToMint(
        uint256 totalGNFTTokens
    ) external view returns (uint256);

}
