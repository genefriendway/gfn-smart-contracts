// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "../interfaces/IContractRegistry.sol";


abstract contract ReservePoolRetriever {

    function _getReservePoolAddress(
        IContractRegistry registry
    )
        internal view returns (address)
    {
        return registry.getContractAddress('ReservePool');
    }

}
