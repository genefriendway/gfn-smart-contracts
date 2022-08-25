// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../interfaces/IIncentiveConfiguration.sol";


contract IncentiveConfiguration is IIncentiveConfiguration, Ownable {

    // State Variables
    address private _geneNFTAddress;

    // Mapping: risk of getting stroke => percentage of reward
    mapping(uint256 => uint256) private customerRewardRatios;

    // Modifiers
    modifier validGeneNFTAddress(address _address) {
         require(
            _geneNFTAddress == address(0),
            "IncentiveConfiguration: address of GeneNFT is configured and can not change anymore"
        );
        require(
            _address != address(0),
            "IncentiveConfiguration: address of GeneNFT must not be null"
        );
        _;
    }

    constructor(
        address owner,
        address incentiveConfiguration
    ) {
        setIncentiveConfiguration(incentiveConfiguration);
        transferOwnership(owner);
    }

    function setDefaultCustomerRewardRatio() private {
        customerRewardRatios[1] = 1000;
        customerRewardRatios[3] = 200;
        customerRewardRatios[16] = 15;
        customerRewardRatios[80] = 2;
    }

    function updateCustomerRewardRatio(
        uint256 riskOfGettingStroke,
        uint256 percentageOfReward
    )
        external
        onlyOwner
    {
        require(
            riskOfGettingStroke > 0,
            "IncentiveConfiguration: risk of getting stroke must be greater zero"
        );
        require(
            percentageOfReward > 0,
            "IncentiveConfiguration: percentage of reward must be greater zero"
        );

        customerRewardRatios[riskOfGettingStroke] = percentageOfReward;
        emit UpdateCustomerRewardRatio(riskOfGettingStroke, percentageOfReward);
    }

    function getCustomerRewardPercentage(
        uint256 riskOfGettingStroke
    )
        external override view returns (uint256)
    {
        return customerRewardRatios[riskOfGettingStroke];
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

}
