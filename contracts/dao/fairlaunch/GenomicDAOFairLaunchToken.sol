// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Capped.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./GasPriceController.sol";
import "./DexListing.sol";
import "./TransferFee.sol";
import "../../interfaces/IGenomicDAOFairLaunchToken.sol";

contract GenomicDAOFairLaunchToken is
    IGenomicDAOFairLaunchToken,
    GasPriceController,
    DexListing,
    TransferFee,
    Ownable,
    ERC20Capped
{
    constructor(
        address owner,
        string memory name,
        string memory symbol,
        uint256 duration,
        uint256 cap
    ) ERC20(name, symbol) ERC20Capped(cap) DexListing(duration) {
        transferOwnership(owner);
        _setTransferFee(_msgSender(), 0, 0, 0);
    }

    function mint(address account, uint256 amount) public override onlyOwner {
        _mint(account, amount);
    }

    function burn(uint256 amount) public override {
        _burn(_msgSender(), amount);
    }

    function _transfer(
        address sender_,
        address recipient_,
        uint256 amount_
    ) internal override onlyValidGasPrice {
        if (!_listingFinished) {
            uint256 fee = _updateAndGetListingFee(sender_, recipient_, amount_);
            require(fee <= amount_, "Token: listing fee too high");
            uint256 transferA = amount_ - fee;
            if (fee > 0) {
                super._transfer(sender_, _getTransferFeeTo(), fee);
            }
            super._transfer(sender_, recipient_, transferA);
        } else {
            uint256 transferFee = _getTransferFee(sender_, recipient_, amount_);
            require(transferFee <= amount_, "transferFee too high");

            uint256 transferA = amount_ - transferFee;
            if (transferFee > 0) {
                super._transfer(sender_, _getTransferFeeTo(), transferFee);
            }
            if (transferA > 0) {
                super._transfer(sender_, recipient_, transferA);
            }
        }
    }

    /*
    Settings
    */
    function setMaxGasPrice(uint256 maxGasPrice_) external override onlyOwner {
        _setMaxGasPrice(maxGasPrice_);
    }

    function setTransferFee(
        address to_,
        uint256 buyFee_,
        uint256 sellFee_,
        uint256 normalFee_
    ) external override onlyOwner {
        _setTransferFee(to_, buyFee_, sellFee_, normalFee_);
    }
}

