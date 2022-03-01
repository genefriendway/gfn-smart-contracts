// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";

import "./interfaces/IContractRegistry.sol";
import "./interfaces/IDataUtilization.sol";
import "./interfaces/IRevenueSharingArrangement.sol";
import "./mixins/RevenueSharingArrangementRetriever.sol";


contract DataUtilization is
    Ownable,
    IDataUtilization,
    RevenueSharingArrangementRetriever
{

    IContractRegistry public registry;

    constructor(address gfnOwner, IContractRegistry _registry) {
        registry = _registry;
        transferOwnership(gfnOwner);
    }

    function payToAccess(
        address fromParticipantWallet,
        address fromSender,
        uint256[] memory receivedTokenIds,
        uint256[] memory receivedLIFEAmounts
    )
        external onlyOwner
    {
        require(
            receivedTokenIds.length == receivedLIFEAmounts.length,
            "DataUtilization: received token ids and received LIFE amounts must be same length"
        );
        IRevenueSharingArrangement revenueSharing = IRevenueSharingArrangement(
            _getRevenueSharingArrangementAddress(registry)
        );

        for (uint256 index = 0; index < receivedTokenIds.length; index++) {
            revenueSharing.distributeRevenue(
                fromParticipantWallet,
                fromSender,
                receivedTokenIds[index],
                receivedLIFEAmounts[index]
            );
        }
        emit PayToAccess(
            fromParticipantWallet,
            fromSender,
            receivedTokenIds,
            receivedLIFEAmounts
        );
    }

}
