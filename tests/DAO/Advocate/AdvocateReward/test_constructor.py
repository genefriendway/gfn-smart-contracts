#!/usr/bin/python3
import pytest
import brownie
from brownie import accounts, AdvocateReward


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__deploy_smart_contract():
    deployer = accounts[0]
    advocate_reward_owner = accounts[1]
    advocate_configuration_address = accounts.add()

    # Actions
    advocate_reward = AdvocateReward.deploy(
        advocate_reward_owner,
        advocate_configuration_address,
        {"from": deployer}
    )

    # Assert Customer Reward Percents
    assert advocate_reward.getAddressOfConfiguration() == advocate_configuration_address
    assert advocate_reward.owner() == advocate_reward_owner


def test_failure__deploy_smart_contract__null_configuration():
    deployer = accounts[0]
    advocate_reward_owner = accounts[1]
    advocate_configuration_address = "0x0000000000000000000000000000000000000000"

    # Actions
    with brownie.reverts("AdvocateReward: address of configuration "
                         "must not be null"):
        # Actions
        AdvocateReward.deploy(
            advocate_reward_owner,
            advocate_configuration_address,
            {"from": deployer}
        )
