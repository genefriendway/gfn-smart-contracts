// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

interface IDataUtilization {

    event PayToAccess(
        address indexed fromParticipantWallet,
        address indexed fromSender,
        uint256[] receivedTokenIds,
        uint256[] receivedLIFEAmounts
    );

    function payToAccess(
        address fromParticipantWallet,
        address fromSender,
        uint256[] memory receivedTokenIds,
        uint256[] memory receivedLIFEAmounts
    ) external;

}