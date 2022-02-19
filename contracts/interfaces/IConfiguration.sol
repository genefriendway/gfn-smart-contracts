// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

interface IConfiguration {

    function findNumberOfLIFEToMint(
        uint256 totalGNFTTokens
    ) external view returns (uint256);

}
