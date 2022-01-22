#!/usr/bin/python3

import pytest

from brownie import (
    accounts,
    ContractRegistry,
    GNFTToken,
    LIFEToken,
    LIFETreasury,
)

from constants import ContractName


class Constant(ContractName):
    GFN_DEPLOYER = 'gfn_deployer'
    GFN_OWNER1 = 'gfn_owner1'
    GFN_OWNER2 = 'gfn_owner2'


@pytest.fixture(scope="module")
def const():
    return Constant


@pytest.fixture(scope="module")
def deployment():
    gfn_deployer = accounts[0]
    gfn_owner1 = accounts[1]
    gfn_owner2 = accounts[2]

    # deploy smart contracts and get instance of them
    registry = ContractRegistry.deploy(gfn_owner1, {'from': gfn_deployer})
    gnft_token = GNFTToken.deploy(gfn_owner1, registry, "GNFT", "GNFT", {'from': gfn_deployer})
    life_token = LIFEToken.deploy(gfn_owner1, registry, "LIFE", "LIFE", {'from': gfn_deployer})
    life_treasury = LIFETreasury.deploy([gfn_owner1, gfn_owner2], 2, {'from': gfn_deployer})

    # add deployed smart contracts to ContractRegistry
    registry.registerContract(Constant.GNFT_TOKEN, gnft_token.address, {'from': gfn_owner1})
    registry.registerContract(Constant.LIFE_TOKEN, life_token.address, {'from': gfn_owner1})
    registry.registerContract(Constant.LIFE_TREASURY, life_treasury.address, {'from': gfn_owner1})

    results = {
        Constant.GFN_DEPLOYER: gfn_deployer,
        Constant.GFN_OWNER1: gfn_owner1,
        Constant.GFN_OWNER2: gfn_owner2,
        Constant.REGISTRY: registry,
        Constant.GNFT_TOKEN: gnft_token,
        Constant.LIFE_TOKEN: life_token,
        Constant.LIFE_TREASURY: life_treasury,
    }

    return results
