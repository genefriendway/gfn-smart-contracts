// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/IDAOToken.sol";



contract DAOToken is IDAOToken, Ownable, ERC20Burnable
{

    constructor(
        address owner,
        string memory name,
        string memory symbol,
        uint256 fixedTotalSupply
    )
        ERC20(name, symbol)
    {
        _mint(owner, fixedTotalSupply);
        transferOwnership(owner);
    }
}
