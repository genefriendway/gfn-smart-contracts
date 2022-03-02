// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/IGNFTToken.sol";
import "./interfaces/ILIFEToken.sol";
import "./interfaces/IContractRegistry.sol";
import "./interfaces/IConfiguration.sol";
import "./mixins/LIFETokenRetriever.sol";
import "./mixins/LIFETreasuryRetriever.sol";
import "./mixins/ConfigurationRetriever.sol";


contract GNFTToken is
    Ownable,
    ERC721Enumerable,
    IGNFTToken, 
    LIFETokenRetriever,
    LIFETreasuryRetriever,
    ConfigurationRetriever
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

    function _baseURI() internal view override returns (string memory) {
        IConfiguration config = IConfiguration(_getConfigurationAddress(registry));
        return config.getBaseGNFTTokenURI();
    }

    function _mintGNFT(
        address geneticProfileOwner,
        uint256 geneticProfileId,
        bool approvalForGFNOwner
    )
        internal
    {
        // Mint a new G-NFT token for genetic profile owner
        _safeMint(geneticProfileOwner, geneticProfileId);

        // when geneticProfileOwner is not an address that provided by end-user,
        // then approvall for GFN Owner and afterward gfn owner will transfer
        // NFT to end-user again
        if (approvalForGFNOwner) {
            _approve(_msgSender(), geneticProfileId);
        }

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

        emit MintGNFT(geneticProfileOwner, geneticProfileId, approvalForGFNOwner);
    }

    function mintBatchGNFT(
        address[] memory geneticProfileOwners,
        uint256[] memory geneticProfileIds,
        bool approvalForGFNOwner
    )
        external
        override
        onlyOwner
        existLIFEToken
        existLIFETreasury
    {
        require(
            geneticProfileOwners.length == geneticProfileIds.length,
            "GNFTToken: genetic profile owners and genetic profile ids must be same length"
        );
        for (uint256 i = 0; i < geneticProfileOwners.length; i++) {
            _mintGNFT(geneticProfileOwners[i], geneticProfileIds[i], approvalForGFNOwner);
        }
        emit MintBatchGNFT(geneticProfileOwners, geneticProfileIds, approvalForGFNOwner);
    }

    function burnGNFT(uint256 geneticProfileId) external override {
        require(
            _isApprovedOrOwner(_msgSender(), geneticProfileId),
            "GNFTToken: transfer caller is not owner nor approved"
        );
        // Perform burning the genetic profile id
        _burn(geneticProfileId);

        emit BurnGNFT(geneticProfileId);
    }

    function getTotalMintedGeneticProfiles() external view override returns (uint256) {
        return _totalMintedGeneticProfiles;
    }
}
