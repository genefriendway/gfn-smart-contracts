// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IPCSPCustomerReward {
    // Events
    event SetAddressOfConfiguration(
        address indexed oldAddress,
        address indexed newAddress
    );

    event RecordRiskOfGettingStroke(
        uint256 geneNFTTokenID,
        uint256 riskOfGettingStroke
    );

    event RewardForRiskOfGettingStroke(
        uint256 geneNFTTokenID,
        address indexed geneNFTOwner,
        uint256 riskOfGettingStroke,
        uint256 revenue,
        uint256 rewardAmount
    );

    // Functions
    function setAddressOfConfiguration(
        address addressOfConfiguration
    ) external;
    function getAddressOfConfiguration() external view returns (address);

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
        uint256[] memory revenues
    ) external;

}
