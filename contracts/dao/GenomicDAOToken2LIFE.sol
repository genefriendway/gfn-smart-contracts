// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../interfaces/kyberswap/IDMMRouter02.sol";
import "../interfaces/IGenomicDAOToken2LIFE.sol";

/**
 * Lock amount of LIFE token that only can be used to buy DAO Token
 * or amount of DAO token that only can be used to buy LIFE token
 */

contract GenomicDAOToken2LIFE is IGenomicDAOToken2LIFE, Ownable {
    using SafeERC20 for IERC20;

    // state variables
    address private immutable _lifeAddress;
    address private immutable _genomicDaoTokenAddress;
    address private immutable _lifeReserveAddress; // Reserve to store exchanged LIFE from genomic dao token

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
     * Withdraw Genomic Dao Token to buy Life
     *
     * Requirements:
     *
     * - `to` address must not zero address
     * - contract must have at least `amount` DAO tokens
     * - only owner of the contract can execute function
     */
    function withdrawGenomicDaoTokenToBuyLife(uint256 amount, address to)
        external
        onlyOwner
    {
        // Validation
        require(to != address(0), "To address is zero address");

        IERC20 genomicDaoToken = IERC20(_genomicDaoTokenAddress);

        require(
            genomicDaoToken.balanceOf(address(this)) >= amount,
            "Dao Token amount exceeds balance"
        );

        // Transfer LIFE token `to` address
        SafeERC20.safeTransfer(genomicDaoToken, to, amount);

        // Emit events
        emit GenomicDaoTokenWithdrawnToBuyLife(amount, to);
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
        uint256 amountGenomicDAOTokenIn,
        uint256 amountLIFEOutMin,
        address addressReceiveLIFE,
        address[] memory bridgeTokens,
        address[] memory poolsPath,
        address kyberSwapRouter
    )
        external onlyOwner
    {
        //next we need to allow the kyberswap router to spend the token we just sent to this contract
        //by calling IERC20 approve you allow the uniswap contract to spend the tokens in this contract
        IERC20(_genomicDaoTokenAddress).approve(
            kyberSwapRouter,
            amountGenomicDAOTokenIn
        );

        // build path of tokens for exchange
        IERC20[] memory tokensPath = new IERC20[](2 + bridgeTokens.length);
        // setup input token
        tokensPath[0] = IERC20(_genomicDaoTokenAddress);
        // setup bridge tokens
        for (uint256 i = 0; i < bridgeTokens.length; i++) {
            tokensPath[i + 1] = IERC20(bridgeTokens[i]);
        }
        // setup output token
        tokensPath[bridgeTokens.length + 1] = IERC20(_lifeAddress);

        require(
            (tokensPath.length - 1) == poolsPath.length,
            "GenomicDAOToken2LIFE: tokensPath and poolsPath invalid."
        );

        //then we will call swapExactTokensForTokens
        //for the deadline we will pass in block.timestamp
        //the deadline is the latest time the trade is valid for
        IDMMRouter02(kyberSwapRouter).swapExactTokensForTokens(
            amountGenomicDAOTokenIn,
            amountLIFEOutMin,
            poolsPath,
            tokensPath,
            addressReceiveLIFE,
            block.timestamp
        );

        emit SwapExactTokensForTokensByKyberSwap(
            amountGenomicDAOTokenIn,
            amountLIFEOutMin,
            addressReceiveLIFE,
            bridgeTokens,
            poolsPath,
            kyberSwapRouter
        );
    }
}
