// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";

import "./interfaces/IContractRegistry.sol";
import "./interfaces/IRevenueSharingArrangement.sol";
import "./interfaces/IParticipantWallet.sol";
import "./mixins/ReservePoolRetriever.sol";
import "./mixins/GNFTTokenRetriever.sol";
import "./mixins/GeneticProfileOwnerWalletRetriever.sol";
import "./mixins/InvestorWalletRetriever.sol";
import "./GNFTToken.sol";


contract RevenueSharingArrangement is
    Ownable,
    IRevenueSharingArrangement,
    ReservePoolRetriever,
    GNFTTokenRetriever,
    GeneticProfileOwnerWalletRetriever,
    InvestorWalletRetriever
{

    IContractRegistry public registry;

    struct DistributionRatio {
        uint256 percentageForInvestor;
        uint256 percentageForGeneticProfileOwner;
    }
    // index => DistributionRatio
    mapping(uint256 => DistributionRatio) private _distributionRatios;

    struct Arrangement {
        address originalGeneticProfileOwner;
        address[] investors;
        // Investor Address -> Invested of LIFE
        mapping(address => uint256) investedLIFEOfInvestors;
        uint256 totalInvestedLIFEOfInvestors;
        uint256 totalAccumulatedRevenue;
    }

    // originalGeneticProfileOwner => Arrangement struct
    mapping(address => Arrangement) arrangements;
    // G-NFT TokenId => originalGeneticProfileOwner
    mapping(uint256 => address) gnftTokenIdToOriginalOwner;

    modifier onlyReservePool() {
        require(
            _msgSender() == _getReservePoolAddress(registry),
            "RevenueSharingArrangement: caller must be reserve pool contract"
        );
        _;
    }

    modifier existedArrangement(address _geneticProfileOwner) {
        require(
            arrangements[_geneticProfileOwner].originalGeneticProfileOwner != address(0),
            'RevenueSharingArrangement: Arrangement must be existed'
        );
        _;
    }


    modifier notLinkFromTokenIdToOriginalOwner(uint256 gnftTokenId) {
        require(
            gnftTokenIdToOriginalOwner[gnftTokenId] == address(0),
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


    modifier validInvestor(address investor) {
        require(
            investor != address(0),
            "RevenueSharingArrangement: investor's address is invalid"
        );
        _;
    }
    
    modifier validInvestedLIFE(uint256 investedLIFEAmount) {
        require(
            investedLIFEAmount > 0,
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
        _setupDistributionRatios();
    }

    function makeArrangementBetweenGeneticProfileOwnerAndInvestor(
        address originalGeneticProfileOwner,
        address investor,
        uint256 investedLIFEAmount
    )
        external
        onlyReservePool
        validGeneticProfileOwner(originalGeneticProfileOwner)
        validInvestor(investor)
        validInvestedLIFE(investedLIFEAmount)
    {
        // retrieve Arrangement by original genetic profile owner
        Arrangement storage arrangement = arrangements[originalGeneticProfileOwner];

        // an investor can have multiple slots in a reverse pool and a genetic
        // profile owner may need many slots in reverse pool to enough requested lIFE
        // initialize Arrangement properties
        if (arrangement.originalGeneticProfileOwner == address(0)) {
            arrangement.originalGeneticProfileOwner = originalGeneticProfileOwner;
        }
        if (arrangement.investedLIFEOfInvestors[investor] == 0){
            arrangement.investors.push(investor);
        }
        arrangement.investedLIFEOfInvestors[investor] += investedLIFEAmount;
        arrangement.totalInvestedLIFEOfInvestors += investedLIFEAmount;

        emit MakeArrangementBetweenGeneticProfileOwnerAndInvestor(
            originalGeneticProfileOwner, investor, investedLIFEAmount
        );
    }

    function linkGNFTTokenIdAndOriginalGeneticProfileOwner(
        uint256 gnftTokenId,
        address originalGeneticProfileOwner
    )
        external
        onlyOwner
        validGeneticProfileOwner(originalGeneticProfileOwner)
        existedArrangement(originalGeneticProfileOwner)
        notLinkFromTokenIdToOriginalOwner(gnftTokenId)
    {
        // retrieve current genetic profile owner
        GNFTToken gnftToken = GNFTToken(_getGNFTTokenAddress(registry));
        address currentGeneticProfileOwner = gnftToken.ownerOf(gnftTokenId);

        require(
            currentGeneticProfileOwner != address(0),
            "RevenueSharingArrangement: G-NFT token id must be existed"
        );

        gnftTokenIdToOriginalOwner[gnftTokenId] = originalGeneticProfileOwner;

        emit LinkGNFTTokenIdAndOriginalGeneticProfileOwner(
            gnftTokenId, originalGeneticProfileOwner
        );
    }

    function distributeRevenue(
        address fromParticipantWallet,
        address fromSender,
        uint256 gnftTokenId,
        uint256 revenue
    )
        external
        onlyOwner
        validRevenue(revenue)
    {
        // retrieve current genetic profile owner
        GNFTToken gnftToken = GNFTToken(_getGNFTTokenAddress(registry));
        address currentGeneticProfileOwner = gnftToken.ownerOf(gnftTokenId);

        require(
            currentGeneticProfileOwner != address(0),
            "RevenueSharingArrangement: G-NFT token id must be existed"
        );

        // retrieve Arrangement by G-NFT Token Id
        address originalGeneticProfileOwner = gnftTokenIdToOriginalOwner[gnftTokenId];
        Arrangement storage arrangement = arrangements[originalGeneticProfileOwner];

        if(hasArrangementByTokenId(gnftTokenId)) {
            _distributeRevenueByArrangement(
                fromParticipantWallet,
                fromSender,
                arrangement,
                currentGeneticProfileOwner,
                revenue
            );
        } else {
            _distributeRevenueToGeneticProfileOwner(
                fromParticipantWallet,
                fromSender,
                currentGeneticProfileOwner,
                revenue
            );
        }
    }

    function _distributeRevenueByArrangement(
        address fromParticipantWallet,
        address fromSender,
        Arrangement storage arrangement,
        address currentGeneticProfileOwner,
        uint256 newRevenue
    ) private onlyOwner {
        
        uint256 remainingNotDistributedRevenue = newRevenue;

        while (remainingNotDistributedRevenue > 0) {
            // distributions = [ remainingNewRevenue, distributedRevenue, % for Investor, % for GPO]
            uint256[4] memory distributions = getDistributionRevenueRatios(
                arrangement.totalInvestedLIFEOfInvestors,
                arrangement.totalAccumulatedRevenue,
                remainingNotDistributedRevenue
            );
            remainingNotDistributedRevenue = distributions[0];

            uint256 revenueOfInvestors = distributions[1] * distributions[2] / 100;
            uint256 revenueOfGPO = distributions[1] - revenueOfInvestors;

            // check and distribute revenue to investors
            if (revenueOfInvestors > 0) {
                for(uint256 index; index < arrangement.investors.length; index++) {
                    address investor = arrangement.investors[index];
                    // retrieve number of invested LIFE of a investor
                    uint256 investedLIFEOfSpecificInvestor = arrangement.investedLIFEOfInvestors[investor];
                    // calculate revenue of each investor depend on their invested LIFE
                    uint256 calculatedRevenue = revenueOfInvestors * investedLIFEOfSpecificInvestor / arrangement.totalInvestedLIFEOfInvestors;
                    // transfer LIFE to investor wallet
                    _distributeRevenueToInvestor(
                        fromParticipantWallet,
                        fromSender,
                        investor,
                        calculatedRevenue
                    );
                }
            }

            // check and distribute revenue to current genetic profile owner
            if (revenueOfGPO > 0) {
                _distributeRevenueToGeneticProfileOwner(
                    fromParticipantWallet,
                    fromSender,
                    currentGeneticProfileOwner,
                    revenueOfGPO
                );
            }
            // increase more Accumulated Revenue
            arrangement.totalAccumulatedRevenue += distributions[1];
        }
    }

    function _distributeRevenueToGeneticProfileOwner(
        address fromParticipantWallet,
        address fromSender,
        address toGeneticProfileOwner,
        uint256 revenue
    ) private onlyOwner {
        IParticipantWallet wallet = IParticipantWallet(fromParticipantWallet);
        wallet.transferToAnotherParticipantWallet(
            fromSender,
            _getGeneticProfileOwnerWalletAddress(registry),
            toGeneticProfileOwner,
            revenue
        );
    }

    function _distributeRevenueToInvestor(
        address fromParticipantWallet,
        address fromSender,
        address toInvestor,
        uint256 revenue
    ) private onlyOwner {
        IParticipantWallet wallet = IParticipantWallet(fromParticipantWallet);
        wallet.transferToAnotherParticipantWallet(
            fromSender,
            _getInvestorWalletAddress(registry),
            toInvestor,
            revenue
        );
    }

    function queryCoInvestorsByGPO(
        address originalGeneticProfileOwner
    ) external view returns (address[] memory){
        Arrangement storage arrangement = arrangements[originalGeneticProfileOwner];
        return arrangement.investors;
    }

    function queryCoInvestorsByTokenId(
        uint256 gnftTokenId
    ) external view returns (address[] memory){
        address originalGeneticProfileOwner = gnftTokenIdToOriginalOwner[gnftTokenId];
        Arrangement storage arrangement = arrangements[originalGeneticProfileOwner];
        return arrangement.investors;
    }

    function queryTotalAccumulatedRevenueByGPO(
        address originalGeneticProfileOwner
    ) external view returns (uint256){
        Arrangement storage arrangement = arrangements[originalGeneticProfileOwner];
        return arrangement.totalAccumulatedRevenue;
    }

    function queryTotalAccumulatedRevenueByTokenId(
        uint256 gnftTokenId
    ) external view returns (uint256){
        address originalGeneticProfileOwner = gnftTokenIdToOriginalOwner[gnftTokenId];
        Arrangement storage arrangement = arrangements[originalGeneticProfileOwner];
        return arrangement.totalAccumulatedRevenue;
    }

    function queryTotalInvestedLIFEOfInvestorsByGPO(
        address originalGeneticProfileOwner
    ) external view returns (uint256){
        return arrangements[originalGeneticProfileOwner].totalInvestedLIFEOfInvestors;
    }

    function queryTotalInvestedLIFEOfInvestorsByTokenId(
        uint256 gnftTokenId
    ) external view returns (uint256){
        address originalGeneticProfileOwner = gnftTokenIdToOriginalOwner[gnftTokenId];
        Arrangement storage arrangement = arrangements[originalGeneticProfileOwner];
        return arrangement.totalInvestedLIFEOfInvestors;
    }

    function queryInvestedLIFEOfInvestorByGPO(
        address originalGeneticProfileOwner,
        address investor
    ) external view returns (uint256){
        return arrangements[originalGeneticProfileOwner].investedLIFEOfInvestors[investor];
    }

    function queryInvestedLIFEOfInvestorByTokenId(
        uint256 gnftTokenId,
        address investor
    ) external view returns (uint256){
        address originalGeneticProfileOwner = gnftTokenIdToOriginalOwner[gnftTokenId];
        Arrangement storage arrangement = arrangements[originalGeneticProfileOwner];
        return arrangement.investedLIFEOfInvestors[investor];
    }

    function hasArrangementByGPO(
        address originalGeneticProfileOwner
    ) public view returns (bool) {
        Arrangement storage arrangement = arrangements[originalGeneticProfileOwner];
        return arrangement.originalGeneticProfileOwner != address(0)
            && arrangement.originalGeneticProfileOwner == originalGeneticProfileOwner;
    }

    function hasArrangementByTokenId(
        uint256 gnftTokenId
    ) public view returns (bool) {
        address originalGeneticProfileOwner = gnftTokenIdToOriginalOwner[gnftTokenId];
        Arrangement storage arrangement = arrangements[originalGeneticProfileOwner];
        return arrangement.originalGeneticProfileOwner != address(0);
    }

     function _setupDistributionRatios() private {
        _distributionRatios[0] = DistributionRatio(100, 0);
        _distributionRatios[1] = DistributionRatio(80, 20);
        _distributionRatios[2] = DistributionRatio(60, 40);
        _distributionRatios[3] = DistributionRatio(40, 60);
        _distributionRatios[4] = DistributionRatio(20, 80);
    }

    function getDistributionRevenueRatios(
        uint256 _totalInvestedLIFEOfInvestors,
        uint256 _totalAccumulatedRevenue,
        uint256 newRevenue
    )
        public view returns (uint256[4] memory)
    {
        uint256[3][5] memory revenueRanges = getDistributionRevenueRanges(
            _totalInvestedLIFEOfInvestors
        );
        // [remainingNewRevenue, distributedRevenue, % for Investor, % for GPO]
        uint256[4] memory distributions;
        uint256 remainingNewRevenue;
        for(uint256 index = 0; index <= 4; index++) {
            uint256[3] memory ranges = revenueRanges[index];
            uint256 milestoneRevenue = ranges[0];
            if (_totalAccumulatedRevenue < milestoneRevenue) {
                uint256 revenueToFillUpMilestone = milestoneRevenue - _totalAccumulatedRevenue;
                uint256 distributedRevenue;
                if (newRevenue <= revenueToFillUpMilestone) {
                    distributedRevenue = newRevenue;
                    remainingNewRevenue = 0;
                } else {
                    distributedRevenue = revenueToFillUpMilestone;
                    remainingNewRevenue = newRevenue - revenueToFillUpMilestone;
                }
                return [remainingNewRevenue, distributedRevenue, ranges[1], ranges[2]];
            }
        }
        // if total Accumulated Revenue went through all milestones
        // => always keep ratio 20 % (investor) - 80 % (GPO)
        return [0, newRevenue, 20, 80];
    }

    function getDistributionRevenueRanges(
        uint256 _totalInvestedLIFEOfInvestors
    ) public view returns (uint256[3][5] memory){
        uint256[3][5] memory revenueRanges;
        for(uint256 index = 0; index <= 4; index++) {
            uint256[3] memory ranges;
            // first position: revenue milestone
            ranges[0] = _totalInvestedLIFEOfInvestors * (index + 1);
            // second position: percentage of revenue belong to investors
            ranges[1] = _distributionRatios[index].percentageForInvestor;
            // third position: percentage of revenue belong to GPO
            ranges[2] = _distributionRatios[index].percentageForGeneticProfileOwner;

            revenueRanges[index] = ranges;
        }
        return revenueRanges;
    }
}
