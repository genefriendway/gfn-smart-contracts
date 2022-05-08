import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__sell_dao_token_to_buy_life(dao_token_lock_deployment):
    # Arrange
    dao_token = dao_token_lock_deployment['dao_token']
    dao_token_lock = dao_token_lock_deployment['dao_token_lock']
    owner = dao_token_lock_deployment['owner']
    to_account = accounts[2]

    to_account_balance = dao_token.balanceOf(to_account)
    lock_balance = dao_token.balanceOf(dao_token_lock.address)
    sell_amount = 10

    # Action
    dao_token_lock.sellGenomicDaoTokenToBuyLife(
        to_account,
        sell_amount,
        {'from': owner}
    )

    # Assert
    assert dao_token.balanceOf(to_account) == to_account_balance + sell_amount
    assert dao_token.balanceOf(
        dao_token_lock.address
    ) == lock_balance - sell_amount
