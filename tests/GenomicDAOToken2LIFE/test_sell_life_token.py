import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__sell_life_to_buy_dao_token(dao_token_lock_deployment):
    # Arrange
    life_token = dao_token_lock_deployment['life_token']
    dao_token_lock = dao_token_lock_deployment['dao_token_lock']
    owner = dao_token_lock_deployment['owner']
    to_account = accounts[2]

    to_account_balance = life_token.balanceOf(to_account)
    lock_balance = life_token.balanceOf(dao_token_lock.address)
    sell_amount = 10

    # Action
    dao_token_lock.sellLifeToBuyGenomicDaoToken(
        to_account,
        sell_amount,
        {'from': owner}
    )

    # Assert
    assert life_token.balanceOf(to_account) == to_account_balance + sell_amount
    assert life_token.balanceOf(
        dao_token_lock.address
    ) == lock_balance - sell_amount
