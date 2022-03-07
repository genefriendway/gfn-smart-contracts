// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "./interfaces/IContractRegistry.sol";
import "./interfaces/IRevenueSharingArrangement.sol";
import "./interfaces/IParticipantWallet.sol";
import "./interfaces/IConfiguration.sol";
import "./mixins/ReservePoolRetriever.sol";
import "./mixins/GNFTTokenRetriever.sol";
import "./mixins/GeneticProfileOwnerWalletRetriever.sol";
import "./mixins/InvestorWalletRetriever.sol";
import "./mixins/DataUtilizationRetriever.sol";
import "./GNFTToken.sol";
import "./mixins/AccessibleRegistry.sol";


contract RevenueSharingArrangement is
    IRevenueSharingArrangement,
    AccessibleRegistry,
    ReservePoolRetriever,
    GNFTTokenRetriever,
    GeneticProfileOwnerWalletRetriever,
    InvestorWalletRetriever,
    DataUtilizationRetriever
{

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

    modifier onlyOperatorOrDataUtilization() {
        require(
            checkSenderIsOperator()|| _msgSender() == _getDataUtilizationAddress(registry),
            "RevenueSharingArrangement: caller must be GFN Owner or DataUtilization contract"
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

    constructor(IContractRegistry _registry) AccessibleRegistry(_registry){}

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
        onlyOperator
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
        onlyOperatorOrDataUtilization
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
                revenue,
                gnftTokenId
            );
        } else {
            _distributeRevenueToGeneticProfileOwner(
                fromParticipantWallet,
                fromSender,
                currentGeneticProfileOwner,
                revenue,
                gnftTokenId
            );
        }

        emit DistributeRevenue(
            fromParticipantWallet, fromSender, gnftTokenId, revenue
        );
    }

    function _distributeRevenueByArrangement(
        address fromParticipantWallet,
        address fromSender,
        Arrangement storage arrangement,
        address currentGeneticProfileOwner,
        uint256 newRevenue,
        uint256 gnftTokenId
    )
        private
    {
        IConfiguration config = IConfiguration(_getConfigurationAddress(registry));
        uint256 remainingNotDistributedRevenue = newRevenue;

        while (remainingNotDistributedRevenue > 0) {
            // distributions = [ remainingNewRevenue, distributedRevenue, % for Investor, % for GPO]
            uint256[4] memory distributions = config.getRevenueDistributionRatios(
                arrangement.totalInvestedLIFEOfInvestors,
                arrangement.totalAccumulatedRevenue,
                remainingNotDistributedRevenue
            );
            remainingNotDistributedRevenue = distributions[0];

            uint256 revenueOfInvestors = distributions[1] * distributions[2] / 100;
            uint256 revenueOfGPO = distributions[1] - revenueOfInvestors;

            // check and distribute revenue to investors
            if (revenueOfInvestors > 0) {
                uint256 totalCalculatedRevenue = 0;

                for(uint256 index; index < arrangement.investors.length; index++) {

                    address investor = arrangement.investors[index];

                    // calculate revenue of each investor depend on their invested LIFE
                    uint256 calculatedRevenue = revenueOfInvestors * arrangement.investedLIFEOfInvestors[investor] / arrangement.totalInvestedLIFEOfInvestors;

                    // Handle precision loss for the last investor
                    if (index == arrangement.investors.length - 1) {
                        calculatedRevenue = revenueOfInvestors - totalCalculatedRevenue;
                    } else {
                        totalCalculatedRevenue += calculatedRevenue;
                    }

                    // transfer LIFE to investor wallet
                    _distributeRevenueToInvestor(
                        fromParticipantWallet,
                        fromSender,
                        investor,
                        calculatedRevenue,
                        gnftTokenId
                    );
                }
            }

            // check and distribute revenue to current genetic profile owner
            if (revenueOfGPO > 0) {
                _distributeRevenueToGeneticProfileOwner(
                    fromParticipantWallet,
                    fromSender,
                    currentGeneticProfileOwner,
                    revenueOfGPO,
                    gnftTokenId
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
        uint256 revenue,
        uint256 byNFTTokenId
    )
        private
    {
        IParticipantWallet wallet = IParticipantWallet(fromParticipantWallet);
        wallet.transferToAnotherParticipantWallet(
            fromSender,
            _getGeneticProfileOwnerWalletAddress(registry),
            toGeneticProfileOwner,
            revenue
        );

        emit DistributeRevenueToGeneticProfileOwner(
            fromParticipantWallet, fromSender, toGeneticProfileOwner, revenue, byNFTTokenId
        );
    }

    function _distributeRevenueToInvestor(
        address fromParticipantWallet,
        address fromSender,
        address toInvestor,
        uint256 revenue,
        uint256 byNFTTokenId
    )
        private
    {
        IParticipantWallet wallet = IParticipantWallet(fromParticipantWallet);
        wallet.transferToAnotherParticipantWallet(
            fromSender,
            _getInvestorWalletAddress(registry),
            toInvestor,
            revenue
        );
        emit DistributeRevenueToInvestor(
            fromParticipantWallet, fromSender, toInvestor, revenue, byNFTTokenId
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
}
