#!/usr/bin/python3

import pytest

from brownie import (
    accounts,
    ContractRegistry,
    Configuration,
    GNFTToken,
    LIFEToken,
    LIFETreasury,
    GeneFriendNetworkWallet,
    ParticipantWallet,
    ReservePool,
    RevenueSharingArrangement,
    DataUtilization
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
    configuration = Configuration.deploy(gfn_owner1, registry, {'from': gfn_deployer})
    gnft_token = GNFTToken.deploy(gfn_owner1, registry, "GNFT", "GNFT", {'from': gfn_deployer})
    life_token = LIFEToken.deploy(gfn_owner1, registry, "LIFE", "LIFE", {'from': gfn_deployer})
    life_treasury = LIFETreasury.deploy([gfn_owner1, gfn_owner2], 2, {'from': gfn_deployer})
    # GeneFriendNetwork Wallet
    gfn_wallet = GeneFriendNetworkWallet.deploy(gfn_owner1, registry, {'from': gfn_deployer})
    gfn_sale_wallet = GeneFriendNetworkWallet.deploy(gfn_owner1, registry, {'from': gfn_deployer})
    # GeneProfileOwner Wallet
    gpo_wallet = ParticipantWallet.deploy(gfn_owner1, registry, {'from': gfn_deployer})
    # DataUtilizer Wallet
    du_wallet = ParticipantWallet.deploy(gfn_owner1, registry, {'from': gfn_deployer})
    # Investor Wallet
    investor_wallet = ParticipantWallet.deploy(gfn_owner1, registry, {'from': gfn_deployer})
    # Reserve Pool Wallet
    reserve_pool_wallet = ParticipantWallet.deploy(gfn_owner1, registry, {'from': gfn_deployer})
    reserve_pool = ReservePool.deploy(gfn_owner1, registry, {'from': gfn_deployer})
    revenue_sharing_arrangement = RevenueSharingArrangement.deploy(
        gfn_owner1, registry, {'from': gfn_deployer}
    )
    data_utilization = DataUtilization.deploy(
        gfn_owner1, registry, {'from': gfn_deployer}
    )

    # add deployed smart contracts to ContractRegistry
    registry.registerContract(Constant.CONFIGURATION, configuration.address, {'from': gfn_owner1})
    registry.registerContract(Constant.GNFT_TOKEN, gnft_token.address, {'from': gfn_owner1})
    registry.registerContract(Constant.LIFE_TOKEN, life_token.address, {'from': gfn_owner1})
    registry.registerContract(Constant.LIFE_TREASURY, life_treasury.address, {'from': gfn_owner1})
    registry.registerContract(Constant.GENE_FRIEND_NETWORK_WALLET, gfn_wallet.address, {'from': gfn_owner1})
    registry.registerContract(Constant.GFN_SALE_WALLET, gfn_sale_wallet.address, {'from': gfn_owner1})
    registry.registerContract(Constant.GENETIC_PROFILE_OWNER_WALLET, gpo_wallet.address, {'from': gfn_owner1})
    registry.registerContract(Constant.DATA_UTILIZER_WALLET, du_wallet.address, {'from': gfn_owner1})
    registry.registerContract(Constant.INVESTOR_WALLET, investor_wallet.address, {'from': gfn_owner1})
    registry.registerContract(Constant.RESERVE_POOL_WALLET, reserve_pool_wallet.address, {'from': gfn_owner1})
    registry.registerContract(Constant.RESERVE_POOL, reserve_pool.address, {'from': gfn_owner1})
    registry.registerContract(Constant.REVENUE_SHARING_ARRANGEMENT, revenue_sharing_arrangement.address, {'from': gfn_owner1})
    registry.registerContract(Constant.DATA_UTILIZATION, data_utilization.address, {'from': gfn_owner1})

    results = {
        Constant.GFN_DEPLOYER: gfn_deployer,
        Constant.GFN_OWNER1: gfn_owner1,
        Constant.GFN_OWNER2: gfn_owner2,
        Constant.REGISTRY: registry,
        Constant.CONFIGURATION: configuration,
        Constant.GNFT_TOKEN: gnft_token,
        Constant.LIFE_TOKEN: life_token,
        Constant.LIFE_TREASURY: life_treasury,
        Constant.GENE_FRIEND_NETWORK_WALLET: gfn_wallet,
        Constant.GFN_SALE_WALLET: gfn_sale_wallet,
        Constant.GENETIC_PROFILE_OWNER_WALLET: gpo_wallet,
        Constant.DATA_UTILIZER_WALLET: du_wallet,
        Constant.INVESTOR_WALLET: investor_wallet,
        Constant.RESERVE_POOL_WALLET: reserve_pool_wallet,
        Constant.RESERVE_POOL: reserve_pool,
        Constant.REVENUE_SHARING_ARRANGEMENT: revenue_sharing_arrangement,
        Constant.DATA_UTILIZATION: data_utilization,
    }

    return results
