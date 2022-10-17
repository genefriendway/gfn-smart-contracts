#!/usr/bin/python3
import brownie
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


def test_failure__deploy_smart_contract__owner_null():
    deployer = accounts.add()
    token_wallet_owner = "0x0000000000000000000000000000000000000000"
    token_address = accounts.add()

    # deploy smart contract TokenWallet
    with brownie.reverts("TokenWallet: address must not be null"):
        TokenWallet.deploy(
            token_wallet_owner,
            token_address,
            {"from": deployer}
        )


def test_failure__deploy_smart_contract__token_wallet_null():
    deployer = accounts.add()
    token_wallet_owner = accounts.add()
    token_address = "0x0000000000000000000000000000000000000000"

    # deploy smart contract TokenWallet
    with brownie.reverts("TokenWallet: address must not be null"):
        TokenWallet.deploy(
            token_wallet_owner,
            token_address,
            {"from": deployer}
        )
