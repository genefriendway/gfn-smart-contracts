#!/usr/bin/python3

from brownie import accounts, TokenWallet


def test_success__deploy_smart_contract():
    deployer = accounts.add()
    token_wallet_owner = accounts.add()
    token_address = accounts.add()

    # deploy smart contract TokenWallet
    token_wallet = TokenWallet.deploy(
        token_wallet_owner,
        token_address,
        {"from": deployer}
    )

    # Assert: DecreaseBalance Event
    # Asserts
    assert token_wallet.owner() == token_wallet_owner
    assert token_wallet.checkActiveOperator(token_wallet_owner) is True
