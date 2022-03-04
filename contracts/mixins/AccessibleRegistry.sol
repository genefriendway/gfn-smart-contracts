// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "../interfaces/IContractRegistry.sol";


abstract contract AccessibleRegistry {
    IContractRegistry registry;

    modifier onlyGFNOperator() {
        require(
            checkSenderIsGFNOperator(),
            "AccessibleRegistry: caller must be GFN Operator"
        );
        _;
    }

    constructor(IContractRegistry _registry) {
        registry = _registry;
    }

    function checkSenderIsGFNOperator() internal view returns (bool) {
        return msg.sender == registry.getGFNOperator(address(this));
    }
}

