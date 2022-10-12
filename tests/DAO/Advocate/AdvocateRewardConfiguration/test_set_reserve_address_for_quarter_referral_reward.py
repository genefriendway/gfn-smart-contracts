import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_reserve_address_for_quarter_referral_reward(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']
    reserve_address = accounts.add()

    # Action
    tx = configuration_contract.setReserveAddressForQuarterReferralReward(
        reserve_address,
        {"from": configuration_owner}
    )
    # Assert: SetReserveAddressForQuarterReferralReward Event
    assert ('SetReserveAddressForQuarterReferralReward' in tx.events) is True
    assert tx.events['SetReserveAddressForQuarterReferralReward']['reserveAddress'] \
           == reserve_address

    # Assert
    assert configuration_contract.getReserveAddressForQuarterReferralReward() \
           == reserve_address


def test_failure__set_reserve_address_for_quarter_referral_reward__invalid_owner_make_txn(
        advocate_deployment
):
    # Arrange
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']
    another_owner = accounts.add()
    reserve_address = accounts.add()

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        configuration_contract.setReserveAddressForQuarterReferralReward(
            reserve_address,
            {"from": another_owner}
        )
