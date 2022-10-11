// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IAdvocateReward {

    // Structs
    struct AdvocateStats {
        uint256 totalRevenueAllTime;
        uint256 totalRevenueMonthly;
        uint256 numberOfReferralAllTime;
        uint256 numberOfReferralMonthly;
        uint256 numberOfReferralQuarterly;
        bool isActive;
    }

    struct ReferralInfo {
        string paymentId;
        string serviceName;
        uint256 revenue;
    }

    // Events
    event SetAdvocateRewardConfiguration(
        address indexed oldConfiguration,
        address indexed newConfiguration
    );

    event RewardAdvocateMonthly(
        address indexed advocateAddress,
        uint256 totalRevenueMonthly,
        uint256 numberOfReferrals,
        uint256 revenueReward
    );

    // Functions
    function setAdvocateRewardConfiguration(address _address) external;
    function getAdvocateRewardConfiguration() external view returns (address);

    function rewardAdvocatesMonthly(
        address[] memory advocateAddresses,
        uint256[] memory revenuesMonthly,
        uint256[] memory referrals
    ) external;

}
