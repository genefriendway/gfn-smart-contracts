// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../../interfaces/pcsp/IPCSPReward.sol";
import "../../interfaces/pcsp/IPCSPConfiguration.sol";
import "../../GNFTToken.sol";


contract PCSPReward is IPCSPReward, Ownable {
    // State Variables
    address private _addressOfPCSPConfiguration;
    // Mapping: GeneNFT Token => risk of Stroke
    mapping(uint256 => uint256) private _riskOfGettingStrokeRecords;


    // Modifiers
    modifier validPCSPConfiguration(address _address) {
        require(
            _address != address(0),
            "PCSPReward: address of PCSP configuration must not be null"
        );
        require(
            _address != _addressOfPCSPConfiguration,
            "PCSPReward: address of PCSP configuration existed"
        );
        _;
    }

    modifier validGeneNFTTokenID(uint256 _tokenID) {

        _;
    }

    constructor(
        address owner,
        address addressOfPCSPConfiguration
    )
        validPCSPConfiguration(addressOfPCSPConfiguration)
    {
        _addressOfPCSPConfiguration = addressOfPCSPConfiguration;
        transferOwnership(owner);
    }

    function setPCSPConfiguration(
        address addressOfPCSPConfiguration
    )
        external
        onlyOwner
        validPCSPConfiguration(addressOfPCSPConfiguration)
    {
        address _oldPCSPConfiguration = _addressOfPCSPConfiguration;
        _addressOfPCSPConfiguration = addressOfPCSPConfiguration;

        emit SetPCSPConfiguration(
            _oldPCSPConfiguration, addressOfPCSPConfiguration
        );
    }

    function getPCSPConfiguration() external override view returns (address) {
        return _addressOfPCSPConfiguration;
    }

    function calculateCustomerReward(
        uint256 geneNFTTokenID,
        uint256 riskOfGettingStroke,
        uint256 revenueInPCSP
    )
        external
        onlyOwner
        validGeneNFTTokenID(geneNFTTokenID)
    {
        IPCSPConfiguration configuration = IPCSPConfiguration(
            _addressOfPCSPConfiguration
        );
        GNFTToken geneNFTToken = GNFTToken(configuration.getGeneNFTAddress());

        // retrieve owner of GeneNFT
        address geneNFTOwner = geneNFTToken.ownerOf(geneNFTTokenID);

        require(
            geneNFTOwner != address(0),
            "PCSPReward: not found owner of geneNFTTokenID"
        );


        uint256 rewardPercent = configuration.getCustomerRewardPercent(
            riskOfGettingStroke
        );

         require(
            rewardPercent > 0,
            "PCSPReward: reward percent must be greater than zero"
        );

        // calculate reward of customer based on their risk of getting stroke
        uint256 customerReward = revenueInPCSP * rewardPercent / 100;

        // record risk of getting stroke of customer
        _riskOfGettingStrokeRecords[geneNFTTokenID] = riskOfGettingStroke;
        emit RecordRiskOfGettingStroke(geneNFTTokenID, riskOfGettingStroke);

        // store Reward of Customer on Genetica Wallet
        // TODO:

    }
}
