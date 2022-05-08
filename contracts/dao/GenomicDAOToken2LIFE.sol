// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "../interfaces/IGenomicDAOToken2LIFE.sol";

/**
 * Lock amount of LIFE token that only can be used to buy DAO Token
 * or amount of DAO token that only can be used to buy LIFE token
 */

contract GenomicDAOToken2LIFE is IDAOToken2LIFE, Ownable {
    // state variables
    address lifeAddress;
    address genomicDaoTokenAddress;

    constructor(
        address owner,
        address lifeToken,
        address genomicDaoToken
    ) {
        lifeAddress = lifeToken;
        genomicDaoTokenAddress = genomicDaoToken;

        transferOwnership(owner);
    }

    /**
     * Sell `amount` of LIFE tokens, by transferring them to `to` address
     *
     * Requirements:
     *
     * - contract must have at least `amount` LIFE tokens
     * - `to` address must not zero address
     * - only owner of the contract can execute function
     */
    function sellLifeToBuyGenomicDaoToken(address to, uint256 amount) external onlyOwner {
        require(to != address(0), "To address is  zero address");

        IERC20 lifeToken = IERC20(lifeAddress);

        require(
            lifeToken.balanceOf(address(this)) >= amount,
            "Sell LIFE amount exceeds balance"
        );

        // Transfer LIFE token
        lifeToken.transfer(to, amount);

        // Emit event
        emit LifeSoldToBuyDaoToken(amount);

    }

    /**
     * Sell `amount` of DAO tokens, by transferring them to `to` address
     *
     * Requirements:
     *
     * - contract must have at least `amount` DAO tokens
     * - `to` address must not zero address
     * - only owner of the contract can execute function
     */
    function sellGenomicDaoTokenToBuyLife(address to, uint256 amount) external onlyOwner {
        require(to != address(0), "To address is  zero address");

        IERC20 daoToken = IERC20(genomicDaoTokenAddress);

        require(
            daoToken.balanceOf(address(this)) >= amount,
            "Sell Dao Token amount exceeds balance"
        );

        // Transfer LIFE token
        daoToken.transfer(to, amount);

        // Emit event
        emit GenomicDaoTokenSoldToBuyLife(amount);

    }
}
