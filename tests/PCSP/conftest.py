#!/usr/bin/python3

import pytest

from brownie import (
    accounts,
    PCSPConfiguration,
    PCSPReward,
    GenomicDAOToken,
    TokenWallet
)


@pytest.fixture(scope="module")
def pcsp_deployment():
    deployer = accounts[0]
    pcsp_reward_owner = accounts[1]
    pcsp_configuration_owner = accounts[2]
    dao_token_owner = accounts[3]
    dao_token_cap = 1000000000 * 10 ** 18  # one billion
    token_wallet_owner = accounts.add()

    # Deploy PCSPConfiguration contract
    pcsp_configuration_contract = PCSPConfiguration.deploy(
        pcsp_configuration_owner,
        {"from": deployer}
    )

    # Deploy PCSPReward contract
    pcsp_reward_contract = PCSPReward.deploy(
        pcsp_reward_owner,
        pcsp_configuration_contract.address,
        {"from": deployer}
    )

    # Deploy GenomicDAOToken contract
    dao_token_contract = GenomicDAOToken.deploy(
        dao_token_owner,
        "Token Name",
        "TOKEN",
        dao_token_cap,
        {"from": deployer}
    )
    dao_token_contract.mint(
        dao_token_owner, 100000000 * 10 ** 18, {"from": dao_token_owner}
    )

    # Deploy TokenWallet contract
    token_wallet_contract = TokenWallet.deploy(
        token_wallet_owner,
        dao_token_contract,
        {"from": deployer}
    )

    results = {
        'dao_token_owner': dao_token_owner,
        'dao_token_contract': dao_token_contract,
        'token_wallet_owner': token_wallet_owner,
        'token_wallet_contract': token_wallet_contract,
        'pcsp_reward_owner': pcsp_reward_owner,
        'pcsp_reward_contract': pcsp_reward_contract,
        'pcsp_configuration_owner': pcsp_configuration_owner,
        'pcsp_configuration_contract': pcsp_configuration_contract,
    }

    return results
