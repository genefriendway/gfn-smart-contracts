import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__add_operator__owner_make_txn(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = accounts.add()

    # Assert before Actions
    assert token_wallet.checkActiveOperator(account_a) is False

    # Actions
    txn = token_wallet.addOperator(
        account_a,
        {"from": token_wallet_owner}
    )

    # Assert: AddOperator Event
    assert ('AddOperator' in txn.events) is True
    assert txn.events['AddOperator']['operatorAddress'] == account_a

    # Asserts
    assert token_wallet.checkActiveOperator(account_a) is True


def test_failure__add_operator__not_owner_make_txn(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    invalid_owner = accounts.add()
    account_a = accounts.add()

    # Assert before Actions
    assert token_wallet.checkActiveOperator(account_a) is False

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        token_wallet.addOperator(
            account_a,
            {"from": invalid_owner}
        )

    # Asserts
    assert token_wallet.checkActiveOperator(account_a) is False


def test_success__add_operator__operator_address_null(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = "0x0000000000000000000000000000000000000000"

    assert token_wallet.checkActiveOperator(account_a) is False

    # Actions: try to set account_a as operator again
    with brownie.reverts("TokenWallet: address of operator must be not null"):
        token_wallet.addOperator(account_a, {"from": token_wallet_owner})

    # Asserts
    assert token_wallet.checkActiveOperator(account_a) is False


def test_success__add_operator__add_existed_operator(token_wallet_deployment):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    account_a = accounts.add()

    # set account is operator
    token_wallet.addOperator(account_a, {"from": token_wallet_owner})
    assert token_wallet.checkActiveOperator(account_a) is True

    # Actions: try to set account_a as operator again
    with brownie.reverts("TokenWallet: the operator was added"):
        token_wallet.addOperator(account_a, {"from": token_wallet_owner})

    # Asserts
    assert token_wallet.checkActiveOperator(account_a) is True
