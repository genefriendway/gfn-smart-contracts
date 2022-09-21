// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../../interfaces/pcsp/IPCSPReward.sol";
import "../../interfaces/pcsp/IPCSPConfiguration.sol";
import "../../GNFTToken.sol";
import "../../common/TokenWallet.sol";


contract PCSPReward is IPCSPReward, Ownable {
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
            "PCSPReward: address of PCSP configuration must not be null"
        );
        require(
            _address != _addressOfPCSPConfiguration,
            "PCSPReward: address of PCSP configuration existed"
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

    function calculateCustomerReward(
        uint256 geneNFTTokenID,
        uint256 riskOfGettingStroke,
        uint256 revenueInPCSP
    )
        external
        onlyOwner
    {
        require(
            !_geneNFTRewardStatuses[geneNFTTokenID],
            "PCSPReward: the GeneNFT has rewarded for risk of getting stroke"
        );

        IPCSPConfiguration config = IPCSPConfiguration(
            _addressOfPCSPConfiguration
        );
        GNFTToken geneNFTToken = GNFTToken(config.getGeneNFTAddress());

        // retrieve owner of GeneNFT
        address geneNFTOwner = geneNFTToken.ownerOf(geneNFTTokenID);
        require(
            geneNFTOwner != address(0),
            "PCSPReward: not found owner of GeneNFT"
        );
        require(
            config.checkActiveRiskOfGettingStroke(riskOfGettingStroke),
            "PCSPReward: risk of getting stroke value is invalid"
        );

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
