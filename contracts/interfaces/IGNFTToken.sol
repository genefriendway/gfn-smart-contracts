// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IGNFTToken {

    event MintGNFT(
        address indexed geneticProfileOwner,
        uint256 geneticProfileId,
        address NFTHolder
    );
    event MintBatchGNFT(
        address[] geneticProfileOwners,
        uint256[] geneticProfileIds,
        bool approvalForGFN
    );
    event BurnGNFT(uint256 geneticProfileId, address indexed burnedBy);

    function mintBatchGNFT(
        address[] memory geneticProfileOwners,
        uint256[] memory geneticProfileIds,
        bool approvalForGFN
    ) external;

    function burnGNFT(uint256 geneticProfileId) external;

    function getTotalMintedGeneticProfiles() external view returns (uint256);

}