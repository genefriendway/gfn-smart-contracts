// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;
import "../../interfaces/pcsp/IAdvocateEnum.sol";


interface IAdvocateReward is IAdvocateEnum {

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

    event RecordReferral(
        address indexed advocateAddress,
        string paymentId,
        string serviceName,
        uint256 revenue
    );

    event RewardAdvocateMonthly(
        address indexed advocateAddress,
        uint256 totalRevenueMonthly,
        Level level,
        uint256 revenueReward
    );

    // Functions
    function setAdvocateRewardConfiguration(address _address) external;
    function getAdvocateRewardConfiguration() external view returns (address);

    function recordReferral(
        address advocateAddress,
        string memory paymentId,
        string memory serviceName,
        uint256 revenue
    ) external;

    function rewardAdvocatesMonthly(address[] memory advocateAddresses) external;

}
