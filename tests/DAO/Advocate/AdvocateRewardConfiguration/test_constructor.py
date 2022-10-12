#!/usr/bin/python3
import pytest
import brownie
from brownie import accounts, AdvocateRewardConfiguration


def test_success__deploy_smart_contract():
    deployer = accounts[0]
    advocate_reward_configuration_owner = accounts[1]

    # Actions
    advocate_reward_configuration_contract = AdvocateRewardConfiguration.deploy(
        advocate_reward_configuration_owner,
        {"from": deployer}
    )

    # Todo: Assert default settings


def test_failure__deploy_smart_contract__null_owner():
    deployer = accounts[0]
    advocate_reward_configuration_owner = "0x0000000000000000000000000000000000000000"

    # Actions
    with brownie.reverts("Ownable: new owner is the zero address"):
        AdvocateRewardConfiguration.deploy(
            advocate_reward_configuration_owner,
            {"from": deployer}
        )


def test_failure__deploy_smart_contract__owner_is_not_adddress_type():
    deployer = accounts[0]
    advocate_reward_configuration_owner = "Hello_Address"

    # Actions
    with pytest.raises(ValueError):
        AdvocateRewardConfiguration.deploy(
            advocate_reward_configuration_owner,
            {"from": deployer}
        )
