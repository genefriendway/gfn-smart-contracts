import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__transfer_dao_token(dao_deployment):
    # Arrange
    dao_token = dao_deployment['dao_token']
    owner = dao_deployment['owner']
    user = accounts[2]
    transfer_amount = 100

    owner_balance = dao_token.balanceOf(owner)
    user_balance = dao_token.balanceOf(user)

    # Action
    tx = dao_token.transfer(user, transfer_amount, {"from": owner})

    # Assert: Transfer event
    assert 'Transfer' in tx.events
    assert tx.events['Transfer']['from'] == owner
    assert tx.events['Transfer']['to'] == user
    assert tx.events['Transfer']['value'] == 100

    # Assert
    assert dao_token.balanceOf(owner) == owner_balance - transfer_amount
    assert dao_token.balanceOf(user) == user_balance + transfer_amount


def test_success__transfer_dao_token__amount_eq_0(dao_deployment):
    # Arrange
    dao_token = dao_deployment['dao_token']
    owner = dao_deployment['owner']
    user = accounts[2]
    transfer_amount = 0

    owner_balance = dao_token.balanceOf(owner)
    user_balance = dao_token.balanceOf(user)

    # Action
    tx = dao_token.transfer(user, transfer_amount, {"from": owner})

    # Assert: Transfer event
    assert 'Transfer' in tx.events
    assert tx.events['Transfer']['from'] == owner
    assert tx.events['Transfer']['to'] == user
    assert tx.events['Transfer']['value'] == 0

    # Assert
    assert dao_token.balanceOf(owner) == owner_balance - transfer_amount
    assert dao_token.balanceOf(user) == user_balance + transfer_amount
