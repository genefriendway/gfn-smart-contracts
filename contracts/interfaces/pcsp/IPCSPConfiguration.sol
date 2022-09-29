// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IPCSPConfiguration {
    // Events
    event SetGeneNFTAddress(address indexed geneNFTAddress);
    event SetTokenPCSPWalletAddress(address indexed tokenPCSPWalletAddress);
    event AddCustomerRewardPercent(
        uint256 riskOfGettingStroke,
        uint256 rewardPercent
    );

    event RemoveCustomerRewardPercent(
        uint256 riskOfGettingStroke
    );

    // Functions
    function setGeneNFTAddress(address geneNFTAddress) external;
    function getGeneNFTAddress() external view returns (address);
    function setTokenPCSPWalletAddress(address tokenPCSPWalletAddress) external;
    function getTokenPCSPWalletAddress() external view returns (address);

    function addCustomerRewardPercent(
        uint256 riskOfGettingStroke,
        uint256 rewardPercent
    ) external;
    function removeCustomerRewardPercent(uint256 riskOfGettingStroke) external;

    function getCustomerRewardPercent(
        uint256 riskOfGettingStroke
    ) external view returns (uint256);

    function calculateCustomerReward(
        uint256 riskOfGettingStroke,
        uint256 revenue
    ) external view returns (uint256);

    function checkActiveRiskOfGettingStroke(
        uint256 riskOfGettingStroke
    ) external view returns (bool);

}
