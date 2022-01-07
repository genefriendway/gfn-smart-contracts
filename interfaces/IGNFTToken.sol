// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IGNFTToken {

    event MintToken(address indexed geneticOwner, uint256 tokenId);
    event BurnToken(uint256 tokenId);

    function mintToken(address geneticOwner, uint256 tokenId) external;
    function burnToken(uint256 tokenId) external;

    function getTotalTokens() external view returns (uint256);

}