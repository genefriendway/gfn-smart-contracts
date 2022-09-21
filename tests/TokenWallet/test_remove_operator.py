import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


@pytest.fixture
def data_test(token_wallet_deployment):
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = accounts.add()
    account_b = accounts.add()
    account_c = accounts.add()
    token_wallet.addOperator(account_a, {"from": token_wallet_owner})
    token_wallet.addOperator(account_b, {"from": token_wallet_owner})
    token_wallet.addOperator(account_c, {"from": token_wallet_owner})

    return {
        'operator_a': account_a,
        'operator_b': account_b,
        'operator_c': account_c,
    }


def test_success__remove_operator__owner_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    operator_a = data_test['operator_a']

    # Assert before Actions
    assert token_wallet.checkActiveOperator(operator_a) is True

    # Actions
    txn = token_wallet.removeOperator(operator_a, {"from": token_wallet_owner})

    # Assert: AddOperator Event
    assert ('RemoveOperator' in txn.events) is True
    assert txn.events['RemoveOperator']['operatorAddress'] == operator_a

    # Asserts
    assert token_wallet.checkActiveOperator(operator_a) is False


def test_failure__remove_operator__not_owner_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    operator_a = data_test['operator_a']
    operator_b = data_test['operator_b']

    # Assert before Actions
    assert token_wallet.checkActiveOperator(operator_a) is True
    assert token_wallet.checkActiveOperator(operator_b) is True

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        token_wallet.removeOperator(operator_a, {"from": operator_b})

    # Asserts
    assert token_wallet.checkActiveOperator(operator_a) is True
    assert token_wallet.checkActiveOperator(operator_b) is True


def test_success__remove_operator__operator_address_null(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    operator_a = "0x0000000000000000000000000000000000000000"

    # Assert before Actions
    assert token_wallet.checkActiveOperator(operator_a) is False

    # Actions
    with brownie.reverts("TokenWallet: address of operator must be not null"):
        token_wallet.removeOperator(operator_a, {"from": token_wallet_owner})

    # Asserts
    assert token_wallet.checkActiveOperator(operator_a) is False


def test_success__remove_operator__not_existed_operator(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    fake_operator = accounts.add()

    # set account is operator
    assert token_wallet.checkActiveOperator(fake_operator) is False

    # Actions: try to set account_a as operator again
    with brownie.reverts("TokenWallet: can not remove a operator that does not exist"):
        token_wallet.removeOperator(fake_operator, {"from": token_wallet_owner})

    # Asserts
    assert token_wallet.checkActiveOperator(fake_operator) is False
