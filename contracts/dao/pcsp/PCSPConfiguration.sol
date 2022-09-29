// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "../../interfaces/pcsp/IPCSPConfiguration.sol";


contract PCSPConfiguration is IPCSPConfiguration, Ownable {

    // State Variables
    address private _geneNFTAddress;
    address private _tokenPCSPWalletAddress;
    
    // Mapping: risk of getting stroke => active or inactive
    mapping(uint256 => bool) private _riskOfGettingStrokeStatuses;
    // Mapping: risk of getting stroke => customer reward percent
    mapping(uint256 => uint256) private _customerRewardPercents;

    // Modifiers
    modifier validGeneNFTAddress(address _address) {
         require(
            _geneNFTAddress == address(0),
            "PCSPConfiguration: address of GeneNFT is configured and can not change anymore"
        );
        require(
            _address != address(0),
            "PCSPConfiguration: address of GeneNFT must not be null"
        );
        _;
    }

    modifier validRiskOfGettingStroke(uint256 _risk) {
         require(
            _risk > 0 ,
            "PCSPConfiguration: risk of getting stroke must be greater than zero"
        );
        require(
            _risk <= 100,
            "PCSPConfiguration: risk of getting stroke must be equal to or less than 100"
        );
        _;
    }

    modifier validRewardPercent(uint256 _rewardPercent) {
         require(
            _rewardPercent > 0 ,
            "PCSPConfiguration: reward percent must be greater than zero"
        );
        _;
    }

    modifier activeRiskOfGettingStroke(uint256 _riskOfGettingStroke) {
         require(
            _riskOfGettingStrokeStatuses[_riskOfGettingStroke],
            "PCSPConfiguration: risk of getting stroke is inactive"
        );
        _;
    }

    constructor(
        address owner
    ) {
        _setDefaultCustomerRewardPercents();
        transferOwnership(owner);
    }

    function _setDefaultCustomerRewardPercents() private {
        _customerRewardPercents[1] = 1000;
        _customerRewardPercents[3] = 200;
        _customerRewardPercents[16] = 15;
        _customerRewardPercents[80] = 2;

        _riskOfGettingStrokeStatuses[1] = true;
        _riskOfGettingStrokeStatuses[3] = true;
        _riskOfGettingStrokeStatuses[16] = true;
        _riskOfGettingStrokeStatuses[80] = true;
    }

    function addCustomerRewardPercent(
        uint256 riskOfGettingStroke,
        uint256 rewardPercent
    )
        external
        onlyOwner
        validRiskOfGettingStroke(riskOfGettingStroke)
        validRewardPercent(rewardPercent)
    {
        _customerRewardPercents[riskOfGettingStroke] = rewardPercent;
        _riskOfGettingStrokeStatuses[riskOfGettingStroke] = true;
        emit AddCustomerRewardPercent(riskOfGettingStroke, rewardPercent);
    }

    function removeCustomerRewardPercent(
        uint256 riskOfGettingStroke
    )
        external
        onlyOwner
        activeRiskOfGettingStroke(riskOfGettingStroke)
    {
        _riskOfGettingStrokeStatuses[riskOfGettingStroke] = false;
        emit RemoveCustomerRewardPercent(riskOfGettingStroke);
    }

    function getCustomerRewardPercent(
        uint256 riskOfGettingStroke
    )
        external
        activeRiskOfGettingStroke(riskOfGettingStroke)
        override view returns (uint256)
    {
        return _customerRewardPercents[riskOfGettingStroke];
    }

    function calculateCustomerReward(
        uint256 riskOfGettingStroke,
        uint256 revenue
    )
        external
        activeRiskOfGettingStroke(riskOfGettingStroke)
        override view returns (uint256)
    {
        return revenue * _customerRewardPercents[riskOfGettingStroke] / 100;
    }

    function checkActiveRiskOfGettingStroke(
        uint256 riskOfGettingStroke
    )
        external
        override view returns (bool)
    {
        return _riskOfGettingStrokeStatuses[riskOfGettingStroke];
    }

    function setGeneNFTAddress(
        address geneNFTAddress
    )
        external
        onlyOwner
        validGeneNFTAddress(geneNFTAddress)
    {
        _geneNFTAddress = geneNFTAddress;
        emit SetGeneNFTAddress(_geneNFTAddress);
    }

    function getGeneNFTAddress() external override view returns (address) {
        return _geneNFTAddress;
    }

    function setTokenPCSPWalletAddress(
        address tokenPCSPWalletAddress
    )
        external
        onlyOwner
    {
        _tokenPCSPWalletAddress = tokenPCSPWalletAddress;
        emit SetTokenPCSPWalletAddress(_tokenPCSPWalletAddress);
    }

    function getTokenPCSPWalletAddress() external override view returns (address) {
        return _tokenPCSPWalletAddress;
    }

}
