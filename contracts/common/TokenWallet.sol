// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../interfaces/common/ITokenWallet.sol";


contract TokenWallet is ITokenWallet, Ownable {
    // State Variables
    address private _tokenAddress;
    // Mapping: address of token owner => amount of token
    mapping(address => uint256) private _balances;
    uint256 private _totalBalance;

    // Mapping: address of operator => status
    mapping(address => bool) private _operators;


    // Modifiers
    modifier onlyOperator() {
        require(
            _operators[_msgSender()],
            "TokenWallet: caller must be the operator"
        );
        _;
    }

    modifier notNullAddress(address _address) {
        require(
            _address != address(0),
            "TokenWallet: address must not be null"
        );
        _;
    }

    modifier positiveAmount(uint256 amount) {
        require(
            amount > 0,
            "TokenWallet: amount must be greater than zero"
        );
        _;
    }

    constructor(
        address owner,
        address tokenAddress
    )
        notNullAddress(owner)
        notNullAddress(tokenAddress)
    {
        _tokenAddress = tokenAddress;
        _operators[owner] = true; // set owner as an operator
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

    function addOperator(address operatorAddress) external onlyOwner {
        require(
            operatorAddress != address(0),
            "TokenWallet: address of operator must be not null"
        );
        require(
            !_operators[operatorAddress],
            "TokenWallet: the operator was added"
        );
        _operators[operatorAddress] = true;
        emit AddOperator(operatorAddress);
    }

    function removeOperator(address operatorAddress) external onlyOwner {
        require(
            operatorAddress != address(0),
            "TokenWallet: address of operator must be not null"
        );
        require(
            _operators[operatorAddress],
            "TokenWallet: can not remove a operator that does not exist"
        );
        _operators[operatorAddress] = false;
        emit RemoveOperator(operatorAddress);
    }

    function checkActiveOperator(
        address operatorAddress
    ) external override view returns (bool) {
        return _operators[operatorAddress];
    }

    function deposit(
        address toAddress,
        uint256 amount,
        string memory description
    )
        external
        onlyOperator
    {
        _increase(toAddress, amount);
        emit Deposit(toAddress, amount, description);
    }

    function increaseBalance(
        address toAddress,
        uint256 amount,
        string memory description
    )
        external
        onlyOwner
    {
        // increase balance of 'fromAddress' on this contract
        _increase(toAddress, amount);
        emit IncreaseBalance(toAddress, amount, description);
    }

    function decreaseBalance(
        address fromAddress,
        uint256 amount,
        string memory description
    )
        external
        onlyOwner
    {
        // decrease balance of 'fromAddress' on this contract
        _decrease(fromAddress, amount);
        emit DecreaseBalance(fromAddress, amount, description);
    }

    function transferFrom(
        address fromAddress,
        address toAddress,
        uint256 amount,
        string memory description
    )
        external
        onlyOperator
    {
        // decrease balance of 'fromAddress' and increase balance of 'toAddress'
        _transferFrom(fromAddress, toAddress, amount);

        emit TransferFrom(fromAddress, toAddress, amount, description);
    }

    function withdrawFrom(
        address fromAddress,
        address toAddress,
        uint256 amount,
        string memory description
    )
        external
        onlyOperator
    {
        // decrease balance of 'fromAddress'
        _decrease(fromAddress, amount);
        // transfer real token from this contract to 'toAddress'
        _transferToken(toAddress, amount);

        emit WithdrawFrom(fromAddress, toAddress, amount, description);
    }

    function withdraw(
        address toAddress,
        uint256 amount,
        string memory description
    )
        external
        onlyOwner
    {
         // transfer real token from this contract to 'toAddress'
        _transferToken(toAddress, amount);

        emit Withdraw(toAddress, amount, description);
    }

    function _increase(
        address toAddress,
        uint256 amount
    )
        private
        notNullAddress(toAddress)
        positiveAmount(amount)
    {
        _balances[toAddress] += amount;
        _totalBalance += amount;
    }

    function _decrease(
        address fromAddress,
        uint256 amount
    )
        private
        notNullAddress(fromAddress)
        positiveAmount(amount)
    {
        require(
            _balances[fromAddress] >= amount,
            "TokenWallet: not enough balance"
        );

        _balances[fromAddress] -= amount;
        _totalBalance -= amount;
    }

    function _transferToken(address toAddress,  uint256 amount) private {
        SafeERC20.safeTransfer(IERC20(_tokenAddress), toAddress, amount);
    }

    function _transferFrom(
        address fromAddress,
        address toAddress,
        uint256 amount
    )
        private
        notNullAddress(fromAddress)
        notNullAddress(toAddress)
        positiveAmount(amount)
    {
        require(
            _balances[fromAddress] >= amount,
            "TokenWallet: not enough balance"
        );

        _balances[fromAddress] -= amount;
        _balances[toAddress] += amount;
        // total balance is not changed
    }
}
