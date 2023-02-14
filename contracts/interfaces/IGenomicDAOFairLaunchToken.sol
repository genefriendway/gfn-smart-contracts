// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IGenomicDAOFairLaunchToken is IERC20 {
    function mint(address account, uint256 amount) external;

    function burn(uint256 amount) external;

    function setMaxGasPrice(uint256 maxGasPrice_) external;

    function setTransferFee(
        address to_,
        uint256 buyFee_,
        uint256 sellFee_,
        uint256 normalFee_
    ) external;
}
