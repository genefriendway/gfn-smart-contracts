// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IParticipantWallet {

    event TransferInternally(address sender, address receiver, uint256 indexed amount);
    event TransferToAnotherParticipantWallet(
        address sender,
        address receiver,
        address participantWallet,
        uint256 indexed amount
    );
    event TransferToGFNWallet(
        address sender,
        address gfnWallet,
        uint256 indexed amount
    );
    event ReceiveFromExternal(address receiver, uint256 indexed amount);

    function transferInternally(
        address sender,
        address receiver,
        uint256 amount
    ) external;

    function transferToAnotherParticipantWallet(
        address sender,
        address participantWallet,
        address receiver,
        uint256 amount
    ) external;

    function transferToGFNWallet(
        address sender,
        address gfnWallet,
        uint256 amount
    ) external;

    function receiveFromExternal(
        address receiver,
        uint256 amount
    ) external;

    function getBalanceOfWallet() external view returns (uint256);
    function getBalanceOfParticipant(
        address participant
    ) external view returns (uint256);
}
