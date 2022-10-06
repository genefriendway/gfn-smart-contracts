// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../../interfaces/pcsp/IAdvocateRewardConfiguration.sol";


contract AdvocateRewardConfiguration is IAdvocateRewardConfiguration, Ownable {

    // Map: AdvocateLevel => Reward Percent
    mapping(Level => uint) _advocateRewardPercents;
    mapping(ReserveObject => uint256) _reservePercents;
    mapping(ReserveObject => address) _reserveAddresses;

    // State Variables
    address private _addressTokenPCSPWallet;

    constructor(address owner)
    {
        transferOwnership(owner);
        _setDefaultAdvocateRewardPercents();
        _setDefaultReservePercents();
    }

    function setAddressTokenPCSPWallet(
        address _address
    )
        external onlyOwner
    {
        _addressTokenPCSPWallet = _address;
        emit SetAddressTokenPCSPWallet(_address);
    }

    function getAddressTokenPCSPWallet() external override view returns (address) {
        return _addressTokenPCSPWallet;
    }

    // functions for Customer Reward
    function setReserveAddressForCustomerReward(
        address _address
    )
        external onlyOwner
    {
        _reserveAddresses[ReserveObject.CUSTOMER_REWARD] = _address;
        emit SetReserveAddressForCustomerReward(_address);
    }

    function getReserveAddressForCustomerReward() external override view returns (address) {
        return _reserveAddresses[ReserveObject.CUSTOMER_REWARD];
    }

    function setReservePercentForCustomerReward(
        uint256 percent
    )
        external onlyOwner
    {
        _reservePercents[ReserveObject.CUSTOMER_REWARD] = percent;
        emit SetReservePercentForCustomerReward(percent);
    }

    function getReservePercentForCustomerReward() external override view returns (uint256) {
        return _reservePercents[ReserveObject.CUSTOMER_REWARD];
    }

    // functions for Platform Fee
    function setReserveAddressForPlatformFee(
        address _address
    )
        external onlyOwner
    {
        _reserveAddresses[ReserveObject.PLATFORM_FEE] = _address;
        emit SetReserveAddressForPlatformFee(_address);
    }

    function getReserveAddressForPlatformFee() external override view returns (address) {
        return _reserveAddresses[ReserveObject.PLATFORM_FEE];
    }

    function setReservePercentForPlatformFee(
        uint256 percent
    )
        external onlyOwner
    {
        _reservePercents[ReserveObject.PLATFORM_FEE] = percent;
        emit SetReservePercentForPlatformFee(percent);
    }

    function getReservePercentForPlatformFee() external override view returns (uint256) {
        return _reservePercents[ReserveObject.PLATFORM_FEE];
    }

    // functions for Community Campaign
    function setReserveAddressForCommunityCampaign(
        address _address
    )
        external onlyOwner
    {
        _reserveAddresses[ReserveObject.COMMUNITY_CAMPAIGN] = _address;
        emit SetReserveAddressForCommunityCampaign(_address);
    }

    function getReserveAddressForCommunityCampaign() external override view returns (address) {
        return _reserveAddresses[ReserveObject.COMMUNITY_CAMPAIGN];
    }

    function setReservePercentForCommunityCampaign(
        uint256 percent
    )
        external onlyOwner
    {
        _reservePercents[ReserveObject.COMMUNITY_CAMPAIGN] = percent;
        emit SetReservePercentForCommunityCampaign(percent);
    }

    function getReservePercentForCommunityCampaign() external override view returns (uint256) {
        return _reservePercents[ReserveObject.COMMUNITY_CAMPAIGN];
    }

    // functions for Quarter Referral Reward
    function setReserveAddressForQuarterReferralReward(
        address _address
    )
        external onlyOwner
    {
        _reserveAddresses[ReserveObject.QUARTER_REFERRAL_REWARD] = _address;
        emit SetReserveAddressForQuarterReferralReward(_address);
    }

    function getReserveAddressForQuarterReferralReward() external override view returns (address) {
        return _reserveAddresses[ReserveObject.QUARTER_REFERRAL_REWARD];
    }

    function setReservePercentForQuarterReferralReward(
        uint256 percent
    )
        external onlyOwner
    {
        _reservePercents[ReserveObject.QUARTER_REFERRAL_REWARD] = percent;
        emit SetReservePercentForCommunityCampaign(percent);
    }

    function getReservePercentForQuarterReferralReward() external override view returns (uint256) {
        return _reservePercents[ReserveObject.QUARTER_REFERRAL_REWARD];
    }

    // functions for Advocate Reward
    function setReserveAddressForAdvocateReward(
        address _address
    )
        external onlyOwner
    {
        _reserveAddresses[ReserveObject.ADVOCATE_REWARD] = _address;
        emit SetReserveAddressForAdvocateReward(_address);
    }

    function getReserveAddressForAdvocateReward() external override view returns (address) {
        return _reserveAddresses[ReserveObject.ADVOCATE_REWARD];
    }

    function setReservePercentForAdvocateReward(
        uint256 percent
    )
        external onlyOwner
    {
        _reservePercents[ReserveObject.ADVOCATE_REWARD] = percent;
        emit SetReservePercentForAdvocateReward(percent);
    }

    function getReservePercentForAdvocateReward() external override view returns (uint256) {
        return _reservePercents[ReserveObject.QUARTER_REFERRAL_REWARD];
    }

    function calculateAdvocateLevel(
        uint256 numberOfReferral
    )
        external override view returns (Level)
    {
        if (numberOfReferral < 100) {
            return Level.SILVER;
        } else if (numberOfReferral < 200 ) {
            return Level.GOLD;
        } else if (numberOfReferral < 300 ) {
            return Level.PLATINUM;
        } else {
            return Level.GOLD;
        }
    }

    function setAdvocateRewardPercent(
        Level level, uint256 percent
    )
        external onlyOwner
    {
        _advocateRewardPercents[level] = percent;
        emit SetAdvocateRewardPercent(level, percent);
    }

     function getAdvocateRewardPercent(
        Level level
    )
        external override view returns (uint256)
    {
        return _advocateRewardPercents[level];
    }

    function _setDefaultAdvocateRewardPercents() private {
        _advocateRewardPercents[Level.SILVER] = 20;
        _advocateRewardPercents[Level.GOLD] = 30;
        _advocateRewardPercents[Level.PLATINUM] = 40;
        _advocateRewardPercents[Level.DIAMOND] = 50;
    }

    function _setDefaultReservePercents() private {
        _reservePercents[ReserveObject.CUSTOMER_REWARD] = 20;
        _reservePercents[ReserveObject.PLATFORM_FEE] = 15;
        _reservePercents[ReserveObject.COMMUNITY_CAMPAIGN] = 10;
        _reservePercents[ReserveObject.QUARTER_REFERRAL_REWARD] = 5;
        _reservePercents[ReserveObject.CUSTOMER_REWARD] = 50;
    }
}
