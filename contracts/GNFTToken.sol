// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/IGNFTToken.sol";
import "../interfaces/ILIFEToken.sol";
import "../interfaces/IContractRegistry.sol";


contract GNFTToken is ERC721, Ownable, IGNFTToken {

    IContractRegistry public registry;
    uint256 private _totalTokens;

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

    function mintToken(
        address geneticOwner,
        uint256 tokenId
    )
        public override onlyOwner
    {
        // Each genetic owner has only one GNFT token
        require(
            balanceOf(geneticOwner) == 0,
            "GNFTToken: genetic owner had GNFT token."
        );
        // Mint a new GNFT token for genetic owner
        _safeMint(geneticOwner, tokenId);
        // increase total tokens by one
        _totalTokens += 1;
        // When a new GNFT Token is minted => some of LIFE token also are minted
        ILIFEToken lifeToken = ILIFEToken(registry.getContractAddress('LIFEToken'));
        lifeToken.mintLIFEToTreasury(tokenId);

        emit MintToken(geneticOwner, tokenId);
    }

    function burnToken(uint256 tokenId) public override onlyOwner {
        // require Token Id must exist
        require(_exists(tokenId), "GNFTToken: token id must exist for burning");
        // Perform burning the token id
        _burn(tokenId);

        // increase total tokens by one
        _totalTokens -= 1;

        emit BurnToken(tokenId);
    }

    function getTotalTokens() external view override returns (uint256) {
        return _totalTokens;
    }

}
