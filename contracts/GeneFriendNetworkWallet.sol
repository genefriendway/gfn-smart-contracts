// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "./interfaces/IContractRegistry.sol";
import "./interfaces/IParticipantWallet.sol";
import "./interfaces/IGeneFriendNetworkWallet.sol";
import "./mixins/LIFETokenRetriever.sol";
import "./mixins/AccessibleRegistry.sol";


contract GeneFriendNetworkWallet is
    IGeneFriendNetworkWallet,
    AccessibleRegistry,
    LIFETokenRetriever
{
    using SafeERC20 for IERC20;

    constructor(IContractRegistry _registry) AccessibleRegistry(_registry) {}

    function transfer(
        address receiver,
        uint256 amount
    )
        external override onlyOperator
    {
        // validate: must have enough balance of wallet
        require(
            getBalanceOfWallet() >= amount,
            "GeneFriendNetWorkWallet: Wallet has not enough amount to transfer"
        );
        SafeERC20.safeTransfer(IERC20(_getLIFETokenAddress(registry)), receiver, amount);
        emit Transfer(receiver, amount);
    }

    function transferToParticipantWallet(
        address participantWallet,
        address receiver,
        uint256 amount
    )
        external override onlyOperator
    {
        // validate: must have enough balance of wallet
        require(
            getBalanceOfWallet() >= amount,
            "GeneFriendNetWorkWallet: Wallet has not enough amount to transfer"
        );
        // transfer real number of LIFE
        SafeERC20.safeTransfer(IERC20(_getLIFETokenAddress(registry)), participantWallet, amount);
        // increase amount of receiver in received wallet
        IParticipantWallet(participantWallet).receiveFromExternal(receiver, amount);

        emit TransferToParticipantWallet(participantWallet, receiver, amount);
    }

    function getBalanceOfWallet() public view returns (uint256) {
        return IERC20(_getLIFETokenAddress(registry)).balanceOf(address(this));
    }
}
