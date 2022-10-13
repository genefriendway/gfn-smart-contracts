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
        bool isExisted;
        bool isActive;
    }

    // Events
    event SetTokenWalletAddress(address indexed tokenWalletAddress);

    event AddAdvocateLevel(
        uint256 levelNumber,
        uint256 minReferral,
        uint256 maxReferral,
        uint256 rewardPercent,
        bool isActive
    );

    event SetAdvocateLevel(
        uint256 levelNumber,
        uint256 minReferral,
        uint256 maxReferral,
        uint256 rewardPercent,
        bool isActive
    );
    event SetMinMaxReferralForAdvocateLevel(
        uint256 levelNumber,
        uint256 minReferral,
        uint256 maxReferral
    );
    event SetRewardPercentForAdvocateLevel(
        uint256 levelNumber,
        uint256 rewardPercent
    );
    event SetAdvocateLevelStatus(
        uint256 levelNumber,
        bool isActive
    );

    event SetReserveAddressForCustomerReward(address indexed reserveAddress);
    event SetReservePercentForCustomerReward(uint256 percent);

    event SetReserveAddressForPlatformFee(address indexed reserveAddress);
    event SetReservePercentForPlatformFee(uint256 percent);

    event SetReserveAddressForCommunityCampaign(address indexed reserveAddress);
    event SetReservePercentForCommunityCampaign(uint256 percent);

    event SetReserveAddressForQuarterReferralReward(address indexed reserveAddress);
    event SetReservePercentForQuarterReferralReward(uint256 percent);

    event SetReserveAddressForAdvocateReward(address indexed reserveAddress);
    event SetReservePercentForAdvocateReward(uint256 percent);

    // Functions
    function setTokenWalletAddress(address tokenWalletAddress) external;
    function getTokenWalletAddress() external view returns (address);

    function setReserveAddressForCustomerReward(address reserveAddress) external;
    function getReserveAddressForCustomerReward() external view returns (address);
    function setReservePercentForCustomerReward(uint256 percent) external;
    function getReservePercentForCustomerReward() external view returns (uint256);

    function setReserveAddressForPlatformFee(address reserveAddress) external;
    function getReserveAddressForPlatformFee() external view returns (address);
    function setReservePercentForPlatformFee(uint256 percent) external;
    function getReservePercentForPlatformFee() external view returns (uint256);

    function setReserveAddressForCommunityCampaign(address reserveAddress) external;
    function getReserveAddressForCommunityCampaign() external view returns (address);
    function setReservePercentForCommunityCampaign(uint256 percent) external;
    function getReservePercentForCommunityCampaign() external view returns (uint256);

    function setReserveAddressForQuarterReferralReward(address reserveAddress) external;
    function getReserveAddressForQuarterReferralReward() external view returns (address);
    function setReservePercentForQuarterReferralReward(uint256 percent) external;
    function getReservePercentForQuarterReferralReward() external view returns (uint256);

    function setReserveAddressForAdvocateReward(address reserveAddress) external;
    function getReserveAddressForAdvocateReward() external view returns (address);
    function setReservePercentForAdvocateReward(uint256 percent) external;
    function getReservePercentForAdvocateReward() external view returns (uint256);

    function addAdvocateLevel(
        uint256 minReferral,
        uint256 maxReferral,
        uint256 rewardPercent,
        bool isActive
    ) external;

    function setAdvocateLevel(
        uint256 levelNumber,
        uint256 minReferral,
        uint256 maxReferral,
        uint256 rewardPercent,
        bool isActive
    ) external;

    function setMinMaxReferralForAdvocateLevel(
        uint256 levelNumber,
        uint256 minReferral,
        uint256 maxReferral
    ) external;

    function setRewardPercentForAdvocateLevel(
        uint256 levelNumber,
        uint256 rewardPercent
    ) external;

    function setAdvocateLevelStatus(
        uint256 levelNumber,
        bool isActive
    ) external;

    function getAdvocateMinReferral(uint256 levelNumber) external view returns (uint256);
    function getAdvocateMaxReferral(uint256 levelNumber) external view returns (uint256);
    function getAdvocateRewardPercent(uint256 levelNumber) external view returns (uint256);
    function getAdvocateLevelStatus(uint256 levelNumber) external view returns (bool);

    function calculateAdvocateLevelNumber(uint256 numberOfReferrals) external view returns (uint256);
    function calculateAdvocateRewardPercent(uint256 numberOfReferrals) external view returns (uint256);

    function getLevelCount() external view returns (uint256);
}
