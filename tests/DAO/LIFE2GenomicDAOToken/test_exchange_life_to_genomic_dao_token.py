import pytest
import brownie


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__exchange_life_to_genomic_dao_token(
        life_2_genomic_dao_token_deployment
):
    # Arrange
    dao_token = life_2_genomic_dao_token_deployment['dao_token']
    life_token = life_2_genomic_dao_token_deployment['life_token']
    life_2_genomic_dao_token = \
        life_2_genomic_dao_token_deployment['life_2_genomic_dao_token']
    owner = life_2_genomic_dao_token_deployment['owner']
    reserve = life_2_genomic_dao_token_deployment['reserve']
    dao_token_holder = life_2_genomic_dao_token_deployment['dao_token_holder']
    receive_account = brownie.accounts.add()

    amount_life = 20
    amount_genomic_token = 10

    contract_balance = life_token.balanceOf(life_2_genomic_dao_token.address)
    receive_account_balance = life_token.balanceOf(receive_account)
    reserve_balance = dao_token.balanceOf(reserve)
    dao_token_holder_balance = dao_token.balanceOf(dao_token_holder)

    # Action
    life_2_genomic_dao_token.exchangeLifeToGenomicDaoToken(
        amount_life,
        amount_genomic_token,
        dao_token_holder,
        receive_account.address,
        {'from': owner}
    )

    # Assert
    assert life_token.balanceOf(
        life_2_genomic_dao_token.address
    ) == contract_balance - amount_life  # Contract life token decrease

    assert life_token.balanceOf(
        receive_account
    ) == receive_account_balance + amount_life  # Increase life token

    assert dao_token.balanceOf(
        dao_token_holder
    ) == dao_token_holder_balance - amount_genomic_token  # Decrease dao token in dao holder account

    assert dao_token.balanceOf(
        reserve
    ) == reserve_balance + amount_genomic_token  # Life reserve increase


def test_exchange_life_to_genomic_dao_token_not_valid_owner(
        life_2_genomic_dao_token_deployment):
    # Arrange
    life_2_genomic_dao_token = \
        life_2_genomic_dao_token_deployment['life_2_genomic_dao_token']
    dao_token_holder = life_2_genomic_dao_token_deployment['dao_token_holder']
    receive_account = brownie.accounts.add()

    amount_life = 10
    amount_genomic_token = 20

    new_account = brownie.accounts.add()

    # Action

    # Assert
    with brownie.reverts("Ownable: caller is not the owner"):
        life_2_genomic_dao_token.exchangeLifeToGenomicDaoToken(
            amount_life,
            amount_genomic_token,
            dao_token_holder,
            receive_account.address,
            {'from': new_account}
        )


def test_exchange_life_to_genomic_dao_token_zero_to_address(
        life_2_genomic_dao_token_deployment,
        zero_address
):
    # Arrange
    life_2_genomic_dao_token = \
        life_2_genomic_dao_token_deployment['life_2_genomic_dao_token']
    owner = life_2_genomic_dao_token_deployment['owner']
    dao_token_holder = life_2_genomic_dao_token_deployment['dao_token_holder']

    amount_life = 10
    amount_genomic_token = 20

    # Action

    # Assert
    with brownie.reverts("To address is zero address"):
        life_2_genomic_dao_token.exchangeLifeToGenomicDaoToken(
            amount_life,
            amount_genomic_token,
            dao_token_holder,
            zero_address,
            {'from': owner}
        )


def test_exchange_life_to_genomic_dao_token_exceed_balance(
        life_2_genomic_dao_token_deployment):
    # Arrange
    life_2_genomic_dao_token = \
        life_2_genomic_dao_token_deployment['life_2_genomic_dao_token']
    owner = life_2_genomic_dao_token_deployment['owner']

    dao_token_holder = life_2_genomic_dao_token_deployment['dao_token_holder']
    receive_account = brownie.accounts.add()

    amount_life = 2000
    amount_genomic_token = 10

    # Action
    with brownie.reverts("LIFE amount exceeds balance"):
        life_2_genomic_dao_token.exchangeLifeToGenomicDaoToken(
            amount_life,
            amount_genomic_token,
            dao_token_holder,
            receive_account.address,
            {'from': owner}
        )


def test_exchange_life_to_genomic_dao_token_not_enough_life_allowance(
        life_2_genomic_dao_token_deployment):
    life_2_genomic_dao_token = \
        life_2_genomic_dao_token_deployment['life_2_genomic_dao_token']
    owner = life_2_genomic_dao_token_deployment['owner']
    dao_token_holder = life_2_genomic_dao_token_deployment['dao_token_holder']
    receive_account = brownie.accounts.add()

    amount_life = 20
    amount_genomic_token = 1000

    # Action
    with brownie.reverts("GenomicDaoToken allowance was not enough"):
        life_2_genomic_dao_token.exchangeLifeToGenomicDaoToken(
            amount_life,
            amount_genomic_token,
            dao_token_holder,
            receive_account.address,
            {'from': owner}
        )
