// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "../interfaces/IContractRegistry.sol";


abstract contract RevenueSharingArrangementRetriever {

    function _getRevenueSharingArrangementAddress(
        IContractRegistry registry
    )
        internal view returns (address)
    {
        return registry.getContractAddress('RevenueSharingArrangement');
    }

}
