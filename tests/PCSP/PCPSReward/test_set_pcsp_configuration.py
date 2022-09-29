#!/usr/bin/python3
import pytest
import brownie
from brownie import accounts, PCSPReward


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_pcsp_configuration__owner_make_txn(pcsp_deployment):
    # Arranges
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    new_pcsp_configuration = accounts.add()

    old_pcsp_configuration = pcsp_reward_contract.getPCSPConfiguration()

    # Actions
    txn = pcsp_reward_contract.setPCSPConfiguration(
        new_pcsp_configuration, {"from": pcsp_reward_owner}
    )

    # Assert: SetPCSPConfiguration Event
    assert ('SetPCSPConfiguration' in txn.events) is True
    assert txn.events['SetPCSPConfiguration']['oldPCSPConfiguration'] == old_pcsp_configuration
    assert txn.events['SetPCSPConfiguration']['newPCSPConfiguration'] == new_pcsp_configuration

    # Assert
    assert pcsp_reward_contract.getPCSPConfiguration() == new_pcsp_configuration


def test_success__set_pcsp_configuration__not_owner_make_txn(pcsp_deployment):
    # Arranges
    pcsp_reward_owner_fake = accounts.add()
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_pcsp_configuration = accounts.add()

    # Assert before actions
    assert pcsp_reward_contract.getPCSPConfiguration() == pcsp_configuration_contract

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        pcsp_reward_contract.setPCSPConfiguration(
            new_pcsp_configuration, {"from": pcsp_reward_owner_fake}
        )

    # Assert
    assert pcsp_reward_contract.getPCSPConfiguration() == pcsp_configuration_contract


def test_success__set_pcsp_configuration__new_configuration_null(pcsp_deployment):
    # Arranges
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_pcsp_configuration = "0x0000000000000000000000000000000000000000"

    # Assert before actions
    assert pcsp_reward_contract.getPCSPConfiguration() == pcsp_configuration_contract

    # Actions
    with brownie.reverts("PCSPReward: address of PCSP configuration must not be null"):
        pcsp_reward_contract.setPCSPConfiguration(
            new_pcsp_configuration, {"from": pcsp_reward_owner}
        )

    # Assert
    assert pcsp_reward_contract.getPCSPConfiguration() == pcsp_configuration_contract


def test_success__set_pcsp_configuration__new_and_old_configuration_identical(pcsp_deployment):
    # Arranges
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']

    # Assert before actions
    assert pcsp_reward_contract.getPCSPConfiguration() == pcsp_configuration_contract

    # Actions
    with brownie.reverts("PCSPReward: address of PCSP configuration existed"):
        pcsp_reward_contract.setPCSPConfiguration(
            pcsp_configuration_contract, {"from": pcsp_reward_owner}
        )

    # Assert
    assert pcsp_reward_contract.getPCSPConfiguration() == pcsp_configuration_contract
