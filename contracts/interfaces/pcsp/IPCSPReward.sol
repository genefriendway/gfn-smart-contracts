// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IPCSPReward {
    // Events
    event SetPCSPConfiguration(
        address indexed oldPCSPConfiguration,
        address indexed newPCSPConfiguration
    );

    event RecordRiskOfGettingStroke(
        uint256 geneNFTTokenID,
        uint256 riskOfGettingStroke
    );

    event RewardForRiskOfGettingStroke(
        uint256 geneNFTTokenID,
        address geneNFTOwner,
        uint256 riskOfGettingStroke,
        uint256 revenueInPCSP,
        uint256 customerRewardInPCSP
    );

    // Functions
    function setPCSPConfiguration(
        address addressOfPCSPConfiguration
    ) external;
    function getPCSPConfiguration() external view returns (address);

    function calculateCustomerReward(
        uint256 geneNFTTokenID,
        uint256 riskOfGettingStroke,
        uint256 revenueInPCSP
    ) external;

}
