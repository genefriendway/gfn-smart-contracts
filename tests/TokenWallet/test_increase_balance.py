import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__increase_balance__owner_make_txn(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = accounts.add()
    increasing_amount = 100 * 10**18
    increasing_description = "Increase Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0

    # Actions
    txn = token_wallet.increaseBalance(
        account_a,
        increasing_amount,
        increasing_description,
        {"from": token_wallet_owner}
    )

    # Assert: IncreaseBalance Event
    assert ('IncreaseBalance' in txn.events) is True
    assert txn.events['IncreaseBalance']['toAddress'] == account_a
    assert txn.events['IncreaseBalance']['amount'] == increasing_amount
    assert txn.events['IncreaseBalance']['description'] == increasing_description

    # Asserts
    assert token_wallet.getBalance(account_a) == increasing_amount
    assert token_wallet.getTotalBalance() == increasing_amount


def test_failure__increase_balance__not_owner_make_txn(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_invalid_owner = accounts.add()
    account_a = accounts.add()
    increasing_amount = 100 * 10**18
    increasing_description = "Increase Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0

    # Actions
    with brownie.reverts("TokenWallet: caller must be the operator"):
        token_wallet.increaseBalance(
            account_a,
            increasing_amount,
            increasing_description,
            {"from": token_wallet_invalid_owner}
        )

    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0


def test_failure__increase_balance__receiver_address__null(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = "0x0000000000000000000000000000000000000000"
    increasing_amount = 100 * 10**18
    increasing_description = "Increase Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0

    # Actions
    with brownie.reverts("TokenWallet: toAddress must be not null"):
        token_wallet.increaseBalance(
            account_a,
            increasing_amount,
            increasing_description,
            {"from": token_wallet_owner}
        )

    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0


def test_failure__increase_balance__amount_is_zero(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = accounts.add()
    increasing_amount = 0
    increasing_description = "Increase Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0

    # Actions
    with brownie.reverts("TokenWallet: amount must be greater than zero"):
        token_wallet.increaseBalance(
            account_a,
            increasing_amount,
            increasing_description,
            {"from": token_wallet_owner}
        )

    assert token_wallet.getBalance(account_a) == 0
    assert token_wallet.getTotalBalance() == 0