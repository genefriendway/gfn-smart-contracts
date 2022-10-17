// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IAdvocateReward {

    // Events
    event SetAddressOfConfiguration(
        address indexed oldAddress,
        address indexed newAddress
    );

    event RewardAdvocateMonthly(
        address indexed advocateAddress,
        uint256 totalRevenue,
        uint256 numberOfReferrals,
        uint256 rewardAmount
    );
    event RewardAdvocateQuarterly(
        address indexed advocateAddress,
        uint256 rewardAmount
    );

    // Functions
    function setAddressOfConfiguration(address newAddress) external;
    function getAddressOfConfiguration() external view returns (address);

    function rewardAdvocatesMonthly(
        address[] memory advocateAddresses,
        uint256[] memory revenuesMonthly,
        uint256[] memory referrals
    ) external;

    function rewardAdvocatesQuarterly(
        address[] memory advocateAddresses,
        uint256[] memory rewardAmounts
    ) external;

}
