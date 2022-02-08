#!/usr/bin/python3
import pytest
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


def test_success__is_registered_contract(setup, registry_deployment, const):
    # Arranges
    registry = registry_deployment[const.REGISTRY]
    gnft_token = registry_deployment[const.GNFT_TOKEN]
    # Actions and Asserts
    assert registry.isRegisteredContract(gnft_token.address) is True


def test_failure__is_registered_contract__check_contract_address(setup, registry_deployment, const):
    # Arranges
    registry = registry_deployment[const.REGISTRY]
    life_token = registry_deployment[const.LIFE_TOKEN]
    # Actions and Asserts
    assert registry.isRegisteredContract(life_token.address) is False


def test_failure__is_registered_contract__check_user_address(setup, registry_deployment, const):
    # Arranges
    registry = registry_deployment[const.REGISTRY]
    # Actions and Asserts
    assert registry.isRegisteredContract(accounts[5]) is False