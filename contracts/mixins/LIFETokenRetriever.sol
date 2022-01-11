// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "../interfaces/IContractRegistry.sol";


abstract contract LIFETokenRetriever {

    function _getLIFETokenAddress(
        IContractRegistry registry
    )
        internal view returns (address)
    {
        return registry.getContractAddress('LIFEToken');
    }

}
