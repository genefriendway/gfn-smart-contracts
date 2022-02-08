// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IGeneFriendNetworkWallet {

    event Transfer(address receiver, uint256 indexed amount);
    event TransferToParticipantWallet(
        address participantWallet,
        address receiver,
        uint256 indexed amount
    );

    function transfer(
        address receiver,
        uint256 amount
    ) external;

    function transferToParticipantWallet(
        address participantWallet,
        address receiver,
        uint256 amount
    ) external;

    function getBalanceOfWallet() external view returns (uint256);
}
