// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface ILIFEToken {

    event MintLIFEToTreasury(address to, uint256 geneticId);
    event BurnLIFE(address account, uint256 amount);

    function mintLIFEToTreasury(uint256 geneticId) external;
    function burnLIFE(uint256 amount) external;
}