// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "./interfaces/IContractRegistry.sol";
import "./interfaces/IParticipantWallet.sol";
import "./mixins/LIFETokenRetriever.sol";
import "./mixins/AccessibleRegistry.sol";


contract ParticipantWallet is
    IParticipantWallet,
    AccessibleRegistry,
    LIFETokenRetriever
{
    using SafeERC20 for IERC20;

    mapping(address => uint256) private balancesOfParticipant;

    modifier onlyOperatorOrRegisteredContract() {
        require(
            checkSenderIsOperator() || registry.isRegisteredContract(msg.sender),
            "ParticipantWallet: caller is not the owner or registered contract"
        );
        _;
    }

    constructor(IContractRegistry _registry) AccessibleRegistry(_registry) {}

    function transferInternally(
        address sender,
        address receiver,
        uint256 amount
    ) external override onlyOperatorOrRegisteredContract {
        // validate: must have enough balance of sender
        require(
            balancesOfParticipant[sender] >= amount,
            "ParticipantWallet: sender has not enough amount to send internally"
        );
        // decrease balance of sender and increase balance of receiver in the same wallet
        balancesOfParticipant[sender] -= amount;
        balancesOfParticipant[receiver] += amount;

        emit TransferInternally(sender, receiver, amount);
    }

    function transferToAnotherParticipantWallet(
        address sender,
        address participantWallet,
        address receiver,
        uint256 amount
    ) external override onlyOperatorOrRegisteredContract {
        // validate: must have enough balance of sender
        require(
            balancesOfParticipant[sender] >= amount,
            "ParticipantWallet: sender has not enough amount to send to another participant wallet"
        );
        // decrease balance of sender
        balancesOfParticipant[sender] -= amount;
        // transfer real number of LIFE from wallet of sender to wallet of receiver
        SafeERC20.safeTransfer(
            IERC20(_getLIFETokenAddress(registry)), participantWallet, amount
        );
        // increase amount of receiver in received wallet
        IParticipantWallet(participantWallet).receiveFromExternal(receiver, amount);

        emit TransferToAnotherParticipantWallet(sender, receiver, participantWallet, amount);
    }

    function transferExternally(
        address sender,
        address receiver,
        uint256 amount
    ) external override onlyOperatorOrRegisteredContract {
        // validate: must have enough balance of sender
        require(
            balancesOfParticipant[sender] >= amount,
            "ParticipantWallet: sender has not enough amount to send to GFN wallet"
        );
        // decrease balance of sender
        balancesOfParticipant[sender] -= amount;
        // transfer real number of LIFE from wallet of sender to receiver
        SafeERC20.safeTransfer(
            IERC20(_getLIFETokenAddress(registry)), receiver, amount
        );

        emit TransferExternally(sender, receiver, amount);
    }

    function receiveFromExternal(
        address receiver,
        uint256 amount
    ) external override onlyOperatorOrRegisteredContract {
        balancesOfParticipant[receiver] += amount;
        emit ReceiveFromExternal(receiver, amount);
    }

    function getBalanceOfWallet() external view returns (uint256) {
        return IERC20(_getLIFETokenAddress(registry)).balanceOf(address(this));
    }

    function getBalanceOfParticipant(
        address participant
    ) external override view returns (uint256) {
        return balancesOfParticipant[participant];
    }
}
