#!/usr/bin/python3
import pytest
import brownie
from brownie import accounts, AdvocateReward


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_configuration_address__owner_make_txn(advocate_deployment):
    # Arranges
    advocate_reward_owner = advocate_deployment['advocate_reward_owner']
    advocate_reward_contract = advocate_deployment['advocate_reward_contract']
    new_configuration = accounts.add()

    old_configuration = advocate_reward_contract.getAddressOfConfiguration()

    # Actions
    txn = advocate_reward_contract.setAddressOfConfiguration(
        new_configuration, {"from": advocate_reward_owner}
    )

    # Assert: SetAddressOfConfiguration Event
    assert ('SetAddressOfConfiguration' in txn.events) is True
    assert txn.events['SetAddressOfConfiguration']['oldAddress'] == old_configuration
    assert txn.events['SetAddressOfConfiguration']['newAddress'] == new_configuration

    # Assert
    assert advocate_reward_contract.getAddressOfConfiguration() == new_configuration


def test_success__set_configuration_address__not_owner_make_txn(advocate_deployment):
    # Arranges
    advocate_reward_owner_fake = accounts.add()
    advocate_reward_contract = advocate_deployment['advocate_reward_contract']
    advocate_reward_configuration_contract = advocate_deployment['advocate_reward_configuration_contract']
    new_advocate_configuration = accounts.add()

    # Assert before actions
    assert advocate_reward_contract.getAddressOfConfiguration() == advocate_reward_configuration_contract

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        advocate_reward_contract.setAddressOfConfiguration(
            new_advocate_configuration, {"from": advocate_reward_owner_fake}
        )

    # Assert
    assert advocate_reward_contract.getAddressOfConfiguration() == advocate_reward_configuration_contract


def test_success__set_configuration_address__new_configuration_null(advocate_deployment):
    # Arranges
    advocate_reward_owner = advocate_deployment['advocate_reward_owner']
    advocate_reward_contract = advocate_deployment['advocate_reward_contract']
    advocate_reward_configuration_contract = advocate_deployment['advocate_reward_configuration_contract']
    new_advocate_configuration = "0x0000000000000000000000000000000000000000"

    # Assert before actions
    assert advocate_reward_contract.getAddressOfConfiguration() == advocate_reward_configuration_contract

    # Actions
    with brownie.reverts("AdvocateReward: address of configuration must not be null"):
        advocate_reward_contract.setAddressOfConfiguration(
            new_advocate_configuration, {"from": advocate_reward_owner}
        )

    # Assert
    assert advocate_reward_contract.getAddressOfConfiguration() == advocate_reward_configuration_contract


def test_success__set_configuration_address__new_and_old_configuration_identical(advocate_deployment):
    # Arranges
    advocate_reward_owner = advocate_deployment['advocate_reward_owner']
    advocate_reward_contract = advocate_deployment['advocate_reward_contract']
    advocate_reward_configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Assert before actions
    assert advocate_reward_contract.getAddressOfConfiguration() == advocate_reward_configuration_contract

    # Actions
    with brownie.reverts("AdvocateReward: address of configuration existed"):
        advocate_reward_contract.setAddressOfConfiguration(
            advocate_reward_configuration_contract, {"from": advocate_reward_owner}
        )

    # Assert
    assert advocate_reward_contract.getAddressOfConfiguration() == advocate_reward_configuration_contract
