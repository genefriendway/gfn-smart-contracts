// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Capped.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/IGenomicDAOToken.sol";

contract GenomicDAOToken is IGenomicDAOToken, Ownable, ERC20Capped {
    constructor(
        address owner,
        string memory name,
        string memory symbol,
        uint256 cap
    ) ERC20(name, symbol) ERC20Capped(cap) {
        transferOwnership(owner);
    }

    function mint(address account, uint256 amount) public override onlyOwner {
        _mint(account, amount);
    }

    function burn(uint256 amount) public {
        _burn(_msgSender(), amount);
    }
}
