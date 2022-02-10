// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

interface IRevenueSharingArrangement {

    event MakeArrangementOnlyGeneticProfileOwner(address indexed geneticProfileOwner);
    event MakeArrangementBetweenGeneticProfileOwnerAndInvestor(
        address indexed geneticProfileOwner,
        address indexed investor,
        uint256 investedLIFE
    );

    function makeArrangementOnlyGeneticProfileOwner(
        address _geneticProfileOwner
    ) external;

    function makeArrangementBetweenGeneticProfileOwnerAndInvestor(
        address _geneticProfileOwner,
        address _investor,
        uint256 _investedNumberOfLIFE
    ) external;

    function distributeRevenue(
        address _geneticProfileOwner,
        uint256 _earnings
    ) external;

    function queryTotalAccumulatedRevenue(
        address _geneticProfileOwner
    ) external view returns (uint256);

}