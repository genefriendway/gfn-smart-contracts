// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IParticipantWallet {

    event TransferInternally(
        address indexed sender,
        address indexed receiver,
        uint256 amount
    );
    event TransferToAnotherParticipantWallet(
        address indexed sender,
        address indexed receiver,
        address indexed participantWallet,
        uint256 amount
    );
    event TransferExternally(
        address indexed sender,
        address indexed receiver,
        uint256 amount
    );
    event ReceiveFromExternal(
        address indexed receiver,
        uint256 amount
    );

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

    function transferExternally(
        address sender,
        address receiver,
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
