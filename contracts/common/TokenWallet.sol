// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../interfaces/common/ITokenWallet.sol";


contract TokenWallet is ITokenWallet, Ownable {
    // State Variables
    address private _tokenAddress;
    // Mapping: address => amount of token
    mapping(address => uint256) private _balances;
    uint256 private _totalBalance;


    // Modifiers
    modifier validTokenAddress(address _address) {
        require(
            _address != address(0),
            "TokenWallet: address of token wallet must not be null"
        );
        _;
    }

    constructor(
        address owner,
        address tokenAddress
    )
        validTokenAddress(tokenAddress)
    {
        _tokenAddress = tokenAddress;
        transferOwnership(owner);
    }

    function getTokenAddress() external override view returns (address) {
        return _tokenAddress;
    }

    function getBalance(address fromAddress) external override view returns (uint256) {
        return _balances[fromAddress];
    }

    function getTotalBalance() external override view returns (uint256) {
        return _totalBalance;
    }

    function increaseBalance(
        address toAddress,
        uint256 amount,
        string memory description
    )
        external
        onlyOwner
    {
        _increase(toAddress, amount, description);
    }

    function decreaseBalance(
        address fromAddress,
        uint256 amount,
        string memory description
    )
        external
        onlyOwner
    {
        _decrease(fromAddress, amount, description);
    }

    function transferFrom(
        address fromAddress,
        address toAddress,
        uint256 amount,
        string memory description
    )
        external
        onlyOwner
    {
        _decrease(fromAddress, amount, description);
        _transfer(toAddress, amount, description);
        emit TransferTokenFrom(fromAddress, toAddress, amount, description);
    }

    function transfer(
        address toAddress,
        uint256 amount,
        string memory description
    )
        external
        onlyOwner
    {
        _transfer(toAddress, amount, description);
    }

    function _increase(
        address toAddress,
        uint256 amount,
        string memory description
    )
        private
    {
        require(
            toAddress != address(0),
            "TokenWallet: toAddress must be not null"
        );
        require(
            amount > 0,
            "TokenWallet: amount must be greater than zero"
        );

        _balances[toAddress] += amount;
        _totalBalance += amount;
        emit IncreaseBalance(toAddress, amount, description);
    }

    function _decrease(
        address fromAddress,
        uint256 amount,
        string memory description
    )
        private
    {
        require(
            fromAddress != address(0),
            "TokenWallet: fromAddress must be not null"
        );
        require(
            amount > 0,
            "TokenWallet: amount must be greater than zero"
        );
        require(
            _balances[fromAddress] >= amount,
            "TokenWallet: not enough balance to decrease"
        );

        _balances[fromAddress] -= amount;
        _totalBalance -= amount;
        emit DecreaseBalance(fromAddress, amount, description);
    }

    function _transfer(
        address toAddress,
        uint256 amount,
        string memory description
    )
        private
    {
        SafeERC20.safeTransfer(IERC20(_tokenAddress), toAddress, amount);
        emit TransferToken(toAddress, amount, description);
    }
}
