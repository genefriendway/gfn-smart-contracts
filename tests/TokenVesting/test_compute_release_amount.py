import pytest

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

    def prepare_vesting_schedule(back_seconds_from_current, revocable=True):
        beneficiary = accounts.add()
        current_timestamp = util.get_timestamp()
        start_vesting_time = current_timestamp - back_seconds_from_current
        cliff_period_seconds = 200
        vesting_duration_seconds = 600
        slice_period_seconds = 120
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

    dao_token_contract.transfer(
        vesting_contract, 10000e+18, {"from": dao_token_owner}
    )

    return {
        "prepare_vesting_schedule": prepare_vesting_schedule
    }


def test_success__compute__current_time_lt_cliff_time(
        vesting_deployment, data_test, util
):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(150)

    # Action
    vested_amount = vesting_contract.computeReleasableAmount(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert:
    assert vested_amount == 0


def test_success__compute__current_time_eq_cliff_time(
        vesting_deployment, data_test, util
):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(200)

    # Action
    vested_amount = vesting_contract.computeReleasableAmount(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert:
    assert vested_amount == 0


def test_success__compute__current_time_gt_cliff_time_and_lt_first_slice(
        vesting_deployment, data_test, util
):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(319)

    # Action
    vested_amount = vesting_contract.computeReleasableAmount(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert:
    assert vested_amount == 0


def test_success__compute__current_time_eq_first_slice(
        vesting_deployment, data_test, util
):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(320)

    # Action 1
    vested_amount = vesting_contract.computeReleasableAmount(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert:
    assert vested_amount == 800e+18


def test_success__compute__current_time_gt_first_slice_and_lt_second_slice(
        vesting_deployment, data_test, util
):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(320)

    # Action
    vested_amount = vesting_contract.computeReleasableAmount(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert:
    assert vested_amount == 800e+18


def test_success__compute__current_time_eq_second_slice(
        vesting_deployment, data_test, util
):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(440)

    # Action
    vested_amount = vesting_contract.computeReleasableAmount(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert:
    assert vested_amount == 1600e+18


def test_success__compute__current_time_gt_second_slice_and_le_third_slice(
        vesting_deployment, data_test, util
):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(500)

    # Action
    vested_amount = vesting_contract.computeReleasableAmount(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert:
    assert vested_amount == 1600e+18


def test_success__compute__current_time_eq_third_slice(
        vesting_deployment, data_test, util
):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(560)

    # Action
    vested_amount = vesting_contract.computeReleasableAmount(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert:
    assert vested_amount == 2400e+18


def test_success__compute__current_time_gt_third_slice_and_lt_fourth_slice(
        vesting_deployment, data_test, util
):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(560)

    # Action
    vested_amount = vesting_contract.computeReleasableAmount(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert:
    assert vested_amount == 2400e+18


def test_success__compute__current_time_eq_fifth_slice(
        vesting_deployment, data_test, util
):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(800)

    # Action
    vested_amount = vesting_contract.computeReleasableAmount(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert:
    assert vested_amount == 4000e+18


def test_success__compute__current_time_gt_fifth_slice(
        vesting_deployment, data_test, util
):
    # Arranges
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']
    prepare_vesting_schedule = data_test['prepare_vesting_schedule']

    vesting_schedule_id = prepare_vesting_schedule(1000)

    # Action
    vested_amount = vesting_contract.computeReleasableAmount(
        vesting_schedule_id, {"from": vesting_owner}
    )

    # Assert:
    assert vested_amount == 4000e+18
