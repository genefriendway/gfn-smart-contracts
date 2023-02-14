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
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    token_wallet_operator = accounts.add()

    account_a = accounts.add()
    increasing_amount = 100 * 10 ** 18
    increasing_description = "Increase Balance of Account A"
    token_wallet.increaseBalance(
        account_a,
        increasing_amount,
        increasing_description,
        {"from": token_wallet_owner}
    )
    token_wallet.addOperator(
        token_wallet_operator,
        {"from": token_wallet_owner}
    )

    assert dao_token.balanceOf(dao_token_owner) == 100000000 * 10 ** 18
    dao_token.transfer(
        token_wallet,
        200 * 10**18,
        {"from": dao_token_owner}
    )
    assert dao_token.balanceOf(dao_token_owner) == 99999800 * 10 ** 18
    assert dao_token.balanceOf(token_wallet) == 200 * 10 ** 18
    
    return {
        'account_a': account_a,
        'token_wallet_operator': token_wallet_operator,
    }


def test_success__withdraw_from__owner_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    dao_token = token_wallet_deployment['dao_token']
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    from_account_a = data_test['account_a']
    to_account_b = accounts.add()

    withdraw_amount = 5 * 10**18
    withdraw_description = "Transfer Amount of Account B"

    # Assert before Actions
    assert dao_token.balanceOf(token_wallet) == 200 * 10**18
    assert dao_token.balanceOf(to_account_b) == 0
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18

    # Actions
    txn = token_wallet.withdrawFrom(
        from_account_a,
        to_account_b,
        withdraw_amount,
        withdraw_description,
        {"from": token_wallet_owner}
    )

    # Assert: WithdrawFrom Event
    assert ('WithdrawFrom' in txn.events) is True
    assert txn.events['WithdrawFrom']['fromAddress'] == from_account_a
    assert txn.events['WithdrawFrom']['toAddress'] == to_account_b
    assert txn.events['WithdrawFrom']['amount'] == withdraw_amount
    assert txn.events['WithdrawFrom']['description'] == withdraw_description

    # Assert
    assert dao_token.balanceOf(token_wallet) == 195 * 10 ** 18
    assert dao_token.balanceOf(to_account_b) == 5 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 95 * 10 ** 18


def test_success__withdraw_from__operator_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    dao_token = token_wallet_deployment['dao_token']
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_operator = data_test['token_wallet_operator']
    from_account_a = data_test['account_a']
    to_account_b = accounts.add()

    withdraw_amount = 5 * 10**18
    withdraw_description = "Transfer Amount of Account B"

    # Assert before Actions
    assert dao_token.balanceOf(token_wallet) == 200 * 10**18
    assert dao_token.balanceOf(to_account_b) == 0
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18

    # Actions
    txn = token_wallet.withdrawFrom(
        from_account_a,
        to_account_b,
        withdraw_amount,
        withdraw_description,
        {"from": token_wallet_operator}
    )

    # Assert: WithdrawFrom Event
    assert ('WithdrawFrom' in txn.events) is True
    assert txn.events['WithdrawFrom']['fromAddress'] == from_account_a
    assert txn.events['WithdrawFrom']['toAddress'] == to_account_b
    assert txn.events['WithdrawFrom']['amount'] == withdraw_amount
    assert txn.events['WithdrawFrom']['description'] == withdraw_description

    # Assert
    assert dao_token.balanceOf(token_wallet) == 195 * 10 ** 18
    assert dao_token.balanceOf(to_account_b) == 5 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 95 * 10 ** 18


def test_failure__withdraw_from__not_operator_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    dao_token = token_wallet_deployment['dao_token']
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_operator_fake = accounts.add()
    from_account_a = data_test['account_a']
    to_account_b = accounts.add()

    withdraw_amount = 5 * 10**18
    withdraw_description = "Transfer Amount of Account B"

    # Assert before Actions
    assert dao_token.balanceOf(token_wallet) == 200 * 10**18
    assert dao_token.balanceOf(to_account_b) == 0
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18

    # Actions
    with brownie.reverts("TokenWallet: caller must be the operator"):
        token_wallet.withdrawFrom(
            from_account_a,
            to_account_b,
            withdraw_amount,
            withdraw_description,
            {"from": token_wallet_operator_fake}
        )

    # Assert
    assert dao_token.balanceOf(token_wallet) == 200 * 10 ** 18
    assert dao_token.balanceOf(to_account_b) == 0
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18
