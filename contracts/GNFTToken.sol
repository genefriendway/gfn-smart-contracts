// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/IGNFTToken.sol";
import "../interfaces/ILIFEToken.sol";
import "../interfaces/IContractRegistry.sol";


contract GNFTToken is ERC721, Ownable, IGNFTToken {

    IContractRegistry public registry;
    uint256 private _totalGeneticProfiles;

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
        public override onlyOwner
    {
        // Mint a new GNFT token for genetic owner
        _safeMint(geneticProfileOwner, geneticProfileId);
        // increase total genetic profiles by one
        _totalGeneticProfiles += 1;
        // When a new GNFT Token is minted => some of LIFE token also are minted
        ILIFEToken lifeToken = ILIFEToken(registry.getContractAddress('LIFEToken'));
        lifeToken.mintLIFE(geneticProfileId);

        emit MintGNFT(geneticProfileOwner, geneticProfileId);
    }

    function burnGNFT(uint256 geneticProfileId) public override onlyOwner {
        // require genetic profile id must exist
        require(_exists(geneticProfileId), "GNFTToken: genetic profile id must exist for burning");
        // Perform burning the genetic profile id
        _burn(geneticProfileId);

        // decrease total genetic profiles by one
        _totalGeneticProfiles -= 1;

        emit BurnGNFT(geneticProfileId);
    }

    function getTotalGeneticProfiles() external view override returns (uint256) {
        return _totalGeneticProfiles;
    }

}
