import pytest
import brownie


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__withdraw_life(
        life_2_genomic_dao_token_deployment
):
    # Arrange
    life_token = life_2_genomic_dao_token_deployment['life_token']
    life_2_genomic_dao_token = \
        life_2_genomic_dao_token_deployment[
            'life_2_genomic_dao_token']
    owner = life_2_genomic_dao_token_deployment['owner']
    amount = 10

    owner_balance = life_token.balanceOf(owner)

    # Action
    life_2_genomic_dao_token.withdrawLifeToBuyPCSP(
        amount,
        owner,
        {'from': owner}
    )

    # Assert
    assert life_token.balanceOf(owner) == owner_balance + amount


def test_failure__withdraw_life_to_zero_address(
        life_2_genomic_dao_token_deployment, zero_address
):
    # Arrange
    life_2_genomic_dao_token = \
        life_2_genomic_dao_token_deployment[
            'life_2_genomic_dao_token']
    owner = life_2_genomic_dao_token_deployment['owner']
    amount = 10

    # Action

    # Assert
    with brownie.reverts("To address is zero address"):
        life_2_genomic_dao_token.withdrawLifeToBuyPCSP(
            amount,
            zero_address,
            {'from': owner}
        )


def test_failure__withdraw_life_from_not_valid_owner(
        life_2_genomic_dao_token_deployment
):
    # Arrange
    life_2_genomic_dao_token = \
        life_2_genomic_dao_token_deployment['life_2_genomic_dao_token']
    owner = life_2_genomic_dao_token_deployment['owner']
    amount = 10
    new_account = brownie.accounts.add()

    # Action

    # Assert
    with brownie.reverts("Ownable: caller is not the owner"):
        life_2_genomic_dao_token.withdrawLifeToBuyPCSP(
            amount,
            owner,
            {'from': new_account}
        )


def test_failure__withdraw_life_exceed_balance(
        life_2_genomic_dao_token_deployment
):
    # Arrange
    life_2_genomic_dao_token = \
        life_2_genomic_dao_token_deployment['life_2_genomic_dao_token']
    owner = life_2_genomic_dao_token_deployment['owner']
    amount = 10000

    # Action

    # Assert
    with brownie.reverts("LIFE amount exceeds balance"):
        life_2_genomic_dao_token.withdrawLifeToBuyPCSP(
            amount,
            owner,
            {'from': owner}
        )
