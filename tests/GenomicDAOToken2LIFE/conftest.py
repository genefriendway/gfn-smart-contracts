#!/usr/bin/python3

import pytest

from brownie import accounts, GenomicDAOToken, GenomicDAOToken2LIFE


@pytest.fixture(scope="module")
def dao_token_lock_deployment(deployment, const):
    deployer = accounts[0]
    owner = accounts[1]

    # deploy dao token smart contracts and get instance of them
    dao_token = GenomicDAOToken.deploy(
        owner,
        "Post-Covid-Stroke Prevention",
        "PCSP",
        1000,
        {"from": deployer}
    )
    dao_token.mint(owner, 1000, {"from": owner})

    # Fake life token for testing
    life_token = GenomicDAOToken.deploy(
        owner,
        "LIFE Token",
        "LIFE",
        1000,
        {"from": deployer}
    )
    life_token.mint(owner, 1000, {"from": owner})

    # Deploy dao token lock
    dao_token_lock = GenomicDAOToken2LIFE.deploy(
        owner,
        life_token.address,
        dao_token.address,
        {"from": deployer}
    )

    # Transfer token to lock
    dao_token.transfer(dao_token_lock.address, 100, {"from": owner})
    life_token.transfer(dao_token_lock.address, 100, {"from": owner})

    results = {
        'dao_token': dao_token,
        'life_token': life_token,
        'dao_token_lock': dao_token_lock,
        'owner': owner
    }

    return results
