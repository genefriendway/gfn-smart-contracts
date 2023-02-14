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
            config.calculateReservedRevenueForCustomerReward(revenueMonthly);

        uint256 reservedRevenueForPlatformFee =
            config.calculateReserveRevenueForPlatformFee(revenueMonthly);

        uint256 reservedRevenueForCommunityCampaign =
            config.calculateReserveRevenueForCommunityCampaign(revenueMonthly);

        uint256 reservedRevenueForQuarterReferralReward =
            config.calculateReserveRevenueForQuarterReferralReward(revenueMonthly);

        uint256 rewardAmountForAdvocate =
            config.calculateRewardAmountForAdvocate(revenueMonthly, numberOfReferrals);

        uint256 remainingReservedRevenueForAdvocateReward = revenueMonthly
            - reservedRevenueForCustomerReward
            - reservedRevenueForPlatformFee
            - reservedRevenueForCommunityCampaign
            - reservedRevenueForQuarterReferralReward
            - rewardAmountForAdvocate;

        emit DistributeRevenue(
            revenueMonthly,
            reservedRevenueForCustomerReward,
            reservedRevenueForPlatformFee,
            reservedRevenueForCommunityCampaign,
            reservedRevenueForQuarterReferralReward,
            rewardAmountForAdvocate,
            remainingReservedRevenueForAdvocateReward
        );

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
