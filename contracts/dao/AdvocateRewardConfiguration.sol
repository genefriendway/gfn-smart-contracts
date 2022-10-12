// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/dao/IAdvocateRewardConfiguration.sol";


contract AdvocateRewardConfiguration is IAdvocateRewardConfiguration, Ownable {

    // State Variables
    address private _addressOfTokenWallet;
    uint256 private _levelCount;
    // Map: Level Number => Detail Level
    mapping(uint256 => AdvocateLevel) private _advocateLevels;
    mapping(ReserveObject => uint256) _reservePercents;
    mapping(ReserveObject => address) _reserveAddresses;

    // Modifiers
    modifier existedLevelNumber(uint256 levelNumber) {
        require(
            _advocateLevels[levelNumber].isExisted,
            "AdvocateRewardConfiguration: level number must be existed"
        );
        _;
    }

    constructor(address owner)
    {
        transferOwnership(owner);
        _setDefaultAdvocateLevels();
        _setDefaultReservePercents();
    }
    // Token Wallet Address
    function setTokenWalletAddress(
        address tokenWalletAddress
    )
        external onlyOwner
    {
        _addressOfTokenWallet = tokenWalletAddress;
        emit SetTokenWalletAddress(_addressOfTokenWallet);
    }

    function getTokenWalletAddress() external override view returns (address) {
        return _addressOfTokenWallet;
    }

    // functions for Customer Reward
    function setReserveAddressForCustomerReward(
        address reserveAddress
    )
        external onlyOwner
    {
        require(
            reserveAddress != address(0),
            "AdvocateRewardConfiguration: reserve address must not be null"
        );
        require(
            reserveAddress != _reserveAddresses[ReserveObject.CUSTOMER_REWARD],
            "AdvocateRewardConfiguration: reserve address existed"
        );

        _reserveAddresses[ReserveObject.CUSTOMER_REWARD] = reserveAddress;
        emit SetReserveAddressForCustomerReward(reserveAddress);
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
        address reserveAddress
    )
        external onlyOwner
    {
        require(
            reserveAddress != address(0),
            "AdvocateRewardConfiguration: reserve address must not be null"
        );
        require(
            reserveAddress != _reserveAddresses[ReserveObject.PLATFORM_FEE],
            "AdvocateRewardConfiguration: reserve address existed"
        );

        _reserveAddresses[ReserveObject.PLATFORM_FEE] = reserveAddress;
        emit SetReserveAddressForPlatformFee(reserveAddress);
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
        address reserveAddress
    )
        external onlyOwner
    {
        require(
            reserveAddress != address(0),
            "AdvocateRewardConfiguration: reserve address must not be null"
        );
        require(
            reserveAddress != _reserveAddresses[ReserveObject.COMMUNITY_CAMPAIGN],
            "AdvocateRewardConfiguration: reserve address existed"
        );

        _reserveAddresses[ReserveObject.COMMUNITY_CAMPAIGN] = reserveAddress;
        emit SetReserveAddressForCommunityCampaign(reserveAddress);
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
        address reserveAddress
    )
        external onlyOwner
    {
        require(
            reserveAddress != address(0),
            "AdvocateRewardConfiguration: reserve address must not be null"
        );
        require(
            reserveAddress != _reserveAddresses[ReserveObject.QUARTER_REFERRAL_REWARD],
            "AdvocateRewardConfiguration: reserve address existed"
        );

        _reserveAddresses[ReserveObject.QUARTER_REFERRAL_REWARD] = reserveAddress;
        emit SetReserveAddressForQuarterReferralReward(reserveAddress);
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
        emit SetReservePercentForQuarterReferralReward(percent);
    }

    function getReservePercentForQuarterReferralReward() external override view returns (uint256) {
        return _reservePercents[ReserveObject.QUARTER_REFERRAL_REWARD];
    }

    // functions for Advocate Reward
    function setReserveAddressForAdvocateReward(
        address reserveAddress
    )
        external onlyOwner
    {
        require(
            reserveAddress != address(0),
            "AdvocateRewardConfiguration: reserve address must not be null"
        );
        require(
            reserveAddress != _reserveAddresses[ReserveObject.ADVOCATE_REWARD],
            "AdvocateRewardConfiguration: reserve address existed"
        );

        _reserveAddresses[ReserveObject.ADVOCATE_REWARD] = reserveAddress;
        emit SetReserveAddressForAdvocateReward(reserveAddress);
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
        return _reservePercents[ReserveObject.ADVOCATE_REWARD];
    }

    function addAdvocateLevel(
        uint256 minReferral,
        uint256 maxReferral,
        uint256 rewardPercent,
        bool isActive
    )
        external onlyOwner
    {
        _addAdvocateLevel(minReferral, maxReferral, rewardPercent, isActive);
    }

    function setAdvocateLevel(
        uint256 levelNumber,
        uint256 minReferral,
        uint256 maxReferral,
        uint256 rewardPercent,
        bool isActive
    )
        external onlyOwner existedLevelNumber(levelNumber)
    {
        require(
            levelNumber > 0,
            "AdvocateRewardConfiguration: level number must be greater than zero"
        );

        require(
            rewardPercent > 0,
            "AdvocateRewardConfiguration: reward percent must be greater than zero"
        );

        // set detail Level Info
        AdvocateLevel storage level = _advocateLevels[levelNumber];
        level.minReferral = minReferral;
        level.maxReferral = maxReferral;
        level.rewardPercent = rewardPercent;
        level.isActive = isActive;

        emit SetAdvocateLevel(
            levelNumber, minReferral, maxReferral, rewardPercent, isActive
        );
    }

    function setMinMaxReferralForAdvocateLevel(
        uint256 levelNumber,
        uint256 minReferral,
        uint256 maxReferral
    )
        external onlyOwner existedLevelNumber(levelNumber)
    {
        require(
            minReferral < maxReferral,
            "AdvocateRewardConfiguration: min referral must be less than max referral"
        );

        AdvocateLevel storage level = _advocateLevels[levelNumber];
        require(
            minReferral != level.minReferral || maxReferral != level.maxReferral,
            "AdvocateRewardConfiguration: min or max referral must differ from current value"
        );

        level.minReferral = minReferral;
        level.maxReferral = maxReferral;

        emit SetMinMaxReferralForAdvocateLevel(
            levelNumber, minReferral, maxReferral
        );
    }

    function setRewardPercentForAdvocateLevel(
        uint256 levelNumber,
        uint256 rewardPercent
    )
        external onlyOwner existedLevelNumber(levelNumber)
    {
        require(
            rewardPercent > 0,
            "AdvocateRewardConfiguration: reward percent must be greater than zero"
        );

        AdvocateLevel storage level = _advocateLevels[levelNumber];
        require(
            rewardPercent != level.rewardPercent,
            "AdvocateRewardConfiguration: reward percent must differ from current value"
        );

        level.rewardPercent = rewardPercent;

        emit SetRewardPercentForAdvocateLevel(levelNumber, rewardPercent);
    }

    function setAdvocateLevelStatus(
        uint256 levelNumber,
        bool isActive
    )
        external onlyOwner existedLevelNumber(levelNumber)
    {
        AdvocateLevel storage level = _advocateLevels[levelNumber];
        require(
            isActive != level.isActive,
            "AdvocateRewardConfiguration: status must differ from current value"
        );

        level.isActive = isActive;

        emit SetAdvocateLevelStatus(levelNumber, isActive);
    }

    function getAdvocateMinReferral(
        uint256 levelNumber
    )
        external override view returns (uint256)
    {
        return _advocateLevels[levelNumber].minReferral;
    }

    function getAdvocateMaxReferral(
        uint256 levelNumber
    )
        external override view returns (uint256)
    {
        return _advocateLevels[levelNumber].maxReferral;
    }

    function getAdvocateRewardPercent(
        uint256 levelNumber
    )
        external override view returns (uint256)
    {
        return _advocateLevels[levelNumber].rewardPercent;
    }

    function getAdvocateLevelStatus(
        uint256 levelNumber
    )
        external override view returns (bool)
    {
        return _advocateLevels[levelNumber].isActive;
    }

    function calculateAdvocateLevelNumber(
        uint256 numberOfReferrals
    )
        external override view returns (uint256)
    {
        for (uint256 i = 1; i <= _levelCount; i++) {
            AdvocateLevel storage level = _advocateLevels[i];
            if (level.isActive
                    && numberOfReferrals >= level.minReferral
                    && numberOfReferrals <= level.maxReferral) {
                return i;
            }
        }
        return 0; // default return zero
    }

    function calculateAdvocateRewardPercent(
        uint256 numberOfReferrals
    )
        external override view returns (uint256)
    {
        for (uint256 i = 1; i <= _levelCount; i++) {
            AdvocateLevel storage level = _advocateLevels[i];
            if (level.isActive
                    && numberOfReferrals >= level.minReferral
                    && numberOfReferrals <= level.maxReferral) {
                return level.rewardPercent;
            }
        }
        return 0; // default return zero reward percent
    }

    function _setDefaultAdvocateLevels() private {
        // level 1
        _addAdvocateLevel(1, 99, 20, true);
        // level 2
        _addAdvocateLevel(100, 199, 30, true);
        // level 3
        _addAdvocateLevel(200, 299, 40, true);
        // level 4
        _addAdvocateLevel(300, 99999999, 50, true);
    }

    function _setDefaultReservePercents() private {
        _reservePercents[ReserveObject.CUSTOMER_REWARD] = 20;
        _reservePercents[ReserveObject.PLATFORM_FEE] = 15;
        _reservePercents[ReserveObject.COMMUNITY_CAMPAIGN] = 10;
        _reservePercents[ReserveObject.QUARTER_REFERRAL_REWARD] = 5;
        _reservePercents[ReserveObject.ADVOCATE_REWARD] = 50;
    }

    function _addAdvocateLevel(
        uint256 minReferral,
        uint256 maxReferral,
        uint256 rewardPercent,
        bool isActive
    )
        private
    {
        require(
            rewardPercent > 0,
            "AdvocateRewardConfiguration: reward percent must be greater than zero"
        );

        // Generate new next level by increase one
        _levelCount += 1;

        // set detail Level Info
        AdvocateLevel storage level = _advocateLevels[_levelCount];
        level.minReferral = minReferral;
        level.maxReferral = maxReferral;
        level.rewardPercent = rewardPercent;
        level.isActive = isActive;

        emit AddAdvocateLevel(
            _levelCount, minReferral, maxReferral, rewardPercent, isActive
        );
    }
}
