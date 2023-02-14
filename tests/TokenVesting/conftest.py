#!/usr/bin/python3

import pytest

from brownie import (
    accounts,
    GenomicDAOToken,
    TokenVesting,
)


@pytest.fixture(scope="module")
def vesting_deployment():
    deployer = accounts[0]
    dao_token_owner = accounts[1]
    token_vesting_owner = accounts[2]
    dao_token_cap = 1000000000 * 10 ** 18  # one billion

    # Deploy GenomicDAOToken contract
    dao_token_contract = GenomicDAOToken.deploy(
        dao_token_owner,
        "Token Name",
        "TOKEN",
        dao_token_cap,
        {"from": deployer}
    )
    dao_token_contract.mint(
        dao_token_owner, 100000000 * 10 ** 18, {"from": dao_token_owner}
    )
    token_vesting_contract = TokenVesting.deploy(
        dao_token_contract, token_vesting_owner, {"from": deployer}
    )

    results = {
        'dao_token_owner': dao_token_owner,
        'dao_token_contract': dao_token_contract,
        'token_vesting_owner': token_vesting_owner,
        'token_vesting_contract': token_vesting_contract,
    }

    return results
