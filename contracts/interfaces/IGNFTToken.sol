// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IGNFTToken {

    event MintGNFT(
        address indexed geneticProfileOwner,
        uint256 geneticProfileId
    );
    event BurnGNFT(uint256 geneticProfileId);

    function mintGNFT(
        address geneticProfileOwner,
        uint256 geneticProfileId
    ) external;
    function burnGNFT(uint256 geneticProfileId) external;

    function getTotalMintedGeneticProfiles() external view returns (uint256);
    function getTotalCurrentTokens() external view returns (uint256);

}