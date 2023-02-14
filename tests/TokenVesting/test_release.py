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


def test_success__release(vesting_deployment, data_test):
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
    tx = vesting_contract.release(
        vesting_schedule_id,
        100e+18,
        {"from": vesting_owner}
    )

    # Assert: Released Event
    assert ('Released' in tx.events) is True
    assert str(tx.events['Released']['vestingScheduleId']) == vesting_schedule_id
    assert tx.events['Released']['beneficiary'] == beneficiary
    assert tx.events['Released']['amount'] == 100e+18

    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) \
           == 100e+18
    assert vesting_contract.getVestingSchedulesTotalAmount() == 3900e+18
