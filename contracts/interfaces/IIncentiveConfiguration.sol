// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IIncentiveConfiguration {
    // Events
    event SetGeneNFTAddress(address indexed geneNFTAddress);
    event UpdateCustomerRewardRatio(
        uint256 riskOfGettingStroke,
        uint256 percentageOfReward
    );

    // Functions
    function setDefaultCustomerRewardRatios() private;
    function updateCustomerRewardRatio(
        uint256 riskOfGettingStroke,
        uint256 percentageOfReward
    ) external;
    function getCustomerRewardPercentage(
        uint256 riskOfGettingStroke
    ) external view returns (uint256);

    function setGeneNFTAddress(address geneNFTAddress) external;
    function getGeneNFTAddress() external view returns (address);

}
