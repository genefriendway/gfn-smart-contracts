// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

interface IRevenueSharingArrangement {

    event MakeCollaborationBetweenGeneticProfileOwnerAndInvestor(
        address indexed geneticProfileOwner,
        address indexed investor,
        uint256 investedLIFE
    );

    event MakeRevenueSharingArrangement(
        address indexed geneticProfileOwner,
        uint256 gnftTokenId
    );

    function makeCollaborationBetweenGeneticProfileOwnerAndInvestor(
        address _geneticProfileOwner,
        address _investor,
        uint256 _investedNumberOfLIFE
    ) external;

    function distributeRevenue(
        uint256 _gnftTokenId,
        uint256 _revenue
    ) external;

    function queryTotalAccumulatedRevenue(
        uint256 _gnftTokenId
    ) external view returns (uint256);

    function queryTotalInvestedLIFEOfInvestors(
        address _originalGeneticProfileOwner
    ) external view returns (uint256);

    function queryTotalInvestedLIFEOfInvestors(
        uint256 _gnftTokenId
    ) external view returns (uint256);

    function queryInvestedLIFEOfInvestor(
        uint256 _gnftTokenId,
        address _investor
    ) external view returns (uint256);

    function queryInvestedLIFEOfInvestor(
        address _originalGeneticProfileOwner,
        address _investor
    ) external view returns (uint256);

}