import pytest
import brownie


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__withdraw_genomic_dao_token(
        genomic_dao_token_2_life_deployment
):
    # Arrange
    dao_token = genomic_dao_token_2_life_deployment['dao_token']
    genomic_dao_token_2_life = \
        genomic_dao_token_2_life_deployment['genomic_dao_token_2_life']
    owner = genomic_dao_token_2_life_deployment['owner']
    amount = 10

    owner_balance = dao_token.balanceOf(owner)

    # Action
    genomic_dao_token_2_life.withdrawGenomicDaoToken(
        amount,
        owner,
        {'from': owner}
    )

    # Assert
    assert dao_token.balanceOf(owner) == owner_balance + amount


def test_withdraw_genomic_dao_token_to_zero_address(
        genomic_dao_token_2_life_deployment, zero_address
):
    # Arrange
    genomic_dao_token_2_life = \
        genomic_dao_token_2_life_deployment['genomic_dao_token_2_life']
    owner = genomic_dao_token_2_life_deployment['owner']
    amount = 10

    # Action

    # Assert
    with brownie.reverts("To address is zero address"):
        genomic_dao_token_2_life.withdrawGenomicDaoToken(
            amount,
            zero_address,
            {'from': owner}
        )


def test_withdraw_genomic_dao_token_from_not_valid_owner(
        genomic_dao_token_2_life_deployment
):
    # Arrange
    genomic_dao_token_2_life = \
        genomic_dao_token_2_life_deployment['genomic_dao_token_2_life']
    owner = genomic_dao_token_2_life_deployment['owner']
    amount = 10
    new_account = brownie.accounts.add()

    # Action

    # Assert
    with brownie.reverts("Ownable: caller is not the owner"):
        genomic_dao_token_2_life.withdrawGenomicDaoToken(
            amount,
            owner,
            {'from': new_account}
        )
