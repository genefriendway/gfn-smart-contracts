#!/usr/bin/python3

import pytest

from brownie import accounts, GenomicDAOToken, GenomicDAOToken2LIFE


@pytest.fixture(scope="module")
def genomic_dao_token_2_life_deployment(deployment, const):
    deployer = accounts[0]
    owner = accounts[1]
    life_holder = accounts[2]
    dao_token_holder = accounts[3]
    reserve = accounts.add()  # Create new account

    # deploy dao token smart contracts and get instance of them
    dao_token = GenomicDAOToken.deploy(
        owner,
        "Post-Covid-Stroke Prevention",
        "PCSP",
        1000,
        {"from": deployer}
    )
    dao_token.mint(dao_token_holder, 1000, {"from": owner})

    # Fake life token for testing
    life_token = GenomicDAOToken.deploy(
        owner,
        "LIFE Token",
        "LIFE",
        1000,
        {"from": deployer}
    )
    life_token.mint(life_holder, 1000, {"from": owner})

    # Deploy dao token lock
    genomic_dao_token_2_life = GenomicDAOToken2LIFE.deploy(
        owner,
        dao_token.address,
        life_token.address,
        reserve,
        {"from": deployer}
    )

    # Transfer token contract
    dao_token.transfer(
        genomic_dao_token_2_life.address,
        100,
        {"from": dao_token_holder}
    )

    # Allow contract to use life token
    life_token.approve(
        genomic_dao_token_2_life.address,
        100,
        {"from": life_holder}
    )

    results = {
        'dao_token': dao_token,
        'life_token': life_token,
        'genomic_dao_token_2_life': genomic_dao_token_2_life,
        'owner': owner,
        'reserve': reserve,
        'life_holder': life_holder
    }

    return results
