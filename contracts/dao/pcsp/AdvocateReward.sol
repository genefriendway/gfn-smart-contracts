// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../../interfaces/pcsp/IAdvocateReward.sol";
import "../../interfaces/pcsp/IAdvocateRewardConfiguration.sol";
import "../../interfaces/common/ITokenWallet.sol";


contract AdvocateReward is IAdvocateReward, Ownable {
    // State Variables
    address private _addressOfConfiguration;
    // Mapping: advocate address => Referral Stats
    mapping(address => AdvocateStats) private _advocateStats;


    // Modifiers
    modifier validAdvocateRewardConfiguration(address _address) {
        require(
            _address != address(0),
            "PCSPReward: address of advocate reward configuration must not be null"
        );
        require(
            _address != _addressOfConfiguration,
            "PCSPReward: address of advocate reward configuration existed"
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

    function recordReferral(
        address advocateAddress,
        string memory paymentId,
        string memory serviceName,
        uint256 revenue
    )
        external
        onlyOwner
    {

        AdvocateStats storage stats = _advocateStats[advocateAddress];
        stats.totalRevenueAllTime += revenue;
        stats.totalRevenueMonthly += revenue;
        stats.numberOfReferralAllTime += 1;
        stats.numberOfReferralMonthly += 1;
        stats.numberOfReferralQuarterly += 1;

        emit RecordReferral(
            advocateAddress,
            paymentId,
            serviceName,
            revenue
        );

        _distributeRevenue(revenue);
    }

    function rewardAdvocatesMonthly(
        address[] memory advocateAddresses
    )
        external
        onlyOwner
    {
        for (uint256 i = 0; i < advocateAddresses.length; i++) {
            _rewardAdvocateMonthly(advocateAddresses[i]);
        }
    }

    function _distributeRevenue(uint256 revenue) private {
        IAdvocateRewardConfiguration config = IAdvocateRewardConfiguration(_addressOfConfiguration);

        uint256 reserveRevenueForCustomerReward = revenue * config.getReservePercentForCustomerReward() / 100;
        uint256 reserveRevenueForPlatformFee = revenue * config.getReservePercentForPlatformFee() / 100;
        uint256 reserveRevenueForCommunityCampaign = revenue * config.getReservePercentForCommunityCampaign() / 100;
        uint256 reserveRevenueForQuarterReferralReward = revenue * config.getReservePercentForQuarterReferralReward() / 100;
        uint256 reserveRevenueForAdvocateReward = revenue
            - reserveRevenueForCustomerReward
            - reserveRevenueForPlatformFee
            - reserveRevenueForCommunityCampaign
            - reserveRevenueForQuarterReferralReward;

        ITokenWallet tokenWallet = ITokenWallet(config.getAddressTokenPCSPWallet());

        tokenWallet.increaseBalance(
            config.getReserveAddressForCustomerReward(),
            reserveRevenueForCustomerReward,
            "Reserve For Customer Reward"
        );

        tokenWallet.increaseBalance(
            config.getReserveAddressForPlatformFee(),
            reserveRevenueForPlatformFee,
            "Reserve For Platform Fee"
        );

        tokenWallet.increaseBalance(
            config.getReserveAddressForCommunityCampaign(),
            reserveRevenueForCommunityCampaign,
            "Reserve For Community Campaign"
        );

        tokenWallet.increaseBalance(
            config.getReserveAddressForQuarterReferralReward(),
            reserveRevenueForQuarterReferralReward,
            "Reserve For Quarter Referral Reward"
        );

        tokenWallet.increaseBalance(
            config.getReserveAddressForAdvocateReward(),
            reserveRevenueForAdvocateReward,
            "Reserve For Advocate Reward"
        );
    }

    function _rewardAdvocateMonthly(address advocateAddress) private {
        AdvocateStats storage stats = _advocateStats[advocateAddress];

        IAdvocateRewardConfiguration config = IAdvocateRewardConfiguration(_addressOfConfiguration);
        Level level = config.calculateAdvocateLevel(stats.numberOfReferralMonthly);
        uint256 revenueReward = stats.totalRevenueMonthly * config.getAdvocateRewardPercent(level) / 100;

        emit RewardAdvocateMonthly(
            advocateAddress,
            stats.totalRevenueMonthly,
            level,
            revenueReward
        );

        // reset stats for next month
        stats.totalRevenueMonthly = 0;
        stats.numberOfReferralMonthly = 0;

    }
}
