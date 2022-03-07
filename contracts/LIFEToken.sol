// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./interfaces/IContractRegistry.sol";
import "./interfaces/IConfiguration.sol";
import "./interfaces/ILIFEToken.sol";
import "./interfaces/IGNFTToken.sol";
import "./mixins/GNFTTokenRetriever.sol";
import "./mixins/LIFETreasuryRetriever.sol";
import "./mixins/AccessibleRegistry.sol";


contract LIFEToken is
    ERC20,
    ILIFEToken,
    AccessibleRegistry,
    GNFTTokenRetriever,
    LIFETreasuryRetriever
{

    modifier onlyGNFTToken() {
        require(
            _msgSender() == _getGNFTTokenAddress(registry),
            "LIFEToken: caller is not GNFTToken contract"
        );
        _;
    }

    constructor(
        IContractRegistry _registry,
        string memory name,
        string memory symbol
    )
        AccessibleRegistry(_registry)
        ERC20(name, symbol) 
    {}

    function mintLIFE(uint256 geneticProfileId) external override onlyGNFTToken {
        address lifeTreasuryAddress = _getLIFETreasuryAddress(registry);
        // find total genetic profiles that minted ever
        IGNFTToken gnft_token = IGNFTToken(_getGNFTTokenAddress(registry));
        uint256 totalGeneticProfiles = gnft_token.getTotalMintedGeneticProfiles();

        // find Number of LIFE to mint based on total genetic profiles
        IConfiguration config = IConfiguration(_getConfigurationAddress(registry));
        uint256 numberOfLIFEToMint = config.findNumberOfLIFEToMint(
            totalGeneticProfiles
        );

        if (numberOfLIFEToMint > 0) {
            // Mint new LIFE tokens to LIFETreasury contract
            _mint(lifeTreasuryAddress, numberOfLIFEToMint);

            emit MintLIFE(lifeTreasuryAddress, geneticProfileId);
        }
    }

    function burnLIFE(uint256 amount) external override {
        address accountToBurn = _msgSender();
        _burn(accountToBurn, amount);
        emit BurnLIFE(accountToBurn, amount);
    }

}
