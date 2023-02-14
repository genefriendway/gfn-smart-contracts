import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_advocate_level__new_level(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 4
    min_referral = 300
    max_referral = 399
    reward_percent = 45
    is_active = True

    # Assert Before Action
    assert configuration_contract.getLevelCount() == 4
    assert configuration_contract.calculateAdvocateRewardPercent(350) == 50
    assert configuration_contract.calculateAdvocateRewardPercent(1000) == 50

    # Action
    tx = configuration_contract.setAdvocateLevel(
        level, min_referral, max_referral, reward_percent, is_active,
        {"from": configuration_owner}
    )

    # Assert Level Count
    assert configuration_contract.getLevelCount() == 4

    # Assert: SetAdvocateLevel Event
    assert ('SetAdvocateLevel' in tx.events) is True
    assert tx.events['SetAdvocateLevel']['levelNumber'] == level
    assert tx.events['SetAdvocateLevel']['minReferral'] == min_referral
    assert tx.events['SetAdvocateLevel']['maxReferral'] == max_referral
    assert tx.events['SetAdvocateLevel']['rewardPercent'] == reward_percent
    assert tx.events['SetAdvocateLevel']['isActive'] is True

    # Assert
    assert configuration_contract.getAdvocateMinReferral(level) == min_referral
    assert configuration_contract.getAdvocateMaxReferral(level) == max_referral
    assert configuration_contract.getAdvocateRewardPercent(level) == reward_percent
    assert configuration_contract.getAdvocateLevelStatus(level) is True

    # Assert: Calculation
    assert configuration_contract.calculateAdvocateRewardPercent(350) == 45
    assert configuration_contract.calculateAdvocateRewardPercent(1000) == 0


def test_failure__set_advocate_level__invalid_owner_make_txn(
        advocate_deployment
):
    # Arrange
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']
    another_owner = accounts.add()

    level = 4
    min_referral = 400
    max_referral = 600
    reward_percent = 25
    is_active = True

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        configuration_contract.setAdvocateLevel(
            level, min_referral, max_referral, reward_percent, is_active,
            {"from": another_owner}
        )


def test_failure__set_advocate_level__not_existed_level(
        advocate_deployment
):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 5  # this level not existed
    min_referral = 400
    max_referral = 600
    reward_percent = 25
    is_active = True

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: level number must be existed"):
        configuration_contract.setAdvocateLevel(
            level, min_referral, max_referral, reward_percent, is_active,
            {"from": configuration_owner}
        )


def test_failure__set_advocate_level__new_percent_equal_0(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 4
    min_referral = 400
    max_referral = 600
    reward_percent = 0
    is_active = True

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: reward percent must "
                         "be greater than zero"):
        configuration_contract.setAdvocateLevel(
            level, min_referral, max_referral, reward_percent, is_active,
            {"from": configuration_owner}
        )
