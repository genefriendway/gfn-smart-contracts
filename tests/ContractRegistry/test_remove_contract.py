#!/usr/bin/python3
import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.fixture(scope="function")
def setup(registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]
    gnft_token = registry_deployment[const.GNFT_TOKEN]

    # Actions
    registry.registerContract('ValidName', gnft_token.address, {"from": gfn_owner1})


def test_success__remove_contract(setup, registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]
    gnft_token = registry_deployment[const.GNFT_TOKEN]

    # Asserts: before removing Contract
    gnft_address = registry.getContractAddress('ValidName')
    gnft_name = registry.getContractName(gnft_token.address)
    assert gnft_address == gnft_token.address
    assert gnft_name == 'ValidName'

    # Actions
    tx = registry.removeContract(
        'ValidName', gnft_token.address, {"from": gfn_owner1}
    )

    # Assert: RegisterContract Event
    assert ('RemoveContract' in tx.events) is True
    assert tx.events['RemoveContract']['name'] == 'ValidName'
    assert tx.events['RemoveContract']['_address'] == gnft_token.address

    # Asserts: after removing Contract
    gnft_address = registry.getContractAddress('ValidName')
    gnft_name = registry.getContractName(gnft_token.address)
    assert gnft_address == '0x0000000000000000000000000000000000000000'
    assert gnft_name == ''


def test_failure__remove_contract__empty_contract_name(setup, registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]
    gnft_token = registry_deployment[const.GNFT_TOKEN]

    # Actions
    with brownie.reverts('ContractRegistry: contract name must not be empty'):
        registry.removeContract(
            '', gnft_token.address, {"from": gfn_owner1}
        )


def test_failure__remove_contract__not_existed_name(registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]
    gnft_token = registry_deployment[const.GNFT_TOKEN]

    # Actions
    with brownie.reverts('ContractRegistry: contract name is not registered'):
        registry.removeContract(
            'InvalidName', gnft_token.address, {"from": gfn_owner1}
        )


def test_failure__remove_contract__empty_contract_address(setup, registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]

    # Actions
    with brownie.reverts('ContractRegistry: contract address is invalid'):
        registry.removeContract(
            'ValidName', '0x0000000000000000000000000000000000000000', {"from": gfn_owner1}
        )


def test_failure__remove_contract__not_existed_address(setup, registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]
    life_token = registry_deployment[const.LIFE_TOKEN]

    # Actions
    with brownie.reverts('ContractRegistry: contract address is not registered'):
        registry.removeContract(
            'ValidName', life_token.address, {"from": gfn_owner1}
        )


def test_failure__remove_contract__not_owner_make_transaction(
        setup, registry_deployment, const
):
    # Arranges
    registry = registry_deployment[const.REGISTRY]
    gnft_token = registry_deployment[const.GNFT_TOKEN]

    fake_owner = accounts.add()

    # Actions
    with brownie.reverts('Ownable: caller is not the owner'):
        registry.removeContract(
            'ValidName', gnft_token.address, {"from": fake_owner}
        )
