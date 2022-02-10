// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";

import "./interfaces/IContractRegistry.sol";
import "./interfaces/IRevenueSharingArrangement.sol";


contract RevenueSharingArrangement is
    Ownable,
    IRevenueSharingArrangement
{

    IContractRegistry public registry;

    struct Arrangement {
        bool hasCoInvestors;
        address geneticProfileOwner;
        address[] investors;
        mapping(address => uint256) investedLIFEOfInvestors;
        uint256 totalInvestedLIFEOfInvestors;
        uint256 totalAccumulatedRevenue;
    }

    // geneticProfileOwner => Arrangement
    mapping(address => Arrangement) arrangements;

    modifier notExistedArrangement(address _geneticProfileOwner) {
        require(
            arrangements[_geneticProfileOwner].geneticProfileOwner == address(0),
            'RevenueSharingArrangement: Arrangement was existed');
        _;
    }

    constructor(address gfnOwner, IContractRegistry _registry) {
        registry = _registry;
        transferOwnership(gfnOwner);
    }

    function makeArrangementOnlyGeneticProfileOwner(
        address _geneticProfileOwner
    ) external onlyOwner notExistedArrangement(_geneticProfileOwner){
        Arrangement storage arrangement = arrangements[_geneticProfileOwner];
        arrangement.hasCoInvestors = false;
        arrangement.geneticProfileOwner = _geneticProfileOwner;
        arrangement.totalAccumulatedRevenue = 0;

        emit MakeArrangementOnlyGeneticProfileOwner(_geneticProfileOwner);
    }

    function makeArrangementBetweenGeneticProfileOwnerAndInvestor(
        address _geneticProfileOwner,
        address _investor,
        uint256 _investedLIFE
    ) external onlyOwner{
        // validations
        require(
            _investor != address(0),
            "RevenueSharingArrangement: investor is required"
        );
        require(
            _investedLIFE > 0,
            "RevenueSharingArrangement: invested LIFE of investors are required"
        );

        // make a genetic investment arrangement
        Arrangement storage arrangement = arrangements[_geneticProfileOwner];

        // check existed investor
        require(
            arrangement.investedLIFEOfInvestors[_investor] == 0,
            "RevenueSharingArrangement: investor existed in the arrangement"
        );

        arrangement.hasCoInvestors = true;
        arrangement.geneticProfileOwner = _geneticProfileOwner;
        arrangement.investors.push(_investor);
        arrangement.investedLIFEOfInvestors[_investor] = _investedLIFE;
        arrangement.totalInvestedLIFEOfInvestors += _investedLIFE;
        arrangement.totalAccumulatedRevenue = 0;

        emit MakeArrangementBetweenGeneticProfileOwnerAndInvestor(
            _geneticProfileOwner, _investor, _investedLIFE
        );
    }

    function distributeRevenue(
        address _geneticProfileOwner,
        uint256 _revenue
    ) external onlyOwner {
        Arrangement storage arrangement = arrangements[_geneticProfileOwner];
        if ( arrangement.hasCoInvestors == false) {
            _distributeRevenueToGeneticOwner(_geneticProfileOwner, _revenue);
        } else {
            (uint256 revenueBelongToInvestors, uint256 revenueBelongToGeneticOwner) = _calculateDistributedRevenue(arrangement, _revenue);
            // check and distribute revenue to investors
            if (revenueBelongToInvestors > 0) {
                for(uint256 index; index < arrangement.investors.length; index++) {
                    address investor = arrangement.investors[index];
                    // retrieve number of invested LIFE of a investor
                    uint256 investedLIFEOfSpecificInvestor = arrangement.investedLIFEOfInvestors[investor];
                    // calculate revenue of each investor depend on their invested LIFE
                    uint256 calculatedRevenue = revenueBelongToInvestors * investedLIFEOfSpecificInvestor / arrangement.totalInvestedLIFEOfInvestors;
                    // transfer LIFE
                    _distributeRevenueToInvestor(investor, calculatedRevenue);
                }
            }

            // check and distribute revenue to geneticProfileOwner
            if (revenueBelongToGeneticOwner > 0) {
                _distributeRevenueToGeneticOwner(_geneticProfileOwner, revenueBelongToGeneticOwner);
            }

        }
        arrangement.totalAccumulatedRevenue += _revenue;
    }

    function _calculateDistributedRevenue(
        Arrangement storage _arrangement,
        uint256 _revenue
    ) private view returns (uint256 revenueBelongToInvestors, uint256 revenueBelongToGeneticOwner) {
        uint256 revenueRatio = _arrangement.totalAccumulatedRevenue / _arrangement.totalInvestedLIFEOfInvestors;
        // only use investorsRate from multiple return by getDistributionRevenueRates
        (uint256 investorsRate, ) = getDistributionRevenueRates(revenueRatio);
        revenueBelongToInvestors = _revenue * investorsRate / 100;
        revenueBelongToGeneticOwner = _revenue - revenueBelongToInvestors;
    }

    function _distributeRevenueToGeneticOwner(
        address _geneticProfileOwner,
        uint256 _revenueOfGeneticOwner
    ) private onlyOwner {

    }

    function _distributeRevenueToInvestor(
        address _investor,
        uint256 _revenueOfInvestor
    ) private onlyOwner {

    }

    function getDistributionRevenueRates(
        uint256 ratio
    ) public view returns (uint256, uint256){

    }

    function hasCoInvestors(
        address _geneticProfileOwner
    ) external view returns (bool) {
        return arrangements[_geneticProfileOwner].hasCoInvestors;
    }

    function queryTotalAccumulatedRevenue(
        address _geneticProfileOwner
    ) external view returns (uint256){
        return arrangements[_geneticProfileOwner].totalAccumulatedRevenue;
    }

    function queryGeneticInvestors(
        address _geneticProfileOwner
    ) external view returns (address[] memory){
        return arrangements[_geneticProfileOwner].investors;
    }

    function queryTotalInvestedLIFEOfInvestors(
        address _geneticProfileOwner
    ) external view returns (uint256){
        return arrangements[_geneticProfileOwner].totalInvestedLIFEOfInvestors;
    }

    function queryInvestedLIFEOfInvestor(
        address _geneticProfileOwner, address _investor
    ) external view returns (uint256){
        return arrangements[_geneticProfileOwner].investedLIFEOfInvestors[_investor];
    }
}
