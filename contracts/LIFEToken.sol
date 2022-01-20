// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/IContractRegistry.sol";
import "./interfaces/ILIFEToken.sol";
import "./interfaces/IGNFTToken.sol";
import "./mixins/GNFTTokenRetriever.sol";
import "./mixins/LIFETreasuryRetriever.sol";


contract LIFEToken is
    ERC20,
    Ownable,
    ILIFEToken,
    GNFTTokenRetriever,
    LIFETreasuryRetriever
{

    IContractRegistry public registry;

    struct GNFTRange {
        uint256 lower;
        uint256 upper;
        uint256 numerOfLIFEToMint;
    }
    // Mapping from index to GNFTRange
    mapping(uint256 => GNFTRange) private _tableOfMintingLIFE;


    modifier onlyGNFTToken() {
        require(
            _msgSender() == _getGNFTTokenAddress(registry),
            "LIFEToken: caller is not GNFTToken contract"
        );
        _;
    }

    constructor(
        address gfnOwner,
        IContractRegistry _registry,
        string memory name,
        string memory symbol
    ) 
        ERC20(name, symbol) 
    {
        registry = _registry;
        _initializeTableOfMintingLIFE();
        transferOwnership(gfnOwner);
    }

    function findNumberOfLIFEToMint(
        uint256 totalGNFTTokens
    )
        public view returns (uint256)
    {
        uint256 minIndex = 1;
        uint256 maxIndex = 18;
        for(uint256 index = minIndex; index <= maxIndex; index++) {
            GNFTRange storage range = _tableOfMintingLIFE[index];
            if (totalGNFTTokens >= range.lower
                && totalGNFTTokens <= range.upper) {
                return range.numerOfLIFEToMint;
            }
        }
        return 0;
    }

    function mintLIFE(
        string memory geneticProfileId,
        uint256 geneticDataId
    ) external override onlyGNFTToken {
        address lifeTreasuryAddress = _getLIFETreasuryAddress(registry);
        require(
            lifeTreasuryAddress != address(0),
            "LIFEToken: Please register LIFETreasury in ContractRegistry"
        );

        // find number of LIFE to mint base on total Genetic Data
        IGNFTToken gnft_token = IGNFTToken(_getGNFTTokenAddress(registry));
        uint256 totalGeneticData = gnft_token.getTotalMintedGeneticProfiles();
        uint256 numberOfLIFEToMint = findNumberOfLIFEToMint(totalGeneticData);

        if (numberOfLIFEToMint > 0) {
            // Mint new LIFE tokens to LIFETreasury contract
            _mint(lifeTreasuryAddress, numberOfLIFEToMint);

            emit MintLIFE(lifeTreasuryAddress, geneticProfileId, geneticDataId);
        }
    }

    function burnLIFE(uint256 amount) external override {
        address accountToBurn = _msgSender();
        require(
            balanceOf(accountToBurn) >= amount,
            "LIFEToken: burn amount exceeds balance"
        );
        _burn(accountToBurn, amount);
        emit BurnLIFE(accountToBurn, amount);
    }

    function _initializeTableOfMintingLIFE() private {
//        _tableOfMintingLIFE[index] = GNFTRange(lower, upper, number of LIFE);
        _tableOfMintingLIFE[1] = GNFTRange(1, 1, 9*10**25);
        _tableOfMintingLIFE[2] = GNFTRange(2, 10**1, 10**25);
        _tableOfMintingLIFE[3] = GNFTRange(10**1 + 1, 10**2, 10**24);
        _tableOfMintingLIFE[4] = GNFTRange(10**2 + 1, 10**3, 10**23);
        _tableOfMintingLIFE[5] = GNFTRange(10**3 + 1, 10**4, 10**22);
        _tableOfMintingLIFE[6] = GNFTRange(10**4 + 1, 10**5, 10**21);
        _tableOfMintingLIFE[7] = GNFTRange(10**5 + 1, 10**6, 10**20);
        _tableOfMintingLIFE[8] = GNFTRange(10**6 + 1, 10**7, 10**19);
        _tableOfMintingLIFE[9] = GNFTRange(10**7 + 1, 10**8, 10**18);
        _tableOfMintingLIFE[10] = GNFTRange(10**8 + 1, 10**9, 10**17);
        _tableOfMintingLIFE[11] = GNFTRange(10**9 + 1, 10**10, 10**16);
        _tableOfMintingLIFE[12] = GNFTRange(10**10 + 1, 10**11, 10**15);
        _tableOfMintingLIFE[13] = GNFTRange(10**11 + 1, 10**12, 10**14);
        _tableOfMintingLIFE[14] = GNFTRange(10**12 + 1, 10**13, 10**13);
        _tableOfMintingLIFE[15] = GNFTRange(10**13 + 1, 10**14, 10**12);
        _tableOfMintingLIFE[16] = GNFTRange(10**14 + 1, 10**15, 10**11);
        _tableOfMintingLIFE[17] = GNFTRange(10**15 + 1, 10**16, 10**10);
        _tableOfMintingLIFE[18] = GNFTRange(10**16 + 1, 10**17, 10**9);
    }
}
