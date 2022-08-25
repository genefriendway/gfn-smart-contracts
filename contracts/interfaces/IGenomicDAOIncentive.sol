// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IGenomicDAOIncentive {
    // Events
    event SetIncentiveConfiguration(
        address indexed oldIncentiveConfiguration,
        address indexed newIncentiveConfiguration
    );

    event RecordRiskOfGettingStroke(
        uint256 geneNFTTokenID,
        address indexed geneNFTOwner,
        uint256 riskOfGettingStroke
    );

    // Functions
    function setIncentiveConfiguration(
        address incentiveConfiguration
    ) external;

    function calculateCustomerReward(
        uint256 geneNFTTokenID,
        uint256 riskOfGettingStroke,
        uint256 originalTokenValue
    ) external;

}
