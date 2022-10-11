// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/dao/IAdvocateReward.sol";
import "../interfaces/dao/IAdvocateRewardConfiguration.sol";
import "../interfaces/common/ITokenWallet.sol";


contract AdvocateReward is IAdvocateReward, Ownable {
    // State Variables
    address private _addressOfConfiguration;
    // Mapping: advocate address => Referral Stats
    mapping(address => AdvocateStats) private _advocateStats;


    // Modifiers
    modifier validAdvocateRewardConfiguration(address _address) {
        require(
            _address != address(0),
            "AdvocateReward: address of advocate reward configuration must not be null"
        );
        require(
            _address != _addressOfConfiguration,
            "AdvocateReward: address of advocate reward configuration existed"
        );
        _;
    }

    constructor(
        address owner,
        address addressOfConfiguration
    )
        validAdvocateRewardConfiguration(addressOfConfiguration)
    {
        _addressOfConfiguration = addressOfConfiguration;
        transferOwnership(owner);
    }

    function setAdvocateRewardConfiguration(
        address addressOfConfiguration
    )
        external
        onlyOwner
        validAdvocateRewardConfiguration(addressOfConfiguration)
    {
        address _oldConfiguration = _addressOfConfiguration;
        _addressOfConfiguration = addressOfConfiguration;

        emit SetAdvocateRewardConfiguration(
            _oldConfiguration, addressOfConfiguration
        );
    }

    function getAdvocateRewardConfiguration() external override view returns (address) {
        return _addressOfConfiguration;
    }

    function rewardAdvocatesMonthly(
        address[] memory advocateAddresses,
        uint256[] memory revenues,
        uint256[] memory referrals
    )
        external
        onlyOwner
    {
        for (uint256 i = 0; i < advocateAddresses.length; i++) {
            _distributeRevenue(
                advocateAddresses[i], revenues[i], referrals[i]
            );
        }
    }

    function _distributeRevenue(
        address advocateAddress,
        uint256 revenueMonthly,
        uint256 numberOfReferrals
    )
        private
    {
        IAdvocateRewardConfiguration config = IAdvocateRewardConfiguration(_addressOfConfiguration);

        uint256 reservedRevenueForCustomerReward =
            revenueMonthly * config.getReservePercentForCustomerReward() / 100;

        uint256 reservedRevenueForPlatformFee =
            revenueMonthly * config.getReservePercentForPlatformFee() / 100;

        uint256 reservedRevenueForCommunityCampaign =
            revenueMonthly * config.getReservePercentForCommunityCampaign() / 100;

        uint256 reservedRevenueForQuarterReferralReward =
            revenueMonthly * config.getReservePercentForQuarterReferralReward() / 100;

        uint256 revenueRewardBelongToAdvocate =
            revenueMonthly * config.getAdvocateRewardPercent(numberOfReferrals) / 100;

        uint256 remainingReservedRevenueForAdvocateReward = revenueMonthly
            - reservedRevenueForCustomerReward
            - reservedRevenueForPlatformFee
            - reservedRevenueForCommunityCampaign
            - reservedRevenueForQuarterReferralReward
            - revenueRewardBelongToAdvocate;

        emit RewardAdvocateMonthly(
            advocateAddress,
            revenueMonthly,
            numberOfReferrals,
            revenueRewardBelongToAdvocate
        );

        ITokenWallet tokenWallet = ITokenWallet(config.getAddressTokenWallet());

        tokenWallet.increaseBalance(
            config.getReserveAddressForCustomerReward(),
            reservedRevenueForCustomerReward,
            "Reserve For Customer Reward"
        );

        tokenWallet.increaseBalance(
            config.getReserveAddressForPlatformFee(),
            reservedRevenueForPlatformFee,
            "Reserve For Platform Fee"
        );

        tokenWallet.increaseBalance(
            config.getReserveAddressForCommunityCampaign(),
            reservedRevenueForCommunityCampaign,
            "Reserve For Community Campaign"
        );

        tokenWallet.increaseBalance(
            config.getReserveAddressForQuarterReferralReward(),
            reservedRevenueForQuarterReferralReward,
            "Reserve For Quarter Referral Reward"
        );

        tokenWallet.increaseBalance(
            config.getReserveAddressForAdvocateReward(),
            remainingReservedRevenueForAdvocateReward,
            "Reserve For Advocate Reward"
        );

        tokenWallet.increaseBalance(
            advocateAddress,
            revenueRewardBelongToAdvocate,
            "Reserve For Advocate Reward"
        );
    }
}
