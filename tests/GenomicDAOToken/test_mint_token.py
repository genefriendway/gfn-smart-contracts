import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__mint_dao_token(dao_deployment):
    # Arrange
    dao_token = dao_deployment['dao_token']
    owner = dao_deployment['owner']
    account = accounts[2]

    total_supply = dao_token.totalSupply()
    mint_amount = 1000

    # Action
    dao_token.mint(account, mint_amount, {"from": owner})

    # Assert
    assert dao_token.totalSupply() == total_supply + mint_amount
    assert dao_token.balanceOf(account) == mint_amount


def test_mint_dao_token_over_cap(dao_deployment):  # Arrange
    dao_token = dao_deployment['dao_token']
    owner = dao_deployment['owner']
    cap = dao_deployment['cap']
    account = accounts[2]

    total_supply = dao_token.totalSupply()
    mint_amount = cap - total_supply + 1

    # Action

    # Assert
    with brownie.reverts("ERC20Capped: cap exceeded"):
        dao_token.mint(account, mint_amount, {"from": owner})
