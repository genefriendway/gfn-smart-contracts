// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/IGNFTToken.sol";
import "./interfaces/ILIFEToken.sol";
import "./interfaces/IContractRegistry.sol";
import "./mixins/LIFETokenRetriever.sol";
import "./mixins/LIFETreasuryRetriever.sol";


contract GNFTToken is
    Ownable,
    ERC721Enumerable,
    IGNFTToken, 
    LIFETokenRetriever,
    LIFETreasuryRetriever
{

    IContractRegistry public registry;
    // Mapping: genetic Profile Id => ever minted or not
    // This mapping tracks genetic profile of Customer that has been ever minted
    // this mapping only incrementally
    mapping(uint256 => bool) private _mintedGeneticProfiles;
    uint256 private _totalMintedGeneticProfiles;

    // ===== Modifiers =======
    modifier existLIFEToken() {
        address lifeTokenAddress = _getLIFETokenAddress(registry);
        require(
            lifeTokenAddress != address(0),
            "GNFTToken: Please register LIFEToken on ContractRegistry"
        );
        _;
    }

    // ===== Modifiers =======
    modifier existLIFETreasury() {
        address lifeTreasuryAddress = _getLIFETreasuryAddress(registry);
        require(
            lifeTreasuryAddress != address(0),
            "GNFTToken: Please register LIFETreasury on ContractRegistry"
        );
        _;
    }

    constructor(
        address gfnOwner,
        IContractRegistry _registry,
        string memory name,
        string memory symbol
    )
        ERC721(name, symbol)
    {
        registry = _registry;
        transferOwnership(gfnOwner);
    }

    function mintGNFT(
        address geneticProfileOwner,
        uint256 geneticProfileId
    )
        public
        override
        onlyOwner
        existLIFEToken
        existLIFETreasury
    {
        // Mint a new G-NFT token for genetic profile owner
        _safeMint(geneticProfileOwner, geneticProfileId);

        // only mint LIFE token once per genetic profile id
        if (!_mintedGeneticProfiles[geneticProfileId]){
            // increase total minted genetic profiles by one
            _totalMintedGeneticProfiles += 1;
            // track genetic profile that was minted G-NFT
            _mintedGeneticProfiles[geneticProfileId] = true;
            // When a new G-NFT Token is minted => some of LIFE token also are minted
            ILIFEToken lifeToken = ILIFEToken(_getLIFETokenAddress(registry));
            lifeToken.mintLIFE(geneticProfileId);
        }

        emit MintGNFT(geneticProfileOwner, geneticProfileId);
    }

    function mintBatchGNFT(
        address[] memory geneticProfileOwners,
        uint256[] memory geneticProfileIds
    )
        public
        override
        onlyOwner
        existLIFEToken
        existLIFETreasury
    {
        for (uint256 i = 0; i < geneticProfileOwners.length; i++) {
            mintGNFT(geneticProfileOwners[i], geneticProfileIds[i]);
        }
        emit MintBatchGNFT(geneticProfileOwners, geneticProfileIds);
    }

    function burnGNFT(uint256 geneticProfileId) public override onlyOwner {
        // require geneticProfileId must exist
        require(
            _exists(geneticProfileId),
            "GNFTToken: genetic profile id must exist for burning"
        );
        // Perform burning the genetic profile id
        _burn(geneticProfileId);

        emit BurnGNFT(geneticProfileId);
    }

    function getTotalMintedGeneticProfiles() external view override returns (uint256) {
        return _totalMintedGeneticProfiles;
    }
}
