// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface ITokenWallet {
    // Events
    event AddOperator(address indexed operatorAddress);
    event RemoveOperator(address indexed operatorAddress);
    event IncreaseBalance(address indexed toAddress, uint256 amount, string description);
    event DecreaseBalance(address indexed fromAddress, uint256 amount, string description);
    event TransferTokenFrom(
        address indexed fromAddress,
        address indexed toAddress,
        uint256 amount,
        string description
    );
    event TransferToken(
        address indexed toAddress,
        uint256 amount,
        string description
    );

    // Functions
    function getTokenAddress() external view returns (address);
    function getBalance(address fromAddress) external view returns (uint256);
    function getTotalBalance() external view returns (uint256);

    function addOperator(address operatorAddress) external;
    function removeOperator(address operatorAddress) external;
    function checkActiveOperator(address operatorAddress) external view returns (bool);

    function increaseBalance(address toAddress, uint256 amount, string memory description) external;
    function decreaseBalance(address fromAddress, uint256 amount, string memory description) external;

    function transferFrom(
        address fromAddress,
        address toAddress,
        uint256 amount,
        string memory description
    ) external;
    function transfer(address toAddress, uint256 amount, string memory description) external;

}
