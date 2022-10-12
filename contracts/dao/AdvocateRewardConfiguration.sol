// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/dao/IAdvocateRewardConfiguration.sol";


contract AdvocateRewardConfiguration is IAdvocateRewardConfiguration, Ownable {

    uint256[] private _levelNumbers;
    // Map: Level Number => Detail Level
    mapping(uint256 => AdvocateLevel) private _advocateLevels;
    mapping(ReserveObject => uint256) _reservePercents;
    mapping(ReserveObject => address) _reserveAddresses;

    // State Variables
    address private _addressOfTokenWallet;

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

    function setAdvocateLevel(
        uint256 levelNumber,
        uint256 minReferral,
        uint256 maxReferral,
        uint256 rewardPercent,
        bool isActive
    )
        external onlyOwner
    {
        _setAdvocateLevel(
            levelNumber, minReferral, maxReferral, rewardPercent, isActive
        );
    }

    function setMinMaxReferralForAdvocateLevel(
        uint256 levelNumber,
        uint256 minReferral,
        uint256 maxReferral
    )
        external onlyOwner
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
        external onlyOwner
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

    function setStatusForAdvocateLevel(
        uint256 levelNumber,
        bool isActive
    )
        external onlyOwner
    {
        AdvocateLevel storage level = _advocateLevels[levelNumber];
        require(
            isActive != level.isActive,
            "AdvocateRewardConfiguration: status must differ from current value"
        );

        level.isActive = isActive;

        emit SetStatusForAdvocateLevel(levelNumber, isActive);
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
        for (uint256 i = 0; i < _levelNumbers.length; i++) {
            AdvocateLevel storage level = _advocateLevels[_levelNumbers[i]];
            if (level.isActive
                    && numberOfReferrals >= level.minReferral
                    && numberOfReferrals <= level.maxReferral) {
                return _levelNumbers[i];
            }
        }
        return 0; // default return zero
    }

    function calculateAdvocateRewardPercent(
        uint256 numberOfReferrals
    )
        external override view returns (uint256)
    {
        for (uint256 i = 0; i < _levelNumbers.length; i++) {
            AdvocateLevel storage level = _advocateLevels[_levelNumbers[i]];
            if (level.isActive
                    && numberOfReferrals >= level.minReferral
                    && numberOfReferrals <= level.maxReferral) {
                return level.rewardPercent;
            }
        }
        return 0; // default return zero reward percent
    }

    function _setDefaultAdvocateLevels() private {
        // Advocate Level start at 1
        _setAdvocateLevel(1, 1, 99, 20, true);
        _setAdvocateLevel(2, 100, 199, 30, true);
        _setAdvocateLevel(3, 200, 299, 40, true);
        _setAdvocateLevel(4, 300, 99999999, 50, true);
    }

    function _setDefaultReservePercents() private {
        _reservePercents[ReserveObject.CUSTOMER_REWARD] = 20;
        _reservePercents[ReserveObject.PLATFORM_FEE] = 15;
        _reservePercents[ReserveObject.COMMUNITY_CAMPAIGN] = 10;
        _reservePercents[ReserveObject.QUARTER_REFERRAL_REWARD] = 5;
        _reservePercents[ReserveObject.ADVOCATE_REWARD] = 50;
    }

    function _setAdvocateLevel(
        uint256 levelNumber,
        uint256 minReferral,
        uint256 maxReferral,
        uint256 rewardPercent,
        bool isActive
    )
        private
    {
        require(
            levelNumber > 0,
            "AdvocateRewardConfiguration: level number must be greater than zero"
        );

        require(
            rewardPercent > 0,
            "AdvocateRewardConfiguration: reward percent must be greater than zero"
        );

        // push list of level number
        _levelNumbers.push(levelNumber);

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
}
