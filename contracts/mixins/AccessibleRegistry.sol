// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "../interfaces/IContractRegistry.sol";
import "../interfaces/IConfiguration.sol";
import "./ConfigurationRetriever.sol";


abstract contract AccessibleRegistry is ConfigurationRetriever {
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
        return msg.sender == config.getOperator(address(this));
    }
}

