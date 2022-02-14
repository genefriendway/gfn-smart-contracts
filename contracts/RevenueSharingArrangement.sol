// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";

import "./interfaces/IContractRegistry.sol";
import "./interfaces/IRevenueSharingArrangement.sol";
import "./mixins/ReservePoolRetriever.sol";
import "./mixins/GNFTTokenRetriever.sol";
import "./GNFTToken.sol";


contract RevenueSharingArrangement is
    Ownable,
    IRevenueSharingArrangement,
    ReservePoolRetriever,
    GNFTTokenRetriever
{

    IContractRegistry public registry;

    struct Collaboration {
        address originalGeneticProfileOwner;
        address[] investors;
        // Investor Address -> Invested of LIFE
        mapping(address => uint256) investedLIFEOfInvestors;
        uint256 totalInvestedLIFEOfInvestors;
    }

    struct Arrangement {
        Collaboration collaboration;
        uint256 totalAccumulatedRevenue;
    }

    // Original Genetic Profile Owner => Collaboration struct
    mapping(address => Collaboration) collaborations;

    // Arrangement between Owner of G-NFT and Co-Investors
    // G-NFT TokenId => Arrangement
    mapping(uint256 => Arrangement) arrangements;

    modifier onlyReservePool() {
        require(
            _msgSender() == _getReservePoolAddress(registry),
            "RevenueSharingArrangement: caller must be reserve pool contract"
        );
        _;
    }

    modifier existedCollaboration(address _geneticProfileOwner) {
        require(
            collaborations[_geneticProfileOwner].originalGeneticProfileOwner != address(0),
            'RevenueSharingArrangement: Arrangement must be existed'
        );
        _;
    }

    modifier notExistedArrangement(uint256 _gnftTokenId) {
        require(
            arrangements[_gnftTokenId].collaboration.originalGeneticProfileOwner == address(0),
            'RevenueSharingArrangement: Arrangement must not be existed'
        );
        _;
    }

    modifier validGeneticProfileOwner(address _geneticProfileOwner) {
        require(
            _geneticProfileOwner != address(0),
            "RevenueSharingArrangement: genetic profile owner's address is invalid"
        );
        _;
    }

    modifier validInvestor(address _investor) {
        require(
            _investor != address(0),
            "RevenueSharingArrangement: investor's address is invalid"
        );
        _;
    }
    
    modifier validInvestedLIFE(uint256 _investedLIFEAmount) {
        require(
            _investedLIFEAmount > 0,
            "RevenueSharingArrangement: invested LIFE of investor must be greater than zero"
        );
        _;
    }

    modifier validRevenue(uint256 _revenue) {
        require(
            _revenue > 0,
            "RevenueSharingArrangement: revenue must be greater than zero"
        );
        _;
    }

    constructor(address gfnOwner, IContractRegistry _registry) {
        registry = _registry;
        transferOwnership(gfnOwner);
    }

    function makeCollaborationBetweenGeneticProfileOwnerAndInvestor(
        address _originalGeneticProfileOwner,
        address _investor,
        uint256 _investedLIFEAmount
    )
        external
        onlyReservePool
        validGeneticProfileOwner(_originalGeneticProfileOwner)
        validInvestor(_investor)
        validInvestedLIFE(_investedLIFEAmount)
    {
        // retrieve Collaboration by genetic profile owner
        Collaboration storage collaboration = collaborations[_originalGeneticProfileOwner];

        // an investor can have multiple slots in a reverse pool and a genetic
        // profile owner may need many slots in reverse pool to enough requested lIFE
        if (collaboration.investedLIFEOfInvestors[_investor] == 0){
            collaboration.investors.push(_investor);
        }
        collaboration.investedLIFEOfInvestors[_investor] += _investedLIFEAmount;
        collaboration.totalInvestedLIFEOfInvestors += _investedLIFEAmount;

        emit MakeCollaborationBetweenGeneticProfileOwnerAndInvestor(
            _originalGeneticProfileOwner, _investor, _investedLIFEAmount
        );
    }

    function makeRevenueSharingArrangement(
        address _originalGeneticProfileOwner,
        uint256 _gnftTokenId
    )
        external
        onlyOwner
        validGeneticProfileOwner(_originalGeneticProfileOwner)
        existedCollaboration(_originalGeneticProfileOwner)
        notExistedArrangement(_gnftTokenId)
    {
        // retrieve Collaboration by genetic profile owner
        Collaboration storage collaboration = collaborations[_originalGeneticProfileOwner];
        // retrieve Arrangement by G-NFT TokenId
        Arrangement storage arrangement = arrangements[_gnftTokenId];
        arrangement.collaboration = collaboration;
        arrangement.totalAccumulatedRevenue = 0;

        emit MakeRevenueSharingArrangement(
            _originalGeneticProfileOwner, _gnftTokenId
        );
    }

    function distributeRevenue(
        uint256 _gnftTokenId,
        uint256 _revenue
    )
        external
        onlyOwner
        validRevenue(_revenue)
    {
        // validate _revenue
        // retrieve current genetic profile owner
        GNFTToken gnftToken = GNFTToken(_getGNFTTokenAddress(registry));
        address _currentGeneticProfileOwner = gnftToken.ownerOf(_gnftTokenId);

        require(
            _currentGeneticProfileOwner != address(0),
            "RevenueSharingArrangement: G-NFT token id must be existed"
        );

        Arrangement storage arrangement = arrangements[_gnftTokenId];

        if(hasCollaboration(_gnftTokenId)) {
            (uint256 revenueBelongToInvestors, uint256 revenueBelongToGeneticOwner) = _calculateDistributedRevenue(arrangement, _revenue);
            // check and distribute revenue to investors
            if (revenueBelongToInvestors > 0) {
                Collaboration storage collaboration = arrangement.collaboration;
                for(uint256 index; index < collaboration.investors.length; index++) {
                    address investor = collaboration.investors[index];
                    // retrieve number of invested LIFE of a investor
                    uint256 investedLIFEOfSpecificInvestor = collaboration.investedLIFEOfInvestors[investor];
                    // calculate revenue of each investor depend on their invested LIFE
                    uint256 calculatedRevenue = revenueBelongToInvestors * investedLIFEOfSpecificInvestor / collaboration.totalInvestedLIFEOfInvestors;
                    // transfer LIFE
                    _distributeRevenueToInvestor(investor, calculatedRevenue);
                }
            }

            // check and distribute revenue to current genetic profile owner
            if (revenueBelongToGeneticOwner > 0) {
                _distributeRevenueToGeneticProfileOwner(
                    _currentGeneticProfileOwner, revenueBelongToGeneticOwner
                );
            }

        } else {
            _distributeRevenueToGeneticProfileOwner(
                _currentGeneticProfileOwner, _revenue
            );
        }
        // update total accumulated revenue that the gene was paid
        arrangement.totalAccumulatedRevenue += _revenue;
    }

    function _calculateDistributedRevenue(
        Arrangement storage _arrangement,
        uint256 _revenue
    ) private view returns (uint256 revenueBelongToInvestors, uint256 revenueBelongToGeneticOwner) {
        uint256 revenueRatio = _arrangement.totalAccumulatedRevenue / _arrangement.collaboration.totalInvestedLIFEOfInvestors;
        // only use investorsRate from multiple return by getDistributionRevenueRates
        (uint256 investorsRate, ) = getDistributionRevenueRates(revenueRatio);
        revenueBelongToInvestors = _revenue * investorsRate / 100;
        revenueBelongToGeneticOwner = _revenue - revenueBelongToInvestors;
    }

    function _distributeRevenueToGeneticProfileOwner(
        address _originalGeneticProfileOwner,
        uint256 _revenueOfGeneticOwner
    ) internal {

    }

    function _distributeRevenueToInvestor(
        address _investor,
        uint256 _revenueOfInvestor
    ) internal {

    }

    function queryTotalAccumulatedRevenue(
        uint256 _gnftTokenId
    ) external view returns (uint256){
        return arrangements[_gnftTokenId].totalAccumulatedRevenue;
    }

    function queryGeneticInvestors(
        uint256 _gnftTokenId
    ) external view returns (address[] memory){
        return arrangements[_gnftTokenId].collaboration.investors;
    }

    function queryTotalInvestedLIFEOfInvestors(
        address _originalGeneticProfileOwner
    ) external view returns (uint256){
        return collaborations[_originalGeneticProfileOwner].totalInvestedLIFEOfInvestors;
    }

    function queryTotalInvestedLIFEOfInvestors(
        uint256 _gnftTokenId
    ) external view returns (uint256){
        return arrangements[_gnftTokenId].collaboration.totalInvestedLIFEOfInvestors;
    }

    function queryInvestedLIFEOfInvestor(
        address _originalGeneticProfileOwner,
        address _investor
    ) external view returns (uint256){
        return collaborations[_originalGeneticProfileOwner].investedLIFEOfInvestors[_investor];
    }

    function queryInvestedLIFEOfInvestor(
        uint256 _gnftTokenId,
        address _investor
    ) external view returns (uint256){
        return arrangements[_gnftTokenId].collaboration.investedLIFEOfInvestors[_investor];
    }

    function hasCollaboration(
        uint256 _gnftTokenId
    ) public view returns (bool) {
        return arrangements[_gnftTokenId].collaboration.originalGeneticProfileOwner != address(0);
    }

    function getDistributionRevenueRates(
        uint256 ratio
    ) public view returns (uint256, uint256){
        // update logic here
    }
}
