// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/IGNFTToken.sol";
import "../interfaces/ILIFEToken.sol";
import "../interfaces/IContractRegistry.sol";


contract GNFTToken is ERC721, Ownable, IGNFTToken {

    IContractRegistry public registry;
    // Mapping: genetic Profile Id => minted or not
    mapping(string => bool) mintedGeneticProfiles;
    uint256 private _totalGeneticData;

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
        public override onlyOwner
    {
        // Mint a new GNFT token for genetic owner
        _safeMint(geneticProfileOwner, geneticDataId);
        // increase total genetic data by one
        _totalGeneticData += 1;

        // only mint LIFE token once per genetic Profile Id
        if (!mintedGeneticProfiles[geneticProfileId]){
            // track genetic profile that was minted G-NFT
            mintedGeneticProfiles[geneticProfileId] = true;
            // When a new G-NFT Token is minted => some of LIFE token also are minted
            ILIFEToken lifeToken = ILIFEToken(registry.getContractAddress('LIFEToken'));
            lifeToken.mintLIFE(geneticProfileId, geneticDataId);
        }

        emit MintGNFT(geneticProfileOwner, geneticProfileId, geneticDataId);
    }

    function burnGNFT(uint256 geneticDataId) public override onlyOwner {
        // require genetic profile id must exist
        require(_exists(geneticDataId), "GNFTToken: genetic profile id must exist for burning");
        // Perform burning the genetic profile id
        _burn(geneticDataId);

        // decrease total genetic profiles by one
        _totalGeneticData -= 1;

        emit BurnGNFT(geneticDataId);
    }

    function getTotalGeneticData() external view override returns (uint256) {
        return _totalGeneticData;
    }

}
