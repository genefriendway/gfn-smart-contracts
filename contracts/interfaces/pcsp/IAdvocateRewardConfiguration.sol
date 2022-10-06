// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "./IAdvocateEnum.sol";

interface IAdvocateRewardConfiguration is IAdvocateEnum{

    // Events
    event SetAddressTokenPCSPWallet(address indexed _address);

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

    event SetAdvocateRewardPercent(Level level, uint256 percent);

    // Functions
    function setAddressTokenPCSPWallet(address _address) external;
    function getAddressTokenPCSPWallet() external view returns (address);

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

    function calculateAdvocateLevel(uint256 numberOfReferral) external view returns (Level);

    function setAdvocateRewardPercent(Level level, uint256 percent) external;
    function getAdvocateRewardPercent(Level level) external view returns (uint256);
}
