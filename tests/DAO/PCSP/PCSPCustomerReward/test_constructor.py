#!/usr/bin/python3
import pytest
import brownie
from brownie import accounts, PCSPCustomerReward


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__deploy_smart_contract():
    deployer = accounts[0]
    pcsp_reward_owner = accounts[1]
    pcsp_configuration_address = accounts.add()

    # Actions
    pcsp_reward = PCSPCustomerReward.deploy(
        pcsp_reward_owner,
        pcsp_configuration_address,
        {"from": deployer}
    )

    # Assert Customer Reward Percents
    assert pcsp_reward.getAddressOfConfiguration() == pcsp_configuration_address
    assert pcsp_reward.owner() == pcsp_reward_owner


def test_failure__deploy_smart_contract__null_configuration():
    deployer = accounts[0]
    pcsp_reward_owner = accounts[1]
    pcsp_configuration_address = "0x0000000000000000000000000000000000000000"

    # Actions
    with brownie.reverts("PCSPCustomerReward: address of configuration "
                         "must not be null"):
        # Actions
        PCSPCustomerReward.deploy(
            pcsp_reward_owner,
            pcsp_configuration_address,
            {"from": deployer}
        )
