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

    account_a = accounts.add()
    decreasing_amount = 100 * 10 ** 18
    decreasing_description = "Increase Balance of Account A"
    token_wallet.increaseBalance(
        account_a,
        decreasing_amount,
        decreasing_description,
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
        'account_a': account_a
    }


def test_success__transfer_from__owner_make_txn(
        token_wallet_deployment, data_test
):
    # Arranges
    dao_token = token_wallet_deployment['dao_token']
    token_wallet = token_wallet_deployment['token_wallet']
    token_wallet_owner = token_wallet_deployment['token_wallet_owner']
    from_account_a = data_test['account_a']
    to_account_b = accounts.add()

    transferring_amount = 5 * 10**18
    transferring_description = "Transfer Amount of Account B"

    # Assert before Actions
    assert dao_token.balanceOf(token_wallet) == 200 * 10**18
    assert dao_token.balanceOf(to_account_b) == 0
    assert token_wallet.getBalance(from_account_a) == 100 * 10 ** 18

    # Actions
    txn = token_wallet.transferFrom(
        from_account_a,
        to_account_b,
        transferring_amount,
        transferring_description,
        {"from": token_wallet_owner}
    )

    # Assert: TransferToken Event
    assert ('TransferToken' in txn.events) is True
    assert txn.events['TransferToken']['toAddress'] == to_account_b
    assert txn.events['TransferToken']['amount'] == transferring_amount
    assert txn.events['TransferToken']['description'] == transferring_description

    # Assert: TransferTokenFrom Event
    assert ('TransferTokenFrom' in txn.events) is True
    assert txn.events['TransferTokenFrom']['fromAddress'] == from_account_a
    assert txn.events['TransferTokenFrom']['toAddress'] == to_account_b
    assert txn.events['TransferTokenFrom']['amount'] == transferring_amount
    assert txn.events['TransferTokenFrom']['description'] == transferring_description

    # Assert
    assert dao_token.balanceOf(token_wallet) == 195 * 10 ** 18
    assert dao_token.balanceOf(to_account_b) == 5 * 10 ** 18
    assert token_wallet.getBalance(from_account_a) == 95 * 10 ** 18
