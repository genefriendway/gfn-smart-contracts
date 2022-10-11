// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IAdvocateRewardConfiguration{

    enum ReserveObject {
        CUSTOMER_REWARD,
        PLATFORM_FEE,
        COMMUNITY_CAMPAIGN,
        QUARTER_REFERRAL_REWARD,
        ADVOCATE_REWARD
    }

    struct AdvocateLevel {
        uint256 minReferral;
        uint256 maxReferral;
        uint256 rewardPercent;
        bool isActive;
    }

    // Events
    event SetAddressTokenWallet(address indexed _address);

    event SetAdvocateLevel(
        uint256 levelNumber,
        uint256 minReferral,
        uint256 maxReferral,
        uint256 rewardPercent,
        bool isActive
    );

    event SetReserveAddressForCustomerReward(address indexed _address);
    event SetReservePercentForCustomerReward(uint256 percent);

    event SetReserveAddressForPlatformFee(address indexed _address);
    event SetReservePercentForPlatformFee(uint256 percent);

    event SetReserveAddressForCommunityCampaign(address indexed _address);
    event SetReservePercentForCommunityCampaign(uint256 percent);

    event SetReserveAddressForQuarterReferralReward(address indexed _address);
    event SetReservePercentForQuarterReferralReward(uint256 percent);

    event SetReserveAddressForAdvocateReward(address indexed _address);
    event SetReservePercentForAdvocateReward(uint256 percent);

//    event SetAdvocateRewardPercent(uint256 level, uint256 percent);

    // Functions
    function setAddressTokenWallet(address _address) external;
    function getAddressTokenWallet() external view returns (address);

    function setReserveAddressForCustomerReward(address _address) external;
    function getReserveAddressForCustomerReward() external view returns (address);
    function setReservePercentForCustomerReward(uint256 percent) external;
    function getReservePercentForCustomerReward() external view returns (uint256);

    function setReserveAddressForPlatformFee(address _address) external;
    function getReserveAddressForPlatformFee() external view returns (address);
    function setReservePercentForPlatformFee(uint256 percent) external;
    function getReservePercentForPlatformFee() external view returns (uint256);

    function setReserveAddressForCommunityCampaign(address _address) external;
    function getReserveAddressForCommunityCampaign() external view returns (address);
    function setReservePercentForCommunityCampaign(uint256 percent) external;
    function getReservePercentForCommunityCampaign() external view returns (uint256);

    function setReserveAddressForQuarterReferralReward(address _address) external;
    function getReserveAddressForQuarterReferralReward() external view returns (address);
    function setReservePercentForQuarterReferralReward(uint256 percent) external;
    function getReservePercentForQuarterReferralReward() external view returns (uint256);

    function setReserveAddressForAdvocateReward(address _address) external;
    function getReserveAddressForAdvocateReward() external view returns (address);
    function setReservePercentForAdvocateReward(uint256 percent) external;
    function getReservePercentForAdvocateReward() external view returns (uint256);

    function setAdvocateLevel(
        uint256 levelNumber,
        uint256 minReferral,
        uint256 maxReferral,
        uint256 rewardPercent,
        bool isActive
    ) external;

    function getAdvocateLevelNumber(uint256 numberOfReferrals) external view returns (uint256);
    function getAdvocateRewardPercent(uint256 numberOfReferrals) external view returns (uint256);
}
