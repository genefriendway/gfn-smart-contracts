// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/IContractRegistry.sol";
import "./interfaces/IConfiguration.sol";
import "./mixins/AccessibleRegistry.sol";


contract Configuration is
    IConfiguration,
    Ownable,
    AccessibleRegistry
{
    
     // mapping from Contract address to GFN Operator
    mapping(address => address) private operators;

    address private NFTHolder;

    // ==== START - Properties for G-NFT TokenURI ==========
    string private baseGNFTTokenURI = "";
    // ==== END - Properties for G-NFT TokenURI ==========
    
    // ==== START - Properties for minting LIFE TOKEN ==========
    struct GNFTRange {
        uint256 lower;
        uint256 upper;
        uint256 numberOfLIFEToMint;
    }
    // Mapping from index to GNFTRange
    mapping(uint256 => GNFTRange) private tableOfMintingLIFE;
    uint256 private totalGNFTRanges = 18;
    // ==== END - Properties for minting LIFE TOKEN ==========
    
    // ==== START - Properties for Distribution Revenue ==========
    struct RevenueRatio {
        uint256 percentageForInvestor;
        uint256 percentageForGeneticProfileOwner;
    }
    // index => RevenueRatio
    mapping(uint256 => RevenueRatio) private revenueRatios;
    // ==== END - Properties for Distribution Revenue ==========


    modifier validContractAddress(address contractAddress) {
        require(
            registry.isRegisteredContract(contractAddress),
            "Configuration: can not set operator for invalid contract address"
        );
        _;
    }

    modifier validNewOperator(address newOperator) {
        require(
            newOperator != address(0),
            "Configuration: new operator must be not empty"
        );
        _;
    }

    modifier validNFTHolder(address _NFTHolder) {
        require(
            _NFTHolder != address(0),
            "Configuration: NFT holder's address must be not empty"
        );
        _;
    }

    constructor(
        address gfnOwner,
        address _NFTHolder,
        IContractRegistry _registry
    )
        AccessibleRegistry(_registry)
    {
        NFTHolder = _NFTHolder;
        _initializeTableOfMintingLIFE();
        _setupDistributionRatios();
        transferOwnership(gfnOwner);
    }

    function setNFTHolder(
        address holder
    )
        external onlyOwner validNFTHolder(holder)
    {
        NFTHolder = holder;

        emit SetNFTHolder(holder);
    }
    
    function setOperator(
        address contractAddress,
        address newOperator
    )
        external
        override
        onlyOwner
        validContractAddress(contractAddress)
        validNewOperator(newOperator)
    {
        address oldOperator = operators[contractAddress];
        operators[contractAddress] = newOperator;
        emit SetOperator(contractAddress, oldOperator, operators[contractAddress]);
    }

    function setBaseGNFTTokenURI(
        string memory baseURI
    )
        external onlyOwner
    {
        require(
            bytes(baseURI).length > 0,
            "Configuration: base G-NFT token URI must be not empty"
        );
        baseGNFTTokenURI = baseURI;

        emit SetBaseGNFTTokenURI(baseURI);
    }

    function getNFTHolder() external override view returns (address) {
        return NFTHolder;
    }

    function getOperator(
        address contractAddress
    )
        external override view returns (address)
    {
        return operators[contractAddress];
    }

    function getBaseGNFTTokenURI() external view returns (string memory) {
        return baseGNFTTokenURI;
    }

    function findNumberOfLIFEToMint(
        uint256 totalGNFTTokens
    )
        external view returns (uint256)
    {
        for(uint256 index = 0; index < totalGNFTRanges; index++) {
            GNFTRange storage range = tableOfMintingLIFE[index];
            if (totalGNFTTokens >= range.lower && totalGNFTTokens <= range.upper) {
                return range.numberOfLIFEToMint;
            }
        }
        return 0;
    }

    function _initializeTableOfMintingLIFE() private {
        // tableOfMintingLIFE[index] = GNFTRange(lower, upper, number of LIFE);
        tableOfMintingLIFE[0] = GNFTRange(1, 1, 9*10**25);
        tableOfMintingLIFE[1] = GNFTRange(2, 10**1, 10**25);
        tableOfMintingLIFE[2] = GNFTRange(10**1 + 1, 10**2, 10**24);
        tableOfMintingLIFE[3] = GNFTRange(10**2 + 1, 10**3, 10**23);
        tableOfMintingLIFE[4] = GNFTRange(10**3 + 1, 10**4, 10**22);
        tableOfMintingLIFE[5] = GNFTRange(10**4 + 1, 10**5, 10**21);
        tableOfMintingLIFE[6] = GNFTRange(10**5 + 1, 10**6, 10**20);
        tableOfMintingLIFE[7] = GNFTRange(10**6 + 1, 10**7, 10**19);
        tableOfMintingLIFE[8] = GNFTRange(10**7 + 1, 10**8, 10**18);
        tableOfMintingLIFE[9] = GNFTRange(10**8 + 1, 10**9, 10**17);
        tableOfMintingLIFE[10] = GNFTRange(10**9 + 1, 10**10, 10**16);
        tableOfMintingLIFE[11] = GNFTRange(10**10 + 1, 10**11, 10**15);
        tableOfMintingLIFE[12] = GNFTRange(10**11 + 1, 10**12, 10**14);
        tableOfMintingLIFE[13] = GNFTRange(10**12 + 1, 10**13, 10**13);
        tableOfMintingLIFE[14] = GNFTRange(10**13 + 1, 10**14, 10**12);
        tableOfMintingLIFE[15] = GNFTRange(10**14 + 1, 10**15, 10**11);
        tableOfMintingLIFE[16] = GNFTRange(10**15 + 1, 10**16, 10**10);
        tableOfMintingLIFE[17] = GNFTRange(10**16 + 1, 10**17, 10**9);
    }
    
    function _setupDistributionRatios() private {
        revenueRatios[0] = RevenueRatio(100, 0);
        revenueRatios[1] = RevenueRatio(80, 20);
        revenueRatios[2] = RevenueRatio(60, 40);
        revenueRatios[3] = RevenueRatio(40, 60);
        revenueRatios[4] = RevenueRatio(20, 80);
    }

    function getRevenueDistributionRanges(
        uint256 totalInvestedLIFEOfInvestors
    )
        internal view returns (uint256[3][5] memory)
    {
        uint256[3][5] memory revenueDistributionRanges;
        for(uint256 index = 0; index <= 4; index++) {
            uint256[3] memory ranges;
            // first position: revenue milestone
            ranges[0] = totalInvestedLIFEOfInvestors * (index + 1);
            // second position: percentage of revenue belong to investors
            ranges[1] = revenueRatios[index].percentageForInvestor;
            // third position: percentage of revenue belong to GPO
            ranges[2] = revenueRatios[index].percentageForGeneticProfileOwner;

            revenueDistributionRanges[index] = ranges;
        }
        return revenueDistributionRanges;
    }

    function getRevenueDistributionRatios(
        uint256 totalInvestedLIFEOfInvestors,
        uint256 totalAccumulatedRevenue,
        uint256 newRevenue
    )
        external view returns (uint256[4] memory)
    {
        // return [remainingNewRevenue, distributedRevenue, % of Investor, % of GPO]

        uint256[3][5] memory revenueDistributionRanges = getRevenueDistributionRanges(
            totalInvestedLIFEOfInvestors
        );

        for(uint256 index = 0; index <= 4; index++) {
            uint256[3] memory ranges = revenueDistributionRanges[index];
            uint256 milestoneRevenue = ranges[0];
            if (totalAccumulatedRevenue < milestoneRevenue) {
                uint256 revenueToFillUpMilestone = milestoneRevenue - totalAccumulatedRevenue;
                uint256 distributedRevenue;
                uint256 remainingNewRevenue;

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
}