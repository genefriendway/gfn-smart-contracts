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
    dao_token = token_wallet_deployment['dao_token']
    dao_token_owner = token_wallet_deployment['dao_token_owner']
    token_wallet = token_wallet_deployment['token_wallet']

    assert dao_token.balanceOf(dao_token_owner) == 100000000 * 10 ** 18

    dao_token.transfer(
        token_wallet,
        200 * 10**18,
        {"from": dao_token_owner}
    )

    assert dao_token.balanceOf(dao_token_owner) == 99999800 * 10 ** 18
    assert dao_token.balanceOf(token_wallet) == 200 * 10 ** 18


def test_success__withdraw__owner_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    dao_token = token_wallet_deployment['dao_token']
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_b = accounts.add()
    withdraw_amount = 5 * 10**18
    withdraw_description = "Withdraw Amount To Account B"

    # Assert before Actions
    assert dao_token.balanceOf(token_wallet) == 200 * 10**18
    assert dao_token.balanceOf(account_b) == 0

    # Actions
    txn = token_wallet.withdraw(
        account_b,
        withdraw_amount,
        withdraw_description,
        {"from": token_wallet_owner}
    )

    # Assert: Withdraw Event
    assert ('Withdraw' in txn.events) is True
    assert txn.events['Withdraw']['toAddress'] == account_b
    assert txn.events['Withdraw']['amount'] == withdraw_amount
    assert txn.events['Withdraw']['description'] == withdraw_description

    # Asserts
    assert dao_token.balanceOf(token_wallet) == 195 * 10 ** 18
    assert dao_token.balanceOf(account_b) == 5 * 10**18


def test_success__withdraw__not_owner_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    dao_token = token_wallet_deployment['dao_token']
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_invalid_owner = accounts.add()
    account_b = accounts.add()
    withdraw_amount = 5 * 10**18
    withdraw_description = "Withdraw Amount To Account B"

    # Assert before Actions
    assert dao_token.balanceOf(token_wallet) == 200 * 10**18
    assert dao_token.balanceOf(account_b) == 0

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        token_wallet.withdraw(
            account_b,
            withdraw_amount,
            withdraw_description,
            {"from": token_wallet_invalid_owner}
        )

    # Assert after Actions
    assert dao_token.balanceOf(token_wallet) == 200 * 10 ** 18
    assert dao_token.balanceOf(account_b) == 0


def test_success__withdraw__not_enough_balance(
        token_wallet_deployment, data_test
):
    # Arranges
    dao_token = token_wallet_deployment['dao_token']
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_b = accounts.add()
    withdraw_amount = 201 * 10**18
    withdraw_description = "Withdraw Amount To Account B"

    # Assert before Actions
    assert dao_token.balanceOf(token_wallet) == 200 * 10**18
    assert dao_token.balanceOf(account_b) == 0

    # Actions
    with brownie.reverts("ERC20: transfer amount exceeds balance"):
        token_wallet.withdraw(
            account_b,
            withdraw_amount,
            withdraw_description,
            {"from": token_wallet_owner}
        )

    # Assert after Actions
    assert dao_token.balanceOf(token_wallet) == 200 * 10 ** 18
    assert dao_token.balanceOf(account_b) == 0
