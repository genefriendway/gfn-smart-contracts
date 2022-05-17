// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../interfaces/kyberswap/IDMMRouter02.sol";
import "../interfaces/ILIFE2GenomicDAOToken.sol";

/**
 * Lock amount of LIFE token that only can be used to buy DAO Token
 * or amount of DAO token that only can be used to buy LIFE token
 */

contract LIFE2GenomicDAOToken is ILIFE2GenomicDAOToken, Ownable {
    using SafeERC20 for IERC20;

    // state variables
    address _lifeAddress;
    address _genomicDaoTokenAddress;
    address _genomicDaoTokenReserveAddress; // Reserve to store exchanged token from LIFE

    constructor(
        address owner,
        address lifeToken,
        address genomicDaoToken,
        address reserve
    ) {
        _lifeAddress = lifeToken;
        _genomicDaoTokenAddress = genomicDaoToken;
        _genomicDaoTokenReserveAddress = reserve;

        transferOwnership(owner);
    }

    /**
     * Spend LIFE token that stores in the smart contract to exchange for DAOToken
     * and transfer exchanged DAOToken to `_genomicDaoTokenReserveAddress` address
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
        IERC20 lifeToken = IERC20(_lifeAddress);
        IERC20 genomicDaoToken = IERC20(_genomicDaoTokenAddress);

        uint256 lifeBalance = lifeToken.balanceOf(address(this));
        uint256 allowance = genomicDaoToken.allowance(
            fromGenomicDaoTokenSource,
            address(this)
        );

        // Validations
        require(lifeBalance >= amountLife, "LIFE amount exceeds balance");

        require(to != address(0), "To address is zero address");

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
            _genomicDaoTokenReserveAddress,
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
     * Withdraw LIFE to buy Genomic Dao Token
     *
     * Requirements:
     *
     * - `to` address must not zero address
     * - contract must have at least `amount` LIFE tokens
     * - only owner of the contract can execute function
     */
    function withdrawLifeToBuyPCSP(uint256 amount, address to)
        external
        onlyOwner
    {
        // Validation
        require(to != address(0), "To address is zero address");

        IERC20 lifeToken = IERC20(_lifeAddress);

        require(
            lifeToken.balanceOf(address(this)) >= amount,
            "LIFE amount exceeds balance"
        );

        // Transfer LIFE token `to` address
        SafeERC20.safeTransfer(lifeToken, to, amount);

        // Emit events
        emit LifeWithdrawnToBuyGenomicDaoToken(amount, to);
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

    function swapExactTokensForTokensByKyberSwap(
        uint256 amountLIFEIn,
        uint256 amountGenomicDAOTokenOutMin,
        address addressReceiveGenomicDAOToken,
        address[] memory bridgeTokens,
        address[] memory poolsPath,
        address kyberSwapRouter
    ) external onlyOwner {
        //next we need to allow the kyberswap router to spend the token we just sent to this contract
        //by calling IERC20 approve you allow the uniswap contract to spend the tokens in this contract
        IERC20(_lifeAddress).approve(kyberSwapRouter, amountLIFEIn);

        // build path of tokens for exchange
        IERC20[] memory tokensPath = new IERC20[](2 + bridgeTokens.length);
        // setup input token
        tokensPath[0] = IERC20(_lifeAddress);
        // setup bridge tokens
        for (uint256 i = 0; i < bridgeTokens.length; i++) {
            tokensPath[i + 1] = IERC20(bridgeTokens[i]);
        }
        // setup output token
        tokensPath[bridgeTokens.length + 1] = IERC20(_genomicDaoTokenAddress);

        require(
            (tokensPath.length - 1) == poolsPath.length,
            "LIFE22GenomicDAOToken: tokensPath and poolsPath invalid."
        );

        //then we will call swapExactTokensForTokens
        //for the deadline we will pass in block.timestamp
        //the deadline is the latest time the trade is valid for
        IDMMRouter02(kyberSwapRouter).swapExactTokensForTokens(
            amountLIFEIn,
            amountGenomicDAOTokenOutMin,
            poolsPath,
            tokensPath,
            addressReceiveGenomicDAOToken,
            block.timestamp
        );

        emit SwapExactTokensForTokensByKyberSwap(
            amountLIFEIn,
            amountGenomicDAOTokenOutMin,
            addressReceiveGenomicDAOToken,
            bridgeTokens,
            poolsPath,
            kyberSwapRouter
        );
    }
}
