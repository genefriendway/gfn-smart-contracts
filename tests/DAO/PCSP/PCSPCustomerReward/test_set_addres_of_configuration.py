#!/usr/bin/python3
import pytest
import brownie
from brownie import accounts, PCSPCustomerReward


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_pcsp_configuration__owner_make_txn(pcsp_deployment):
    # Arranges
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    new_pcsp_configuration = accounts.add()

    old_pcsp_configuration = pcsp_reward_contract.getAddressOfConfiguration()

    # Actions
    txn = pcsp_reward_contract.setAddressOfConfiguration(
        new_pcsp_configuration, {"from": pcsp_reward_owner}
    )

    # Assert: SetAddressOfConfiguration Event
    assert ('SetAddressOfConfiguration' in txn.events) is True
    assert txn.events['SetAddressOfConfiguration']['oldAddress'] == old_pcsp_configuration
    assert txn.events['SetAddressOfConfiguration']['newAddress'] == new_pcsp_configuration

    # Assert
    assert pcsp_reward_contract.getAddressOfConfiguration() == new_pcsp_configuration


def test_success__set_pcsp_configuration__not_owner_make_txn(pcsp_deployment):
    # Arranges
    pcsp_reward_owner_fake = accounts.add()
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_pcsp_configuration = accounts.add()

    # Assert before actions
    assert pcsp_reward_contract.getAddressOfConfiguration() == pcsp_configuration_contract

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        pcsp_reward_contract.setAddressOfConfiguration(
            new_pcsp_configuration, {"from": pcsp_reward_owner_fake}
        )

    # Assert
    assert pcsp_reward_contract.getAddressOfConfiguration() == pcsp_configuration_contract


def test_success__set_pcsp_configuration__new_configuration_null(pcsp_deployment):
    # Arranges
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_pcsp_configuration = "0x0000000000000000000000000000000000000000"

    # Assert before actions
    assert pcsp_reward_contract.getAddressOfConfiguration() == pcsp_configuration_contract

    # Actions
    with brownie.reverts("PCSPCustomerReward: address of configuration must not be null"):
        pcsp_reward_contract.setAddressOfConfiguration(
            new_pcsp_configuration, {"from": pcsp_reward_owner}
        )

    # Assert
    assert pcsp_reward_contract.getAddressOfConfiguration() == pcsp_configuration_contract


def test_success__set_pcsp_configuration__new_and_old_configuration_identical(pcsp_deployment):
    # Arranges
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']

    # Assert before actions
    assert pcsp_reward_contract.getAddressOfConfiguration() == pcsp_configuration_contract

    # Actions
    with brownie.reverts("PCSPCustomerReward: address of configuration existed"):
        pcsp_reward_contract.setAddressOfConfiguration(
            pcsp_configuration_contract, {"from": pcsp_reward_owner}
        )

    # Assert
    assert pcsp_reward_contract.getAddressOfConfiguration() == pcsp_configuration_contract
