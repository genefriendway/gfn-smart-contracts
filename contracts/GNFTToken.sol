// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/IGNFTToken.sol";
import "./interfaces/ILIFEToken.sol";
import "./interfaces/IContractRegistry.sol";
import "./mixins/LIFETokenRetriever.sol";


contract GNFTToken is ERC721, Ownable, IGNFTToken, LIFETokenRetriever{

    IContractRegistry public registry;
    // Mapping: genetic Profile Id => ever minted or not
    // This mapping tracks genetic profile of Customer that has been ever minted
    // this mapping only incrementally
    mapping(string => bool) mintedGeneticProfiles;
    uint256 private _totalMintedGeneticProfiles;

    // Total number of current tokens that will be changed when minting or burning
    uint256 private _totalCurrentTokens;

    // ===== Modifiers =======
    modifier notNullGeneticProfileId(string memory geneticProfileId) {
        require(
            bytes(geneticProfileId).length > 0,
            "GNFTToken: genetic profile id must not be null"
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
        string memory geneticProfileId,
        uint256 geneticDataId
    )
        public
        override
        onlyOwner
        notNullGeneticProfileId(geneticProfileId)
    {
        // Mint a new G-NFT token for genetic profile owner
        _safeMint(geneticProfileOwner, geneticDataId);
        // increase total current tokens by one
        _totalCurrentTokens += 1;

        // only mint LIFE token once per genetic profile id
        if (!mintedGeneticProfiles[geneticProfileId]){
            // increase total minted genetic profiles by one
            _totalMintedGeneticProfiles += 1;
            // track genetic profile that was minted G-NFT
            mintedGeneticProfiles[geneticProfileId] = true;
            // When a new G-NFT Token is minted => some of LIFE token also are minted
            ILIFEToken lifeToken = ILIFEToken(_getLIFETokenAddress(registry));
            lifeToken.mintLIFE(geneticProfileId, geneticDataId);
        }

        emit MintGNFT(geneticProfileOwner, geneticProfileId, geneticDataId);
    }

    function burnGNFT(uint256 geneticDataId) public override onlyOwner {
        // require geneticDataId must exist
        require(
            _exists(geneticDataId),
            "GNFTToken: genetic data id must exist for burning"
        );
        // Perform burning the genetic data id
        _burn(geneticDataId);
        // decrease total current tokens by one
        _totalCurrentTokens -= 1;

        emit BurnGNFT(geneticDataId);
    }

    function getTotalMintedGeneticProfiles() external view override returns (uint256) {
        return _totalMintedGeneticProfiles;
    }

    function getTotalCurrentTokens() external view override returns (uint256) {
        return _totalCurrentTokens;
    }

}
