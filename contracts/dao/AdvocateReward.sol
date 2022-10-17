// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/dao/IAdvocateReward.sol";
import "../interfaces/dao/IAdvocateRewardConfiguration.sol";
import "../interfaces/common/ITokenWallet.sol";


contract AdvocateReward is IAdvocateReward, Ownable {
    // State Variables
    address private _addressOfConfiguration;

    // Modifiers
    modifier validAddressOfConfiguration(address _address) {
        require(
            _address != address(0),
            "AdvocateReward: address of configuration must not be null"
        );
        require(
            _address != _addressOfConfiguration,
            "AdvocateReward: address of configuration existed"
        );
        _;
    }

    constructor(
        address owner,
        address addressOfConfiguration
    )
        validAddressOfConfiguration(addressOfConfiguration)
    {
        _addressOfConfiguration = addressOfConfiguration;
        transferOwnership(owner);
    }

    function setAddressOfConfiguration(
        address newAddress
    )
        external
        onlyOwner
        validAddressOfConfiguration(newAddress)
    {
        address _oldAddress = _addressOfConfiguration;
        _addressOfConfiguration = newAddress;

        emit SetAddressOfConfiguration(_oldAddress, _addressOfConfiguration);
    }

    function getAddressOfConfiguration() external override view returns (address) {
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

    function rewardAdvocatesQuarterly(
        address[] memory advocateAddresses,
        uint256[] memory rewardAmounts
    )
        external
        onlyOwner
    {
        require(
            advocateAddresses.length == rewardAmounts.length,
            "AdvocateReward: two arrays must have same length"
        );
        IAdvocateRewardConfiguration config = IAdvocateRewardConfiguration(_addressOfConfiguration);
        ITokenWallet tokenWallet = ITokenWallet(config.getTokenWalletAddress());

        for (uint256 i = 0; i < advocateAddresses.length; i++) {
            tokenWallet.transferFrom(
                config.getReserveAddressForQuarterReferralReward(),
                advocateAddresses[i],
                rewardAmounts[i],
                "Reserve For Advocate Quarterly"
            );
            emit RewardAdvocateQuarterly(
                advocateAddresses[i],
                rewardAmounts[i]
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

        uint256 rewardAmountForAdvocate =
            revenueMonthly * config.calculateAdvocateRewardPercent(numberOfReferrals) / 100;

        uint256 remainingReservedRevenueForAdvocateReward = revenueMonthly
            - reservedRevenueForCustomerReward
            - reservedRevenueForPlatformFee
            - reservedRevenueForCommunityCampaign
            - reservedRevenueForQuarterReferralReward
            - rewardAmountForAdvocate;

        emit RewardAdvocateMonthly(
            advocateAddress,
            revenueMonthly,
            numberOfReferrals,
            rewardAmountForAdvocate
        );

        ITokenWallet tokenWallet = ITokenWallet(config.getTokenWalletAddress());

        tokenWallet.deposit(
            config.getReserveAddressForCustomerReward(),
            reservedRevenueForCustomerReward,
            "Reserve For Customer Reward"
        );

        tokenWallet.deposit(
            config.getReserveAddressForPlatformFee(),
            reservedRevenueForPlatformFee,
            "Reserve For Platform Fee"
        );

        tokenWallet.deposit(
            config.getReserveAddressForCommunityCampaign(),
            reservedRevenueForCommunityCampaign,
            "Reserve For Community Campaign"
        );

        tokenWallet.deposit(
            config.getReserveAddressForQuarterReferralReward(),
            reservedRevenueForQuarterReferralReward,
            "Reserve For Quarter Referral Reward"
        );

        tokenWallet.deposit(
            config.getReserveAddressForAdvocateReward(),
            remainingReservedRevenueForAdvocateReward,
            "Reserve For Advocate Reward"
        );

        tokenWallet.deposit(
            advocateAddress,
            rewardAmountForAdvocate,
            "Reward For Advocate Monthly"
        );
    }
}
