// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface ITokenWallet {
    // Events
    event IncreaseBalance(address toAddress, uint256 amount, string description);
    event DecreaseBalance(address fromAddress, uint256 amount, string description);
    event TransferTokenFrom(
        address fromAddress,
        address toAddress,
        uint256 amount,
        string description
    );
    event TransferToken(
        address toAddress,
        uint256 amount,
        string description
    );

    // Functions
    function getTokenAddress() external view returns (address);
    function getBalance(address fromAddress) external view returns (uint256);
    function getTotalBalance() external view returns (uint256);

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
