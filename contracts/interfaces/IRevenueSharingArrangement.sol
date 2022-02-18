// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

interface IRevenueSharingArrangement {

    event MakeArrangementBetweenGeneticProfileOwnerAndInvestor(
        address indexed originalGeneticProfileOwner,
        address indexed investor,
        uint256 investedLIFEAmount
    );

    event LinkGNFTTokenIdAndOriginalGeneticProfileOwner(
        uint256 gnftTokenId,
        address indexed originalGeneticProfileOwner

    );

    function makeArrangementBetweenGeneticProfileOwnerAndInvestor(
        address geneticProfileOwner,
        address investor,
        uint256 investedNumberOfLIFE
    ) external;

    function linkGNFTTokenIdAndOriginalGeneticProfileOwner(
        uint256 gnftTokenId,
        address originalGeneticProfileOwner
    ) external;

    function distributeRevenue(
        address fromParticipantWallet,
        address fromSender,
        uint256 gnftTokenId,
        uint256 revenue
    ) external;

    function queryCoInvestorsByGPO(
        address originalGeneticProfileOwner
    ) external view returns (address[] memory);

    function queryCoInvestorsByTokenId(
        uint256 gnftTokenId
    ) external view returns (address[] memory);

    function queryTotalAccumulatedRevenueByGPO(
        address originalGeneticProfileOwner
    ) external view returns (uint256);

    function queryTotalAccumulatedRevenueByTokenId(
        uint256 gnftTokenId
    ) external view returns (uint256);

    function queryTotalInvestedLIFEOfInvestorsByGPO(
        address originalGeneticProfileOwner
    ) external view returns (uint256);

    function queryTotalInvestedLIFEOfInvestorsByTokenId(
        uint256 gnftTokenId
    ) external view returns (uint256);

    function queryInvestedLIFEOfInvestorByGPO(
        address originalGeneticProfileOwner,
        address investor
    ) external view returns (uint256);

    function queryInvestedLIFEOfInvestorByTokenId(
        uint256 gnftTokenId,
        address investor
    ) external view returns (uint256);

}