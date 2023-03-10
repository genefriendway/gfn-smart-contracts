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

    dao_token_contract.transfer(
        vesting_contract, 10000e+18, {"from": dao_token_owner}
    )

    def prepare_vesting_schedule(back_seconds_from_current, revocable=True):
        current_timestamp = util.get_timestamp()
        start_vesting_time = current_timestamp - back_seconds_from_current
        cliff_period_seconds = 200
        vesting_duration_seconds = 600
        slice_period_seconds = 50
        vesting_amount = 4000e+18

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
        vesting_schedule_id = str(tx.events['CreatedVestingSchedule']['vestingScheduleId'])
        return vesting_schedule_id

    # create vesting schedule


    return {
        "beneficiary": beneficiary,
        "prepare_vesting_schedule": prepare_vesting_schedule,
    }


def test_success__revoke__after_first_slice(vesting_deployment, data_test):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    beneficiary = data_test['beneficiary']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(250, revocable=True)

    # Assert before actions
    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) == 0
    assert vesting_contract.getVestingSchedulesTotalAmount() == 4000e+18

    # Action
    tx = vesting_contract.revoke(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert: Released Event
    assert ('Released' in tx.events) is True
    assert str(tx.events['Released']['vestingScheduleId']) == vesting_schedule_id
    assert tx.events['Released']['beneficiary'] == beneficiary
    assert tx.events['Released']['amount'] == 333333333333333333333

    assert ('Revoked' in tx.events) is True
    assert str(tx.events['Revoked']['vestingScheduleId']) == vesting_schedule_id
    assert tx.events['Revoked']['vestedAmount'] == 333333333333333333333
    assert tx.events['Revoked']['unreleasedAmount'] == 3666666666666666666667

    # Assert: Balance of beneficiary
    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) \
           == 333333333333333333333
    assert vesting_contract.getVestingSchedulesTotalAmount() == 0

    assert vesting_contract.getWithdrawableAmount() == 9666666666666666666667


def test_success__revoke__after_second_slice(
        vesting_deployment, data_test
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    beneficiary = data_test['beneficiary']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(310, revocable=True)

    # Assert before actions
    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) == 0
    assert vesting_contract.getVestingSchedulesTotalAmount() == 4000e+18

    # Action
    tx = vesting_contract.revoke(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert: Released Event
    assert ('Released' in tx.events) is True
    assert str(tx.events['Released']['vestingScheduleId']) == vesting_schedule_id
    assert tx.events['Released']['beneficiary'] == beneficiary
    assert tx.events['Released']['amount'] == 666666666666666666666

    assert ('Revoked' in tx.events) is True
    assert str(tx.events['Revoked']['vestingScheduleId']) == vesting_schedule_id
    assert tx.events['Revoked']['vestedAmount'] == 666666666666666666666
    assert tx.events['Revoked']['unreleasedAmount'] == 3333333333333333333334

    # Assert: Balance of beneficiary
    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) \
           == 666666666666666666666
    assert vesting_contract.getVestingSchedulesTotalAmount() == 0

    assert vesting_contract.getWithdrawableAmount() == 9333333333333333333334


def test_success__revoke__before_first_slice(
        vesting_deployment, data_test
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    beneficiary = data_test['beneficiary']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(220, revocable=True)

    # Assert before actions
    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) == 0
    assert vesting_contract.getVestingSchedulesTotalAmount() == 4000e+18

    # Action
    tx = vesting_contract.revoke(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert: Released Event
    assert ('Released' in tx.events) is False

    assert ('Revoked' in tx.events) is True
    assert str(tx.events['Revoked']['vestingScheduleId']) == vesting_schedule_id
    assert tx.events['Revoked']['vestedAmount'] == 0
    assert tx.events['Revoked']['unreleasedAmount'] == 4000e+18

    # Assert: Balance of beneficiary
    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) \
           == 0
    assert vesting_contract.getVestingSchedulesTotalAmount() == 0

    assert vesting_contract.getWithdrawableAmount() == 10000e+18


def test_success__revoke__before_cliff(
        vesting_deployment, data_test
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    beneficiary = data_test['beneficiary']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(10, revocable=True)

    # Assert before actions
    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) == 0
    assert vesting_contract.getVestingSchedulesTotalAmount() == 4000e+18

    # Action
    tx = vesting_contract.revoke(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert: Released Event
    assert ('Released' in tx.events) is False

    assert ('Revoked' in tx.events) is True
    assert str(tx.events['Revoked']['vestingScheduleId']) == vesting_schedule_id
    assert tx.events['Revoked']['vestedAmount'] == 0
    assert tx.events['Revoked']['unreleasedAmount'] == 4000e+18

    # Assert: Balance of beneficiary
    assert dao_token_contract.balanceOf(beneficiary, {"from": dao_token_owner}) \
           == 0
    assert vesting_contract.getVestingSchedulesTotalAmount() == 0

    assert vesting_contract.getWithdrawableAmount() == 10000e+18


def test_failure__revoke__not_revocable(vesting_deployment, data_test):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']
    vesting_schedule_id2 = prepare_vesting_schedule(250, revocable=False)

    # Action
    with brownie.reverts("TokenVesting: vesting is not revocable"):
        vesting_contract.revoke(
            vesting_schedule_id2, {"from": vesting_owner}
        )


def test_failure__revoke__duplicated_revoke(vesting_deployment, data_test):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']
    vesting_schedule_id = prepare_vesting_schedule(250, revocable=True)

    # Action
    vesting_contract.revoke(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Action: Revoke again
    with brownie.reverts("Schedule has been revoked"):
        vesting_contract.revoke(
            vesting_schedule_id, {"from": vesting_owner}
        )


def test_failure__revoke__by_fake_owner(vesting_deployment, data_test):
    # Arranges
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']
    vesting_schedule_id = prepare_vesting_schedule(250, revocable=True)

    fake_owner = accounts.add()

    # Action:
    with brownie.reverts("Ownable: caller is not the owner"):
        vesting_contract.revoke(
            vesting_schedule_id, {"from": fake_owner}
        )


def test_failure__revoke__by_beneficiary(vesting_deployment, data_test):
    # Arranges
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']
    beneficiary = data_test['beneficiary']
    vesting_schedule_id = prepare_vesting_schedule(250, revocable=True)

    # Action:
    with brownie.reverts("Ownable: caller is not the owner"):
        vesting_contract.revoke(
            vesting_schedule_id, {"from": beneficiary}
        )