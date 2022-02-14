// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "../interfaces/IContractRegistry.sol";


abstract contract LabServiceProviderWalletRetriever {

    function _getLIFETreasuryAddress(
        IContractRegistry registry
    )
        internal view returns (address)
    {
        return registry.getContractAddress('LabServiceProviderWallet');
    }

}
