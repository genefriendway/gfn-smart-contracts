#!/usr/bin/python3

import pytest

from brownie import accounts, GenomicDAOToken, TokenWallet


@pytest.fixture(scope="module")
def token_wallet_deployment():
    deployer = accounts[0]
    dao_token_owner = accounts[1]
    token_wallet_owner = accounts[2]
    cap = 1000000000 * 10**18  # one billion

    # deploy smart contract GenomicDAOToken
    dao_token = GenomicDAOToken.deploy(
        dao_token_owner,
        "Token Name",
        "TOKEN",
        cap,
        {"from": deployer}
    )
    dao_token.mint(
        dao_token_owner, 100000000 * 10**18, {"from": dao_token_owner}
    )

    # deploy smart contract TokenWallet
    token_wallet = TokenWallet.deploy(
        token_wallet_owner,
        dao_token.address,
        {"from": deployer}
    )

    results = {
        'dao_token': dao_token,
        'dao_token_owner': dao_token_owner,
        'token_wallet': token_wallet,
        'token_wallet_owner': token_wallet_owner,
    }

    return results
