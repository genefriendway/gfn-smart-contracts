// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../../interfaces/dao/pcsp/IPCSPCustomerReward.sol";
import "../../interfaces/dao/pcsp/IPCSPCustomerRewardConfiguration.sol";
import "../../GNFTToken.sol";
import "../../common/TokenWallet.sol";


contract PCSPCustomerReward is IPCSPCustomerReward, Ownable {
    // State Variables
    address private _addressOfPCSPConfiguration;
    // Mapping: GeneNFT Token => risk of Stroke
    mapping(uint256 => uint256) private _riskOfGettingStrokeRecords;
    // Mapping: GeneNFT Token => rewarded or not
    mapping(uint256 => bool) private _geneNFTRewardStatuses;


    // Modifiers
    modifier validPCSPConfiguration(address _address) {
        require(
            _address != address(0),
            "PCSPCustomerReward: address of PCSP configuration must not be null"
        );
        require(
            _address != _addressOfPCSPConfiguration,
            "PCSPCustomerReward: address of PCSP configuration existed"
        );
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

    function getRiskOfGettingStroke(
        uint256 geneNFTTokenID
    )
        external override view returns (uint256)
    {
        return _riskOfGettingStrokeRecords[geneNFTTokenID];
    }

    function checkGeneNFTRewardStatus(
        uint256 geneNFTTokenID
    )
        external override view returns (bool)
    {
        return _geneNFTRewardStatuses[geneNFTTokenID];
    }

    function calculateRewardForMultipleCustomers(
        uint256[] memory geneNFTTokenIDs,
        uint256[] memory risksOfGettingStroke,
        uint256[] memory revenuesInPCSP
    )
        external
        override
        onlyOwner
    {
        require(
            geneNFTTokenIDs.length == risksOfGettingStroke.length,
            "PCSPCustomerReward: list of GeneNFTTokenIds and risksOfGettingStroke must have same length"
        );
        require(
            risksOfGettingStroke.length == revenuesInPCSP.length,
            "PCSPCustomerReward: list of risksOfGettingStroke and revenuesInPCSP must have same length"
        );

        for(uint256 i = 0; i < geneNFTTokenIDs.length; i++) {
            _calculateCustomerReward(
                geneNFTTokenIDs[i], risksOfGettingStroke[i], revenuesInPCSP[i]
            );
        }

    }

    function _calculateCustomerReward(
        uint256 geneNFTTokenID,
        uint256 riskOfGettingStroke,
        uint256 revenueInPCSP
    )
        private
    {
        require(
            !_geneNFTRewardStatuses[geneNFTTokenID],
            "PCSPCustomerReward: the GeneNFT has rewarded for risk of getting stroke"
        );

        IPCSPCustomerRewardConfiguration config = IPCSPCustomerRewardConfiguration(
            _addressOfPCSPConfiguration
        );
        require(
            config.checkActiveRiskOfGettingStroke(riskOfGettingStroke),
            "PCSPCustomerReward: risk of getting stroke value is invalid"
        );

        GNFTToken geneNFTToken = GNFTToken(config.getGeneNFTAddress());
        // retrieve owner of GeneNFT
        address geneNFTOwner = geneNFTToken.ownerOf(geneNFTTokenID);


        // mark GeneNFT rewarded
        _geneNFTRewardStatuses[geneNFTTokenID] = true;
        // record risk of getting stroke of customer
        _riskOfGettingStrokeRecords[geneNFTTokenID] = riskOfGettingStroke;

        emit RecordRiskOfGettingStroke(geneNFTTokenID, riskOfGettingStroke);

        // calculate reward of customer based on risk of getting stroke value
        uint256 customerRewardInPCSP = config.calculateCustomerReward(
            riskOfGettingStroke, revenueInPCSP
        );

        // store Reward of Customer on Token PCSP Wallet
        TokenWallet tokenWallet = TokenWallet(config.getTokenPCSPWalletAddress());
        tokenWallet.increaseBalance(
            geneNFTOwner,
            customerRewardInPCSP,
            "Reward for risk of getting stroke"
        );

        emit RewardForRiskOfGettingStroke(
            geneNFTTokenID,
            geneNFTOwner,
            riskOfGettingStroke,
            revenueInPCSP,
            customerRewardInPCSP
        );
    }
}
