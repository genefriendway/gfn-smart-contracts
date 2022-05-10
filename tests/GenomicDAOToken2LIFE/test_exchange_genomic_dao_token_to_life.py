import pytest
import brownie


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__exchange_genomic_dao_token_to_life(
        genomic_dao_token_2_life_deployment
):
    # Arrange
    dao_token = genomic_dao_token_2_life_deployment['dao_token']
    life_token = genomic_dao_token_2_life_deployment['life_token']
    genomic_dao_token_2_life = \
        genomic_dao_token_2_life_deployment['genomic_dao_token_2_life']
    owner = genomic_dao_token_2_life_deployment['owner']
    reserve = genomic_dao_token_2_life_deployment['reserve']
    life_holder = genomic_dao_token_2_life_deployment['life_holder']
    receive_account = brownie.accounts.add()

    amount_life = 10
    amount_genomic_token = 20

    contract_balance = dao_token.balanceOf(genomic_dao_token_2_life.address)
    receive_account_balance = dao_token.balanceOf(receive_account)
    reserve_balance = life_token.balanceOf(reserve)
    life_holder_balance = life_token.balanceOf(life_holder)

    # Action
    genomic_dao_token_2_life.exchangeGenomicDaoTokenToLife(
        amount_genomic_token,
        amount_life,
        life_holder,
        receive_account.address,
        {'from': owner}
    )

    # Assert
    assert dao_token.balanceOf(
        genomic_dao_token_2_life.address
    ) == contract_balance - amount_genomic_token  # Contract dao token decrease

    assert dao_token.balanceOf(
        receive_account
    ) == receive_account_balance + amount_genomic_token  # Increase dao token

    assert life_token.balanceOf(
        life_holder
    ) == life_holder_balance - amount_life  # Decrease life in life holder account

    assert life_token.balanceOf(
        reserve
    ) == reserve_balance + amount_life  # Life reserve increase


def test_exchange_genomic_dao_token_to_life_not_valid_owner(
        genomic_dao_token_2_life_deployment):
    # Arrange
    genomic_dao_token_2_life = \
        genomic_dao_token_2_life_deployment['genomic_dao_token_2_life']
    life_holder = genomic_dao_token_2_life_deployment['life_holder']
    receive_account = brownie.accounts.add()

    amount_life = 10
    amount_genomic_token = 20

    new_account = brownie.accounts.add()

    # Action

    # Assert
    with brownie.reverts("Ownable: caller is not the owner"):
        genomic_dao_token_2_life.exchangeGenomicDaoTokenToLife(
            amount_genomic_token,
            amount_life,
            life_holder,
            receive_account.address,
            {'from': new_account}
        )


def test_exchange_genomic_dao_token_to_life_zero_to_address(
        genomic_dao_token_2_life_deployment,
        zero_address
):
    # Arrange
    genomic_dao_token_2_life = \
        genomic_dao_token_2_life_deployment['genomic_dao_token_2_life']
    owner = genomic_dao_token_2_life_deployment['owner']
    life_holder = genomic_dao_token_2_life_deployment['life_holder']

    amount_life = 10
    amount_genomic_token = 20

    # Action

    # Assert
    with brownie.reverts("To address is zero address"):
        genomic_dao_token_2_life.exchangeGenomicDaoTokenToLife(
            amount_genomic_token,
            amount_life,
            life_holder,
            zero_address,
            {'from': owner}
        )


def test_exchange_genomic_dao_token_to_life_exceed_balance(
        genomic_dao_token_2_life_deployment):
    # Arrange
    genomic_dao_token_2_life = \
        genomic_dao_token_2_life_deployment['genomic_dao_token_2_life']
    owner = genomic_dao_token_2_life_deployment['owner']

    life_holder = genomic_dao_token_2_life_deployment['life_holder']
    receive_account = brownie.accounts.add()

    amount_life = 10
    amount_genomic_token = 2000

    # Action
    with brownie.reverts("Genomic Dao Token amount exceeds balance"):
        genomic_dao_token_2_life.exchangeGenomicDaoTokenToLife(
            amount_genomic_token,
            amount_life,
            life_holder,
            receive_account.address,
            {'from': owner}
        )


def test_exchange_genomic_dao_token_to_life_not_enough_life_allowance(
        genomic_dao_token_2_life_deployment):
    genomic_dao_token_2_life = \
        genomic_dao_token_2_life_deployment['genomic_dao_token_2_life']
    owner = genomic_dao_token_2_life_deployment['owner']
    life_holder = genomic_dao_token_2_life_deployment['life_holder']
    receive_account = brownie.accounts.add()

    amount_life = 1000
    amount_genomic_token = 20

    # Action
    with brownie.reverts("LIFE allowance was not enough"):
        genomic_dao_token_2_life.exchangeGenomicDaoTokenToLife(
            amount_genomic_token,
            amount_life,
            life_holder,
            receive_account.address,
            {'from': owner}
        )
