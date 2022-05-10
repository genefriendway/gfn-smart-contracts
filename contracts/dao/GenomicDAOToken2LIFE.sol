// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../interfaces/IGenomicDAOToken2LIFE.sol";

/**
 * Lock amount of LIFE token that only can be used to buy DAO Token
 * or amount of DAO token that only can be used to buy LIFE token
 */

contract GenomicDAOToken2LIFE is IGenomicDAOToken2LIFE, Ownable {
    using SafeERC20 for IERC20;

    // state variables
    address lifeAddress;
    address genomicDaoTokenAddress;
    address lifeReserveAddress; // Reserve to store exchanged LIFE from genomic dao token

    constructor(
        address owner,
        address lifeToken,
        address genomicDaoToken,
        address reserve
    ) {
        lifeAddress = lifeToken;
        genomicDaoTokenAddress = genomicDaoToken;
        lifeReserveAddress = reserve;

        transferOwnership(owner);
    }

    /**
     * Spend GenomicDaoToken that stores in the smart contract to exchange for LIFE
     * and transfer exchanged LIFE to `lifeReserveAddress` address
     *
     * Requirements:
     *
     * - contract must have at least `amountGenomicDaoToken` tokens
     * - contract must have approval to spend `amountLife`
     * - `to` address must not zero address
     */
    function exchangeGenomicDaoTokenToLife(
        uint256 amountGenomicDaoToken,
        uint256 amountLife,
        address from,
        address to
    ) external onlyOwner {
        IERC20 lifeToken = IERC20(lifeAddress);
        IERC20 genomicDaoToken = IERC20(genomicDaoTokenAddress);

        uint256 genomicDaoTokenBalance = genomicDaoToken.balanceOf(
            address(this)
        );
        uint256 allowance = lifeToken.allowance(from, address(this));

        // Validations
        require(
            genomicDaoTokenBalance >= amountGenomicDaoToken,
            "Genomic Dao Token amount exceeds balance"
        );

        require(allowance >= amountLife, "LIFE allowance was not enough");

        require(to != address(0), "To address is zero address");

        // Transfer GenomicDAO token `to` address
        SafeERC20.safeTransfer(genomicDaoToken, to, amountGenomicDaoToken);

        // Transfer LIFE token reserve address
        SafeERC20.safeTransferFrom(
            lifeToken,
            from,
            lifeReserveAddress,
            amountLife
        );

        // Emit events
        emit GenomicDaoTokenExchangedToLife(
            amountGenomicDaoToken,
            amountLife,
            from,
            to
        );
    }

    /**
     * Backup method to withdraw Genomic Dao Token to avoid Genomic Dao Token is locked in the contract
     *
     * Requirements:
     *
     * - `to` address must not zero address
     * - only owner of the contract can execute function
     */
    function withdrawGenomicDaoToken(uint256 amount, address to)
        external
        onlyOwner
    {
        // Validation
        require(to != address(0), "To address is zero address");

        IERC20 genomicDaoToken = IERC20(genomicDaoTokenAddress);

        // Transfer LIFE token `to` address
        SafeERC20.safeTransfer(genomicDaoToken, to, amount);

        // Emit events
        emit GenomicDaoTokenWithdrawn(amount, to);
    }
}
