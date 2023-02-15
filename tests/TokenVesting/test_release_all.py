import time
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
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']

    beneficiary = accounts.add()
    current_timestamp = util.get_timestamp()
    start_vesting_time = current_timestamp - 250
    cliff_period_seconds = 200
    vesting_duration_seconds = 600
    slice_period_seconds = 50
    revocable = True
    vesting_amount = 4000e+18

    dao_token_contract.transfer(
        vesting_contract, 10000e+18, {"from": dao_token_owner}
    )

    # Action
    tx = vesting_contract.createVestingSchedule(
        beneficiary,
        start_vesting_time,
        cliff_period_seconds,
        vesting_duration_seconds,
        slice_period_seconds,
        revocable,
        vesting_amount,
        {"from": vesting_owner}
    )

    return {
        "beneficiary": beneficiary,
        "vesting_schedule_id": str(tx.events['CreatedVestingSchedule']['vestingScheduleId']),
    }


def test_success__release_all__by_owner(vesting_deployment, data_test):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    beneficiary = data_test['beneficiary']
    vesting_schedule_id = data_test['vesting_schedule_id']

    # Assert before actions
    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) == 0
    assert vesting_contract.getVestingSchedulesTotalAmount() == 4000e+18

    # Action
    tx = vesting_contract.releaseAll(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert: Released Event
    assert ('Released' in tx.events) is True
    assert str(tx.events['Released']['vestingScheduleId']) == vesting_schedule_id
    assert tx.events['Released']['beneficiary'] == beneficiary
    assert tx.events['Released']['amount'] == 333333333333333333333

    # Assert: Balance of beneficiary
    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) \
           == 333333333333333333333
    assert vesting_contract.getVestingSchedulesTotalAmount() \
           == 3666666666666666666667


def test_success__release_all__by_beneficiary(vesting_deployment, data_test):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    beneficiary = data_test['beneficiary']
    vesting_schedule_id = data_test['vesting_schedule_id']

    # Assert before actions
    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) == 0
    assert vesting_contract.getVestingSchedulesTotalAmount() == 4000e+18

    # Action
    tx = vesting_contract.releaseAll(
        vesting_schedule_id,
        {"from": beneficiary}
    )

    # Assert: Released Event
    # Assert: Released Event
    assert ('Released' in tx.events) is True
    assert str(tx.events['Released']['vestingScheduleId']) == vesting_schedule_id
    assert tx.events['Released']['beneficiary'] == beneficiary
    assert tx.events['Released']['amount'] == 333333333333333333333

    # Assert: Balance of beneficiary
    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) \
           == 333333333333333333333
    assert vesting_contract.getVestingSchedulesTotalAmount() \
           == 3666666666666666666667


def test_failure__release_all__by_fake_beneficiary(vesting_deployment, data_test):
    # Arranges
    vesting_contract = vesting_deployment['token_vesting_contract']
    fake_beneficiary = accounts.add()
    vesting_schedule_id = data_test['vesting_schedule_id']

    # Action
    with brownie.reverts("TokenVesting: only beneficiary "
                         "and owner can release vested tokens"):
        vesting_contract.releaseAll(
            vesting_schedule_id,
            {"from": fake_beneficiary}
        )


def test_failure__release_all__revoked_schedule(vesting_deployment, data_test):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    vesting_schedule_id = data_test['vesting_schedule_id']

    # Revoke schedule
    vesting_contract.revoke(vesting_schedule_id, {"from": vesting_owner})

    # Action
    with brownie.reverts("Schedule has been revoked"):
        vesting_contract.releaseAll(
            vesting_schedule_id, {"from": vesting_owner}
        )


def test_failure__release_all__not_enough_vested_amount(
        vesting_deployment, util
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']

    beneficiary = accounts.add()
    current_timestamp = util.get_timestamp()
    start_vesting_time = current_timestamp - 100
    cliff_period_seconds = 200
    vesting_duration_seconds = 600
    slice_period_seconds = 50
    revocable = True
    vesting_amount = 4000e+18

    dao_token_contract.transfer(
        vesting_contract, 10000e+18, {"from": dao_token_owner}
    )

    # Action
    tx = vesting_contract.createVestingSchedule(
        beneficiary,
        start_vesting_time,
        cliff_period_seconds,
        vesting_duration_seconds,
        slice_period_seconds,
        revocable,
        vesting_amount,
        {"from": vesting_owner}
    )

    vesting_schedule_id = str(
        tx.events['CreatedVestingSchedule']['vestingScheduleId']
    )

    # Action
    with brownie.reverts("TokenVesting: cannot release tokens, "
                         "not enough vested tokens"):
        vesting_contract.releaseAll(
            vesting_schedule_id, {"from": vesting_owner}
        )
