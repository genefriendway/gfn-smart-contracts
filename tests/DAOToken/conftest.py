#!/usr/bin/python3

import pytest

from brownie import accounts, DAOToken


@pytest.fixture(scope="module")
def dao_deployment():
    deployer = accounts[0]
    owner = accounts[1]

    # deploy smart contracts and get instance of them
    dao_token = DAOToken.deploy(
        owner,
        "Post-Covid-Stroke Prevention",
        "PCSP",
        1000,
        {"from": deployer}
    )

    results = {
        'dao_token': dao_token,
        'owner': owner
    }

    return results
