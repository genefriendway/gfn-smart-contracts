#!/usr/bin/python3

import pytest

from brownie import (
    accounts,
    ContractRegistry,
    GNFTToken,
    LIFEToken,
    LIFETreasury
)


@pytest.fixture(scope="module")
def registry_deployment(const):
    gfn_deployer = accounts[0]
    gfn_owner1 = accounts[1]

    # deploy smart contracts and get instance of them
    registry = ContractRegistry.deploy(gfn_owner1, {"from": gfn_deployer})
    gnft_token = GNFTToken.deploy(registry, "GNFT", "GNFT", {"from": gfn_deployer})
    life_token = LIFEToken.deploy(registry, "LIFE", "LIFE", {"from": gfn_deployer})

    assert registry.owner() == gfn_owner1.address

    results = {
        const.GFN_DEPLOYER: gfn_deployer,
        const.GFN_OWNER1: gfn_owner1,
        const.REGISTRY: registry,
        const.GNFT_TOKEN: gnft_token,
        const.LIFE_TOKEN: life_token,
    }

    return results
