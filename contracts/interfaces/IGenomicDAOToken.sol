// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IGenomicDAOToken is IERC20 {
    function mint(address account, uint256 amount) external;

    function burn(uint256 amount) external;
}
