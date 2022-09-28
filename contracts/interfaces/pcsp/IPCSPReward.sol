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
        address indexed geneNFTOwner,
        uint256 riskOfGettingStroke,
        uint256 revenueInPCSP,
        uint256 customerRewardInPCSP
    );

    // Functions
    function setPCSPConfiguration(
        address addressOfPCSPConfiguration
    ) external;
    function getPCSPConfiguration() external view returns (address);

    function getRiskOfGettingStroke(
        uint256 geneNFTTokenID
    )
    external view returns (uint256);

    function checkGeneNFTRewardStatus(
        uint256 geneNFTTokenID
    )
    external view returns (bool);

    function calculateRewardForMultipleCustomers(
        uint256[] memory geneNFTTokenIDs,
        uint256[] memory risksOfGettingStroke,
        uint256[] memory revenuesInPCSP
    ) external;

}
