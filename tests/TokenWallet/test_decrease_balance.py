import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


@pytest.fixture
def data_test(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = accounts.add()
    decreasing_amount = 100 * 10**18
    decreasing_description = "Increase Balance of Account A"

    # Actions
    token_wallet.increaseBalance(
        account_a,
        decreasing_amount,
        decreasing_description,
        {"from": token_wallet_owner}
    )

    return {
        'account_a': account_a
    }


def test_success__decrease_balance__owner_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = data_test['account_a']
    decreasing_amount = 5 * 10**18
    decreasing_description = "Decrease Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 100 * 10**18
    assert token_wallet.getTotalBalance() == 100 * 10**18

    # Actions
    txn = token_wallet.decreaseBalance(
        account_a,
        decreasing_amount,
        decreasing_description,
        {"from": token_wallet_owner}
    )

    # Assert: DecreaseBalance Event
    assert ('DecreaseBalance' in txn.events) is True
    assert txn.events['DecreaseBalance']['fromAddress'] == account_a
    assert txn.events['DecreaseBalance']['amount'] == decreasing_amount
    assert txn.events['DecreaseBalance']['description'] == decreasing_description

    # Asserts
    assert token_wallet.getBalance(account_a) == 95 * 10**18
    assert token_wallet.getTotalBalance() == 95 * 10**18


def test_failure__decrease_balance__not_owner_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    account_a = data_test['account_a']
    token_wallet_invalid_owner = accounts.add()
    decreasing_amount = 5 * 10**18
    decreasing_description = "Decrease Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 100 * 10**18
    assert token_wallet.getTotalBalance() == 100 * 10**18

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        token_wallet.decreaseBalance(
            account_a,
            decreasing_amount,
            decreasing_description,
            {"from": token_wallet_invalid_owner}
        )

    assert token_wallet.getBalance(account_a) == 100 * 10**18
    assert token_wallet.getTotalBalance() == 100 * 10**18


def test_failure__decrease_balance__receiver_address__null(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = "0x0000000000000000000000000000000000000000"
    decreasing_amount = 5 * 10**18
    decreasing_description = "Decrease Balance of Account A"

    # Assert before Actions
    assert token_wallet.getTotalBalance() == 100 * 10**18

    # Actions
    with brownie.reverts("TokenWallet: fromAddress must be not null"):
        token_wallet.decreaseBalance(
            account_a,
            decreasing_amount,
            decreasing_description,
            {"from": token_wallet_owner}
        )

    assert token_wallet.getTotalBalance() == 100 * 10**18


def test_failure__decrease_balance__amount_is_zero(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = data_test['account_a']
    decreasing_amount = 0
    decreasing_description = "Decrease Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 100 * 10**18
    assert token_wallet.getTotalBalance() == 100 * 10**18

    # Actions
    with brownie.reverts("TokenWallet: amount must be greater than zero"):
        token_wallet.decreaseBalance(
            account_a,
            decreasing_amount,
            decreasing_description,
            {"from": token_wallet_owner}
        )

    assert token_wallet.getBalance(account_a) == 100 * 10**18
    assert token_wallet.getTotalBalance() == 100 * 10**18


def test_failure__decrease_balance__amount_over_balance(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = data_test['account_a']
    decreasing_amount = 101 * 10**18
    decreasing_description = "Decrease Balance of Account A"

    # Assert before Actions
    assert token_wallet.getBalance(account_a) == 100 * 10**18
    assert token_wallet.getTotalBalance() == 100 * 10**18

    # Actions
    with brownie.reverts("TokenWallet: not enough balance to decrease"):
        token_wallet.decreaseBalance(
            account_a,
            decreasing_amount,
            decreasing_description,
            {"from": token_wallet_owner}
        )

    assert token_wallet.getBalance(account_a) == 100 * 10**18
    assert token_wallet.getTotalBalance() == 100 * 10**18