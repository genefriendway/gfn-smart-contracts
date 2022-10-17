// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IPCSPCustomerRewardConfiguration {
    // Events
    event SetGeneNFTAddress(address indexed geneNFTAddress);
    event SetTokenWalletAddress(address indexed tokenWalletAddress);
    event SetBudgetAddressToReward(address indexed budgetAddress);
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
    function setTokenWalletAddress(address tokenWalletAddress) external;
    function getTokenWalletAddress() external view returns (address);
    function setBudgetAddressToReward(address budgetAddress) external;
    function getBudgetAddressToReward() external view returns (address);

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
