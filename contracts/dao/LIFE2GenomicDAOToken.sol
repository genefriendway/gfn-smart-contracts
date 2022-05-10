// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../interfaces/ILIFE2GenomicDAOToken.sol";

/**
 * Lock amount of LIFE token that only can be used to buy DAO Token
 * or amount of DAO token that only can be used to buy LIFE token
 */

contract LIFE2GenomicDAOToken is ILIFE2GenomicDAOToken, Ownable {
    using SafeERC20 for IERC20;

    // state variables
    address lifeAddress;
    address genomicDaoTokenAddress;
    address genomicDaoTokenReserveAddress; // Reserve to store exchanged token from LIFE

    constructor(
        address owner,
        address genomicDaoToken,
        address lifeToken,
        address reserve
    ) {
        genomicDaoTokenAddress = genomicDaoToken;
        lifeAddress = lifeToken;
        genomicDaoTokenReserveAddress = reserve;

        transferOwnership(owner);
    }

    /**
     * Spend LIFE token that stores in the smart contract to exchange for DAOToken
     * and transfer exchanged DAOToken to `genomicDaoTokenReserveAddress` address
     *
     * Requirements:
     *
     * - contract must have at least `amountLife` tokens
     * - contract must have approval to spend `amountGenomicDaoToken`
     * - `to` address must not zero address
     */
    function exchangeLifeToGenomicDaoToken(
        uint256 amountLife,
        uint256 amountGenomicDaoToken,
        address fromGenomicDaoTokenSource,
        address to
    ) external onlyOwner {
        IERC20 lifeToken = IERC20(lifeAddress);
        IERC20 genomicDaoToken = IERC20(genomicDaoTokenAddress);

        uint256 lifeBalance = lifeToken.balanceOf(address(this));
        uint256 allowance = genomicDaoToken.allowance(
            fromGenomicDaoTokenSource,
            address(this)
        );

        // Validations
        require(lifeBalance >= amountLife, "LIFE amount exceeds balance");

        require(to != address(0), "To address is  zero address");

        require(
            allowance >= amountGenomicDaoToken,
            "GenomicDaoToken allowance was not enough"
        );

        // Transfer LIFE token `to` address
        SafeERC20.safeTransfer(lifeToken, to, amountLife);

        // Transfer Genomic Dao token to reserve address
        SafeERC20.safeTransferFrom(
            genomicDaoToken,
            fromGenomicDaoTokenSource,
            genomicDaoTokenReserveAddress,
            amountGenomicDaoToken
        );

        // Emit events
        emit LifeExchangedToGenomicDaoToken(
            amountLife,
            amountGenomicDaoToken,
            fromGenomicDaoTokenSource,
            to
        );
    }

    /**
     * Backup method to withdraw LIFE to avoid LIFE is locked in the contract
     *
     * Requirements:
     *
     * - `to` address must not zero address
     * - only owner of the contract can execute function
     */
    function withdrawLife(uint256 amount, address to) external onlyOwner {
        // Validation
        require(to != address(0), "To address is zero address");

        IERC20 lifeToken = IERC20(lifeAddress);

        // Transfer LIFE token `to` address
        SafeERC20.safeTransfer(lifeToken, to, amount);

        // Emit events
        emit LifeWithdrawn(amount, to);
    }
}
