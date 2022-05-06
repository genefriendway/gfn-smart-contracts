import pytest


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__burn_dao_token(dao_deployment):
    # Arrange
    dao_token = dao_deployment['dao_token']
    owner = dao_deployment['owner']

    total_supply = dao_token.totalSupply()
    burn_amount = 100

    # Action
    dao_token.burn(burn_amount, {"from": owner})

    # Assert
    assert dao_token.totalSupply() == total_supply - burn_amount
    assert dao_token.balanceOf(owner) == total_supply - burn_amount
