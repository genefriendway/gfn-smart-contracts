// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/IContractRegistry.sol";
import "./interfaces/IConfiguration.sol";


contract Configuration is Ownable, IConfiguration {

    IContractRegistry public registry;

    // ==== START - Properties for G-NFT TokenURI ==========
    string private baseGNFTTokenURI = "";
    // ==== END - Properties for G-NFT TokenURI ==========
    
    // ==== START - Properties for mintting LIFE TOKEN ==========
    struct GNFTRange {
        uint256 lower;
        uint256 upper;
        uint256 numberOfLIFEToMint;
    }
    // Mapping from index to GNFTRange
    mapping(uint256 => GNFTRange) private tableOfMintingLIFE;
    uint256 private totalGNFTRanges = 18;
    // ==== END - Properties for mintting LIFE TOKEN ==========


    constructor(address gfnOwner, IContractRegistry _registry) {
        registry = _registry;
        _initializeTableOfMintingLIFE();
        transferOwnership(gfnOwner);
    }

    function setBaseGNFTTokenURI(
        string memory uri
    ) external onlyOwner {
        require(
            bytes(uri).length > 0,
            "Configuration: base G-NFT token URI must be not empty"
        );
        baseGNFTTokenURI = uri;

        emit SetBaseGNFTTokenURI(uri);
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



}