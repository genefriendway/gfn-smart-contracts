import pytest
import brownie

from brownie import (
    accounts,
    TokenVesting,
)


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


@pytest.fixture
def data_test(vesting_deployment, util):
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_contract = vesting_deployment['token_vesting_contract']

    dao_token_contract.transfer(
        vesting_contract, 10000e+18, {"from": dao_token_owner}
    )


def test_success__withdraw__withdrawing_amount_lt_balance(
        vesting_deployment, data_test
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']

    # Assert before actions
    assert dao_token_contract.balanceOf(vesting_contract, {"from": dao_token_owner}) \
           == 10000e+18
    assert dao_token_contract.balanceOf(vesting_owner, {"from": dao_token_owner}) \
           == 0

    # Action
    vesting_contract.withdraw(
        2000e+18, {"from": vesting_owner}
    )

    # Assert after actions
    assert dao_token_contract.balanceOf(vesting_contract, {"from": dao_token_owner}) \
           == 8000e+18
    assert dao_token_contract.balanceOf(vesting_owner, {"from": dao_token_owner}) \
           == 2000e+18


def test_success__withdraw__withdrawing_amount_eq_balance(
        vesting_deployment, data_test
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']

    # Assert before actions
    assert dao_token_contract.balanceOf(vesting_contract, {"from": dao_token_owner}) \
           == 10000e+18
    assert dao_token_contract.balanceOf(vesting_owner, {"from": dao_token_owner}) \
           == 0

    # Action
    vesting_contract.withdraw(
        10000e+18, {"from": vesting_owner}
    )

    # Assert after actions
    assert dao_token_contract.balanceOf(vesting_contract, {"from": dao_token_owner}) \
           == 0
    assert dao_token_contract.balanceOf(vesting_owner, {"from": dao_token_owner}) \
           == 10000e+18


def test_failure__withdraw__not_owner(vesting_deployment, data_test):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    fake_owner = accounts.add()

    # Assert before actions
    assert dao_token_contract.balanceOf(vesting_contract, {"from": dao_token_owner}) \
           == 10000e+18
    assert dao_token_contract.balanceOf(vesting_owner, {"from": dao_token_owner}) \
           == 0

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        vesting_contract.withdraw(2000e+18, {"from": fake_owner})


def test_failure__withdraw__not_enough_balance(vesting_deployment, data_test):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']

    # Assert before actions
    assert dao_token_contract.balanceOf(vesting_contract, {"from": dao_token_owner}) \
           == 10000e+18
    assert dao_token_contract.balanceOf(vesting_owner, {"from": dao_token_owner}) \
           == 0

    # Action
    with brownie.reverts("TokenVesting: not enough withdrawable funds"):
        vesting_contract.withdraw(12000e+18, {"from": vesting_owner})
