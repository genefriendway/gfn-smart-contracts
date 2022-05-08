import pytest
import brownie


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


def test_burn_exceed_amount_dao_token(dao_deployment):
    # Arrange
    dao_token = dao_deployment['dao_token']
    owner = dao_deployment['owner']

    burn_amount = dao_token.balanceOf(owner) + 1

    # Action

    # Assert
    with brownie.reverts("ERC20: burn amount exceeds balance"):
        dao_token.burn(burn_amount, {"from": owner})


def test_burn_dao_token_from_zero_address(dao_deployment, zero_address):
    # Arrange
    dao_token = dao_deployment['dao_token']
    owner = dao_deployment['owner']

    burn_amount = dao_token.balanceOf(owner) + 1

    # Action

    # Assert
    with brownie.reverts("ERC20: burn from the zero address"):
        dao_token.burn(burn_amount,
                       {"from": zero_address})
