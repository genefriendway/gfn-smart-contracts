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
    address private _lifeAddress;
    address private _genomicDaoTokenAddress;
    address private _lifeReserveAddress; // Reserve to store exchanged LIFE from genomic dao token

    constructor(
        address owner,
        address genomicDaoToken,
        address lifeToken,
        address reserve
    ) {
        _genomicDaoTokenAddress = genomicDaoToken;
        _lifeAddress = lifeToken;
        _lifeReserveAddress = reserve;

        transferOwnership(owner);
    }

    /**
     * Spend GenomicDaoToken that stores in the smart contract to exchange for LIFE
     * and transfer exchanged LIFE to `_lifeReserveAddress` address
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
        address fromLifeSource,
        address to
    ) external onlyOwner {
        IERC20 lifeToken = IERC20(_lifeAddress);
        IERC20 genomicDaoToken = IERC20(_genomicDaoTokenAddress);

        uint256 genomicDaoTokenBalance = genomicDaoToken.balanceOf(
            address(this)
        );
        uint256 allowance = lifeToken.allowance(fromLifeSource, address(this));

        // Validations
        require(
            genomicDaoTokenBalance >= amountGenomicDaoToken,
            "Genomic Dao Token amount exceeds balance"
        );

        require(allowance >= amountLife, "LIFE allowance was not enough");

        require(to != address(0), "To address is zero address");

        // Transfer GenomicDAO token `to` address
        SafeERC20.safeTransfer(genomicDaoToken, to, amountGenomicDaoToken);

        // Transfer LIFE token to reserve address
        SafeERC20.safeTransferFrom(
            lifeToken,
            fromLifeSource,
            _lifeReserveAddress,
            amountLife
        );

        // Emit events
        emit GenomicDaoTokenExchangedToLife(
            amountGenomicDaoToken,
            amountLife,
            fromLifeSource,
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

        IERC20 genomicDaoToken = IERC20(_genomicDaoTokenAddress);

        // Transfer LIFE token `to` address
        SafeERC20.safeTransfer(genomicDaoToken, to, amount);

        // Emit events
        emit GenomicDaoTokenWithdrawn(amount, to);
    }

    /**
     * Returns the address of LIFE token
     */
    function lifeToken() public view returns (address) {
        return _lifeAddress;
    }

    /**
     * Return the address of GenomicDAOToken
     */
    function genomicDaoToken() public view returns (address) {
        return _genomicDaoTokenAddress;
    }
}
