#!/usr/bin/python3

import pytest

from brownie import accounts, GenomicDAOToken, LIFE2GenomicDAOToken


@pytest.fixture(scope="module")
def life_2_genomic_dao_token_deployment(deployment, const):
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

    # Deploy LIFE2GenomicDAOToken contract
    life_2_genomic_dao_token = LIFE2GenomicDAOToken.deploy(
        owner,
        life_token.address,
        dao_token.address,
        reserve,
        {"from": deployer}
    )

    # Transfer LIFE to contract
    life_token.transfer(
        life_2_genomic_dao_token.address,
        100,
        {"from": life_holder}
    )

    # Allow contract to use genomic dao token
    dao_token.approve(
        life_2_genomic_dao_token.address,
        100,
        {"from": dao_token_holder}
    )

    results = {
        'dao_token': dao_token,
        'life_token': life_token,
        'life_2_genomic_dao_token': life_2_genomic_dao_token,
        'owner': owner,
        'reserve': reserve,
        'dao_token_holder': dao_token_holder
    }

    return results
