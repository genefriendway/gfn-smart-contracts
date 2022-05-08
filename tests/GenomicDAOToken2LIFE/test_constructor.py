import pytest


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__initialize_dao_token(dao_token_lock_deployment):
    # Arranges
    dao_token = dao_token_lock_deployment['dao_token']
    life_token = dao_token_lock_deployment['life_token']
    dao_token_lock = dao_token_lock_deployment['dao_token_lock']
    owner = dao_token_lock_deployment['owner']

    # Assert
    assert dao_token.balanceOf(dao_token_lock.address) == 100
    assert life_token.balanceOf(dao_token_lock.address) == 100
    assert dao_token.balanceOf(owner) == 900
    assert life_token.balanceOf(owner) == 900
