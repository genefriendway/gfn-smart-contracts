import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_reserve_percent_for_quarter_referral_reward(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']
    percent = 20

    # Action
    tx = configuration_contract.setReservePercentForQuarterReferralReward(
        percent,
        {"from": configuration_owner}
    )
    # Assert: SetReservePercentForQuarterReferralReward Event
    assert ('SetReservePercentForQuarterReferralReward' in tx.events) is True
    assert tx.events['SetReservePercentForQuarterReferralReward']['percent'] \
           == percent

    # Assert
    assert configuration_contract.getReservePercentForQuarterReferralReward() \
           == percent


def test_failure__set_reserve_percent_for_quarter_referral_reward__invalid_owner_make_txn(
        advocate_deployment
):
    # Arrange
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']
    another_owner = accounts.add()
    percent = 20

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        configuration_contract.setReservePercentForQuarterReferralReward(
            percent,
            {"from": another_owner}
        )
