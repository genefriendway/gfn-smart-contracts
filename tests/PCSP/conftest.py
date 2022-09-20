#!/usr/bin/python3

import pytest

from brownie import accounts, PCSPConfiguration, PCSPReward


@pytest.fixture(scope="module")
def pcsp_deployment():
    deployer = accounts[0]
    pcsp_reward_owner = accounts[1]
    pcsp_configuration_owner = accounts[2]

    # deploy smart contracts and get instance of them
    pcsp_configuration_contract = PCSPConfiguration.deploy(
        pcsp_configuration_owner,
        {"from": deployer}
    )

    pcsp_reward_contract = PCSPReward.deploy(
        pcsp_reward_owner,
        pcsp_configuration_contract.address,
        {"from": deployer}
    )

    results = {
        'pcsp_reward_owner': pcsp_reward_owner,
        'pcsp_reward_contract': pcsp_reward_contract,
        'pcsp_configuration_owner': pcsp_configuration_owner,
        'pcsp_configuration_contract': pcsp_configuration_contract,
    }

    return results
