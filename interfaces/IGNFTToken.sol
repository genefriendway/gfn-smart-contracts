// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IGNFTToken {

    event MintGNFT(
        address indexed geneticProfileOwner,
        string geneticProfileId,
        uint256 geneticDataId
    );
    event BurnGNFT(uint256 geneticProfileId);

    function mintGNFT(
        address geneticProfileOwner,
        string memory geneticProfileId,
        uint256 geneticDataId
    ) external;
    function burnGNFT(uint256 geneticDataId) external;

    function getTotalGeneticData() external view returns (uint256);

}