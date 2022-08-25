// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../interfaces/IGenomicDAOIncentive.sol";
import "../interfaces/IIncentiveConfiguration.sol";
import "../interfaces/IGNFTToken.sol";


contract GenomicDAOIncentive is IGenomicDAOIncentive, Ownable {
    // State Variables
    // Mapping: GeneNFT Token => risk of Stroke
    mapping(uint256 => uint256) private _riskOfGettingStrokes;

    address private _incentiveConfiguration;

    // Modifiers
    modifier validIncentiveConfiguration(address _address) {
        require(
            _address != address(0),
            "GenomicDAOIncentive: address of incentive configuration must not be null"
        );
        require(
            _address != _incentiveConfiguration,
            "GenomicDAOIncentive: address of incentive configuration existed"
        );
        _;
    }

    modifier validGeneNFTTokenID(uint256 _tokenID) {

        _;
    }

    constructor(
        address owner,
        address incentiveConfiguration
    ) {
        setIncentiveConfiguration(incentiveConfiguration);
        transferOwnership(owner);
    }

    function setIncentiveConfiguration(
        address incentiveConfiguration
    )
        external
        onlyOwner
        validIncentiveConfiguration(incentiveConfiguration)
    {
        address _oldIncentiveConfiguration = _incentiveConfiguration;
        _incentiveConfiguration = incentiveConfiguration;

        emit SetIncentiveConfiguration(
            _oldIncentiveConfiguration, incentiveConfiguration
        );
    }

    function calculateCustomerReward(
        uint256 geneNFTTokenID,
        uint256 riskOfGettingStroke,
        uint256 originalTokenValue
    )
        external
        onlyOwner
        validGeneNFTTokenID(geneNFTTokenID)
    {
        IIncentiveConfiguration configuration = IIncentiveConfiguration(
            _incentiveConfiguration
        );
        IGNFTToken geneNFTToken = IGNFTToken(configuration.getGeneNFTAddress());

        // retrieve owner of GeneNFT
        address geneNFTOwner = geneNFTToken.ownerOf(gnftTokenId);

        require(
            geneNFTOwner != address(0),
            "GenomicDAOIncentive: not found owner of geneNFTTokenID"
        );


        rewardPercentage = configuration.getCustomerRewardPercentage(
            riskOfGettingStroke
        );

         require(
            rewardPercentage > 0,
            "GenomicDAOIncentive: reward percentage must be greater than zero"
        );

        // calculate reward of customer based on their risk of getting stroke
        uint256 customerReward = originalTokenValue * rewardPercentage / 100;

        // record risk of getting stroke of customer
        _riskOfGettingStrokes[geneNFTTokenID] = riskOfGettingStroke;

        // store Reward of Customer on Genetica Wallet
        // TODO:

    }
}
