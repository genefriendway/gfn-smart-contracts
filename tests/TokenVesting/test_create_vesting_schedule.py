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


def test_success__create_schedule__vesting_amount_lt_balance(
        vesting_deployment, util
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']

    dao_token_contract.transfer(
        vesting_contract, 10000e+18, {"from": dao_token_owner}
    )

    beneficiary = accounts.add()
    start_vesting_time = 1660808868
    cliff_period_seconds = 10 * 24 * 60 * 60  # 10 days
    vesting_duration_seconds = 40 * 24 * 60 * 60  # 40 days
    slice_period_seconds = 5 * 24 * 60 * 60  # 5 days
    revocable = True
    vesting_amount = 4000e+18

    # Assert before action
    assert vesting_contract.getVestingSchedulesCountByBeneficiary(beneficiary) == 0

    assert vesting_contract.getWithdrawableAmount() == 10000e+18
    assert vesting_contract.getVestingSchedulesTotalAmount() == 0

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

    # Assert: CreatedVestingSchedule Event
    assert ('CreatedVestingSchedule' in tx.events) is True
    assert tx.events['CreatedVestingSchedule']['vestingScheduleId'] is not None
    assert tx.events['CreatedVestingSchedule']['beneficiary'] == beneficiary
    assert tx.events['CreatedVestingSchedule']['start'] == 1660808868
    assert tx.events['CreatedVestingSchedule']['cliff'] == 1661672868
    assert tx.events['CreatedVestingSchedule']['duration'] == 3456000
    assert tx.events['CreatedVestingSchedule']['slicePeriodSeconds'] == 432000
    assert tx.events['CreatedVestingSchedule']['revocable'] is True
    assert tx.events['CreatedVestingSchedule']['amount'] == 4000e+18

    # Assert vesting_contract
    assert vesting_contract.getVestingSchedulesCountByBeneficiary(beneficiary) == 1
    assert vesting_contract.getWithdrawableAmount() == 6000e+18
    assert vesting_contract.getVestingSchedulesTotalAmount() == 4000e+18

    vesting_schedule_id = vesting_contract.computeVestingScheduleIdForAddressAndIndex(
        beneficiary, 0
    )
    assert str(tx.events['CreatedVestingSchedule']['vestingScheduleId']) == str(vesting_schedule_id)
    assert str(vesting_contract.getVestingIdAtIndex(0)) == str(vesting_schedule_id)


def test_success__create_schedule__vesting_amount_eq_balance(
        vesting_deployment, util
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']

    dao_token_contract.transfer(
        vesting_contract, 10000e+18, {"from": dao_token_owner}
    )

    beneficiary = accounts.add()
    start_vesting_time = 1660808868
    cliff_period_seconds = 10 * 24 * 60 * 60  # 10 days
    vesting_duration_seconds = 40 * 24 * 60 * 60  # 40 days
    slice_period_seconds = 5 * 24 * 60 * 60  # 5 days
    revocable = True
    vesting_amount = 10000e+18

    # Assert before action
    assert vesting_contract.getVestingSchedulesCountByBeneficiary(beneficiary) == 0

    assert vesting_contract.getWithdrawableAmount() == 10000e+18
    assert vesting_contract.getVestingSchedulesTotalAmount() == 0

    # Action
    vesting_contract.createVestingSchedule(
        beneficiary,
        start_vesting_time,
        cliff_period_seconds,
        vesting_duration_seconds,
        slice_period_seconds,
        revocable,
        vesting_amount,
        {"from": vesting_owner}
    )

    # Make a Transaction to withdraw
    with brownie.reverts("TokenVesting: not enough withdrawable funds"):
        vesting_contract.withdraw(1e+18, {"from": vesting_owner})


def test_failure__create_schedule__not_owner(
        vesting_deployment, util
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']

    dao_token_contract.transfer(
        vesting_contract, 10000e+18, {"from": dao_token_owner}
    )
    fake_owner = accounts.add()

    beneficiary = accounts.add()
    start_vesting_time = 1660808868
    cliff_period_seconds = 10 * 24 * 60 * 60  # 10 days
    vesting_duration_seconds = 40 * 24 * 60 * 60  # 40 days
    slice_period_seconds = 5 * 24 * 60 * 60  # 5 days
    revocable = True
    vesting_amount = 10000e+18

    # Assert before action
    assert vesting_contract.getVestingSchedulesCountByBeneficiary(beneficiary) == 0

    assert vesting_contract.getWithdrawableAmount() == 10000e+18
    assert vesting_contract.getVestingSchedulesTotalAmount() == 0

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        vesting_contract.createVestingSchedule(
            beneficiary,
            start_vesting_time,
            cliff_period_seconds,
            vesting_duration_seconds,
            slice_period_seconds,
            revocable,
            vesting_amount,
            {"from": fake_owner}
        )


def test_failure__create_schedule__vesting_amount_gt_balance(
        vesting_deployment, util
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']

    dao_token_contract.transfer(
        vesting_contract, 10000e+18, {"from": dao_token_owner}
    )

    beneficiary = accounts.add()
    start_vesting_time = 1660808868
    cliff_period_seconds = 10 * 24 * 60 * 60  # 10 days
    vesting_duration_seconds = 40 * 24 * 60 * 60  # 40 days
    slice_period_seconds = 5 * 24 * 60 * 60  # 5 days
    revocable = True
    vesting_amount = 10001e+18  # > 10000e+18

    # Assert before action
    assert vesting_contract.getVestingSchedulesCountByBeneficiary(beneficiary) == 0

    assert vesting_contract.getWithdrawableAmount() == 10000e+18
    assert vesting_contract.getVestingSchedulesTotalAmount() == 0

    # Action
    with brownie.reverts("TokenVesting: cannot create vesting schedule "
                         "because not sufficient tokens"):
        vesting_contract.createVestingSchedule(
            beneficiary,
            start_vesting_time,
            cliff_period_seconds,
            vesting_duration_seconds,
            slice_period_seconds,
            revocable,
            vesting_amount,
            {"from": vesting_owner}
        )


def test_failure__create_schedule__duration_eq_0(
        vesting_deployment, util
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']

    dao_token_contract.transfer(
        vesting_contract, 10000e+18, {"from": dao_token_owner}
    )

    beneficiary = accounts.add()
    start_vesting_time = 1660808868
    cliff_period_seconds = 10 * 24 * 60 * 60  # 10 days
    vesting_duration_seconds = 0
    slice_period_seconds = 5 * 24 * 60 * 60  # 5 days
    revocable = True
    vesting_amount = 10000e+18

    # Assert before action
    assert vesting_contract.getVestingSchedulesCountByBeneficiary(beneficiary) == 0

    assert vesting_contract.getWithdrawableAmount() == 10000e+18
    assert vesting_contract.getVestingSchedulesTotalAmount() == 0

    # Action
    with brownie.reverts("TokenVesting: duration must be > 0"):
        vesting_contract.createVestingSchedule(
            beneficiary,
            start_vesting_time,
            cliff_period_seconds,
            vesting_duration_seconds,
            slice_period_seconds,
            revocable,
            vesting_amount,
            {"from": vesting_owner}
        )


def test_failure__create_schedule__vesting_amount_eq_0(
        vesting_deployment, util
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']

    dao_token_contract.transfer(
        vesting_contract, 10000e+18, {"from": dao_token_owner}
    )

    beneficiary = accounts.add()
    start_vesting_time = 1660808868
    cliff_period_seconds = 10 * 24 * 60 * 60  # 10 days
    vesting_duration_seconds = 40 * 24 * 60 * 60  # 40 days
    slice_period_seconds = 5 * 24 * 60 * 60  # 5 days
    revocable = True
    vesting_amount = 0

    # Assert before action
    assert vesting_contract.getVestingSchedulesCountByBeneficiary(beneficiary) == 0

    assert vesting_contract.getWithdrawableAmount() == 10000e+18
    assert vesting_contract.getVestingSchedulesTotalAmount() == 0

    # Action
    with brownie.reverts("TokenVesting: amount must be > 0"):
        vesting_contract.createVestingSchedule(
            beneficiary,
            start_vesting_time,
            cliff_period_seconds,
            vesting_duration_seconds,
            slice_period_seconds,
            revocable,
            vesting_amount,
            {"from": vesting_owner}
        )


def test_failure__create_schedule__slice_eq_0(
        vesting_deployment, util
):
    # Arranges
    dao_token_owner = vesting_deployment['dao_token_owner']
    dao_token_contract = vesting_deployment['dao_token_contract']
    vesting_owner = vesting_deployment['token_vesting_owner']
    vesting_contract = vesting_deployment['token_vesting_contract']

    dao_token_contract.transfer(
        vesting_contract, 10000e+18, {"from": dao_token_owner}
    )

    beneficiary = accounts.add()
    start_vesting_time = 1660808868
    cliff_period_seconds = 10 * 24 * 60 * 60  # 10 days
    vesting_duration_seconds = 40 * 24 * 60 * 60  # 40 days
    slice_period_seconds = 0
    revocable = True
    vesting_amount = 10000e+18

    # Assert before action
    assert vesting_contract.getVestingSchedulesCountByBeneficiary(beneficiary) == 0

    assert vesting_contract.getWithdrawableAmount() == 10000e+18
    assert vesting_contract.getVestingSchedulesTotalAmount() == 0

    # Action
    with brownie.reverts("TokenVesting: slicePeriodSeconds must be >= 1"):
        vesting_contract.createVestingSchedule(
            beneficiary,
            start_vesting_time,
            cliff_period_seconds,
            vesting_duration_seconds,
            slice_period_seconds,
            revocable,
            vesting_amount,
            {"from": vesting_owner}
        )
