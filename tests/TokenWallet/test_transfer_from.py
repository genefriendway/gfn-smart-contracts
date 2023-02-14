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
    token_wallet_operator = accounts.add()

    account_a = accounts.add()
    deposit_amount = 100 * 10 ** 18
    deposit_description = "Increase Balance of Account A"
    token_wallet.deposit(
        account_a,
        deposit_amount,
        deposit_description,
        {"from": token_wallet_owner}
    )

    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(account_a) == 100 * 10 ** 18

    token_wallet.addOperator(token_wallet_operator, {"from": token_wallet_owner})
    
    return {
        'account_a': account_a,
        'token_wallet_operator': token_wallet_operator,
    }


def test_success__transfer_from__owner_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    from_account_a = data_test['account_a']
    to_account_b = accounts.add()

    transfer_amount = 5 * 10 ** 18
    transfer_description = "Transfer Amount From Account A to Account B"

    # Assert before Actions
    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18
    assert token_wallet.getBalance(to_account_b) == 0

    # Actions
    txn = token_wallet.transferFrom(
        from_account_a,
        to_account_b,
        transfer_amount,
        transfer_description,
        {"from": token_wallet_owner}
    )

    # Assert: TransferFrom Event
    assert ('TransferFrom' in txn.events) is True
    assert txn.events['TransferFrom']['fromAddress'] == from_account_a
    assert txn.events['TransferFrom']['toAddress'] == to_account_b
    assert txn.events['TransferFrom']['amount'] == transfer_amount
    assert txn.events['TransferFrom']['description'] == transfer_description

    # Assert
    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 95 * 10 ** 18
    assert token_wallet.getBalance(to_account_b) == 5 * 10 ** 18


def test_success__transfer_from__operator_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_operator = data_test['token_wallet_operator']
    from_account_a = data_test['account_a']
    to_account_b = accounts.add()

    transfer_amount = 20 * 10 ** 18
    transfer_description = "Transfer Amount From Account A to Account B"

    # Assert before Actions
    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18
    assert token_wallet.getBalance(to_account_b) == 0

    # Actions
    txn = token_wallet.transferFrom(
        from_account_a,
        to_account_b,
        transfer_amount,
        transfer_description,
        {"from": token_wallet_operator}
    )

    # Assert: TransferFrom Event
    assert ('TransferFrom' in txn.events) is True
    assert txn.events['TransferFrom']['fromAddress'] == from_account_a
    assert txn.events['TransferFrom']['toAddress'] == to_account_b
    assert txn.events['TransferFrom']['amount'] == transfer_amount
    assert txn.events['TransferFrom']['description'] == transfer_description

    # Assert
    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 80 * 10 ** 18
    assert token_wallet.getBalance(to_account_b) == 20 * 10 ** 18


def test_failure__transfer_from__not_operator_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_operator_fake = accounts.add()
    from_account_a = data_test['account_a']
    to_account_b = accounts.add()

    transfer_amount = 20 * 10 ** 18
    transfer_description = "Transfer Amount From Account A to Account B"

    # Assert before Actions
    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18
    assert token_wallet.getBalance(to_account_b) == 0

    # Actions
    with brownie.reverts("TokenWallet: caller must be the operator"):
        token_wallet.transferFrom(
            from_account_a,
            to_account_b,
            transfer_amount,
            transfer_description,
            {"from": token_wallet_operator_fake}
        )

    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18
    assert token_wallet.getBalance(to_account_b) == 0


def test_failure__transfer_from__sender_account_null(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_operator = data_test['token_wallet_operator']
    from_account_a = "0x0000000000000000000000000000000000000000"
    to_account_b = accounts.add()

    transfer_amount = 20 * 10 ** 18
    transfer_description = "Transfer Amount From Account A to Account B"

    # Assert before Actions
    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(to_account_b) == 0

    # Actions
    with brownie.reverts("TokenWallet: address must not be null"):
        token_wallet.transferFrom(
            from_account_a,
            to_account_b,
            transfer_amount,
            transfer_description,
            {"from": token_wallet_operator}
        )

    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(to_account_b) == 0


def test_failure__transfer_from__receiver_account_null(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_operator = data_test['token_wallet_operator']
    from_account_a = data_test['account_a']
    to_account_b = "0x0000000000000000000000000000000000000000"

    transfer_amount = 20 * 10 ** 18
    transfer_description = "Transfer Amount From Account A to Account B"

    # Assert before Actions
    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18
    assert token_wallet.getBalance(to_account_b) == 0

    # Actions
    with brownie.reverts("TokenWallet: address must not be null"):
        token_wallet.transferFrom(
            from_account_a,
            to_account_b,
            transfer_amount,
            transfer_description,
            {"from": token_wallet_operator}
        )

    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18
    assert token_wallet.getBalance(to_account_b) == 0


def test_failure__transfer_from__amount_is_zero(
        token_wallet_deployment, data_test
):
    # Arranges
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_operator = data_test['token_wallet_operator']
    from_account_a = data_test['account_a']
    to_account_b = accounts.add()

    transfer_amount = 0
    transfer_description = "Transfer Amount From Account A to Account B"

    # Assert before Actions
    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18
    assert token_wallet.getBalance(to_account_b) == 0

    # Actions
    with brownie.reverts("TokenWallet: amount must be greater than zero"):
        token_wallet.transferFrom(
            from_account_a,
            to_account_b,
            transfer_amount,
            transfer_description,
            {"from": token_wallet_operator}
        )

    assert token_wallet.getTotalBalance() == 100 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18
    assert token_wallet.getBalance(to_account_b) == 0