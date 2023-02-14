#!/usr/bin/python3

import pytest

from brownie import accounts, GenomicDAOToken, TokenWallet


@pytest.fixture(scope="module")
def token_wallet_deployment():
    deployer = accounts[0]
    dao_token_owner = accounts[1]
    token_wallet_owner = accounts[2]
    token_wallet_operator = accounts.add()
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

    # set operator
    token_wallet.addOperator(token_wallet_operator, {"from": token_wallet_owner})

    results = {
        'dao_token': dao_token,
        'dao_token_owner': dao_token_owner,
        'token_wallet': token_wallet,
        'token_wallet_owner': token_wallet_owner,
        'token_wallet_operator': token_wallet_operator,
    }

    return results
