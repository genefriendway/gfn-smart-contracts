#!/usr/bin/python3

import pytest

from brownie import accounts, GenomicDAOToken


@pytest.fixture(scope="module")
def zero_address():
    return "0x0000000000000000000000000000000000000000"


@pytest.fixture(scope="module")
def dao_deployment():
    deployer = accounts[0]
    owner = accounts[1]
    cap = 1000000000

    # deploy smart contracts and get instance of them
    dao_token = GenomicDAOToken.deploy(
        owner,
        "Post-Covid-Stroke Prevention",
        "PCSP",
        cap,
        {"from": deployer}
    )

    dao_token.mint(owner, 1000, {"from": owner})

    results = {
        'dao_token': dao_token,
        'owner': owner,
        'cap': cap
    }

    return results
