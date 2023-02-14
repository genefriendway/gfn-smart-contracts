import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__deposit__owner_make_txn(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = accounts.add()
    deposit_amount = 100 * 10**18
    deposit_description = "Increase Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0

    # Actions
    txn = token_wallet.deposit(
        account_a,
        deposit_amount,
        deposit_description,
        {"from": token_wallet_owner}
    )

    # Assert: Deposit Event
    assert ('Deposit' in txn.events) is True
    assert txn.events['Deposit']['toAddress'] == account_a
    assert txn.events['Deposit']['amount'] == deposit_amount
    assert txn.events['Deposit']['description'] == deposit_description

    # Asserts
    assert token_wallet.getBalance(account_a) == deposit_amount
    assert token_wallet.getTotalBalance() == deposit_amount


def test_success__deposit__operator_make_txn(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_operator = token_wallet_deployment['token_wallet_operator']
    account_a = accounts.add()
    deposit_amount = 100 * 10**18
    deposit_description = "Increase Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0

    # Actions
    txn = token_wallet.deposit(
        account_a,
        deposit_amount,
        deposit_description,
        {"from": token_wallet_operator}
    )

    # Assert: Deposit Event
    assert ('Deposit' in txn.events) is True
    assert txn.events['Deposit']['toAddress'] == account_a
    assert txn.events['Deposit']['amount'] == deposit_amount
    assert txn.events['Deposit']['description'] == deposit_description

    # Asserts
    assert token_wallet.getBalance(account_a) == deposit_amount
    assert token_wallet.getTotalBalance() == deposit_amount


def test_failure__deposit__not_operator_make_txn(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_invalid_owner = accounts.add()
    account_a = accounts.add()
    deposit_amount = 100 * 10**18
    deposit_description = "Increase Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0

    # Actions
    with brownie.reverts("TokenWallet: caller must be the operator"):
        token_wallet.deposit(
            account_a,
            deposit_amount,
            deposit_description,
            {"from": token_wallet_invalid_owner}
        )

    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0


def test_failure__deposit__receiver_address__null(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = "0x0000000000000000000000000000000000000000"
    deposit_amount = 100 * 10**18
    deposit_description = "Increase Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0

    # Actions
    with brownie.reverts("TokenWallet: address must not be null"):
        token_wallet.deposit(
            account_a,
            deposit_amount,
            deposit_description,
            {"from": token_wallet_owner}
        )

    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0


def test_failure__deposit__amount_is_zero(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = accounts.add()
    deposit_amount = 0
    deposit_description = "Increase Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0

    # Actions
    with brownie.reverts("TokenWallet: amount must be greater than zero"):
        token_wallet.deposit(
            account_a,
            deposit_amount,
            deposit_description,
            {"from": token_wallet_owner}
        )

    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0