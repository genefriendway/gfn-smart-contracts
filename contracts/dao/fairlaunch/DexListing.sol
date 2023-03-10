// SPDX-License-Identifier: MIT

pragma solidity ^0.8.11;

import "./OriginOwner.sol";
import "./libs/LDex.sol";

contract DexListing is OriginOwner {
    address public immutable uniswapV2Router;
    address public immutable wbnbPair;
    address public immutable busdPair;

    uint256 private _listingFeePercent = 0;
    uint256 private _listingDuration;
    uint256 private _listingStartAt;
    uint256 private _finishListingFeePercent = 0;

    bool internal _listingFinished;

    constructor(uint256 listingDuration_, uint256 finishListingFeePercent_) {
        require(finishListingFeePercent_ <= 100, "FinishListingFeePercent: fee must be less or equal 100%");

        _listingDuration = listingDuration_;
        _finishListingFeePercent = finishListingFeePercent_;

        // address router = address(0x10ED43C718714eb63d5aA57B78B54704E256024E);
        address router = address(0xD99D1c33F9fC3444f8101754aBC46c52416550D1); // Test net
        uniswapV2Router = router;

        wbnbPair = LDex._createPair(router, LDex._wbnb);
        busdPair = LDex._createPair(router, LDex._busd);
    }

    function _startListing() private onlyOriginOwner {
        _listingStartAt = block.timestamp;
        _listingFeePercent = 100;

        // originOwner removed, once listing started
        _removeOriginOwner();
    }

    function _finishListing() private {
        _listingFinished = true;
    }

    function _updateListingFee() private {
        uint256 pastTime = block.timestamp - _listingStartAt;
        if (pastTime > _listingDuration) {
            _listingFeePercent = _finishListingFeePercent;
        } else {
            // pastTime == 0 => fee = 100
            // pastTime == _listingDuration => fee = _finishListingFee
            _listingFeePercent =
                (100 * (_listingDuration - pastTime)) /
                _listingDuration;
            
            if (_listingFeePercent < _finishListingFeePercent) {
                _listingFeePercent = _finishListingFeePercent;
            }
        }
    }

    function _updateAndGetListingFee(
        address sender_,
        address recipient_,
        uint256 amount_
    ) internal returns (uint256) {
        if (_listingStartAt == 0) {
            // first addLiquidity
            if (LDex._isPair(recipient_) && amount_ > 0) {
                _startListing();
            }
            return 0;
        } else {
            _updateListingFee();
            if (_listingStartAt + _listingDuration <= block.timestamp) {
                _finishListing();
            }

            if (!LDex._isPair(sender_) && !LDex._isPair(recipient_)) {
                // normal transfer
                return 0;
            } else {
                // swap
                return (amount_ * _listingFeePercent) / 100;
            }
        }
    }

    function listingDuration() public view returns (uint256) {
        return _listingDuration;
    }

    function listingFinished() public view returns (bool) {
        return _listingFinished;
    }
}
