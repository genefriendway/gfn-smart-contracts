// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface ILIFEToken {

    event MintLIFE(address to, string geneticProfileId, uint256 geneticDataId);
    event BurnLIFE(address account, uint256 amount);

    function mintLIFE(string memory geneticProfileId, uint256 geneticDataId) external;
    function burnLIFE(uint256 amount) external;
}