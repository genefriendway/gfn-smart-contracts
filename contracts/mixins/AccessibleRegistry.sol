// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/utils/Context.sol";
import "../interfaces/IContractRegistry.sol";
import "../interfaces/IConfiguration.sol";
import "./ConfigurationRetriever.sol";


abstract contract AccessibleRegistry is
    Context,
    ConfigurationRetriever
{
    IContractRegistry registry;

    modifier onlyOperator() {
        require(
            checkSenderIsOperator(),
            "AccessibleRegistry: caller must be operator"
        );
        _;
    }

    constructor(IContractRegistry _registry) {
        registry = _registry;
    }

    function checkSenderIsOperator() internal view returns (bool) {
        IConfiguration config = IConfiguration(_getConfigurationAddress(registry));
        return _msgSender() == config.getOperator(address(this));
    }
}

