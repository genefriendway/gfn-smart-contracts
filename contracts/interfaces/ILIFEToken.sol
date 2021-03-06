// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface ILIFEToken {

    event MintLIFE(address indexed to, uint256 geneticProfileId);
    event BurnLIFE(address indexed account, uint256 amount);

    function mintLIFE(uint256 geneticProfileId) external;
    function burnLIFE(uint256 amount) external;
}