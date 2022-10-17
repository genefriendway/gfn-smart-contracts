import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_min_max_referral__new_level(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 2
    new_min_referral = 120
    new_max_referral = 180

    # Assert Before Action
    assert configuration_contract.calculateAdvocateRewardPercent(150) == 30

    # Action
    tx = configuration_contract.setMinMaxReferralForAdvocateLevel(
        level, new_min_referral, new_max_referral,
        {"from": configuration_owner}
    )

    # Assert Level Count
    assert configuration_contract.getLevelCount() == 4

    # Assert: SetMinMaxReferralForAdvocateLevel Event
    assert ('SetMinMaxReferralForAdvocateLevel' in tx.events) is True
    assert tx.events['SetMinMaxReferralForAdvocateLevel']['levelNumber'] == level
    assert tx.events['SetMinMaxReferralForAdvocateLevel']['minReferral'] == new_min_referral
    assert tx.events['SetMinMaxReferralForAdvocateLevel']['maxReferral'] == new_max_referral

    # Assert
    assert configuration_contract.getAdvocateMinReferral(level) == new_min_referral
    assert configuration_contract.getAdvocateMaxReferral(level) == new_max_referral
    assert configuration_contract.getAdvocateRewardPercent(level) == 30
    assert configuration_contract.getAdvocateLevelStatus(level) is True

    # Assert: Calculation
    assert configuration_contract.calculateAdvocateRewardPercent(150) == 30


def test_failure__set_min_max_referral__invalid_owner_make_txn(
        advocate_deployment
):
    # Arrange
    another_owner = accounts.add()
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 2
    new_min_referral = 120
    new_max_referral = 180

    # Assert Before Action
    assert configuration_contract.calculateAdvocateRewardPercent(150) == 30

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        configuration_contract.setMinMaxReferralForAdvocateLevel(
            level, new_min_referral, new_max_referral,
            {"from": another_owner}
        )


def test_failure__set_min_max_referral__not_existed_level(
        advocate_deployment
):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 10
    new_min_referral = 120
    new_max_referral = 180

    # Assert Before Action
    assert configuration_contract.calculateAdvocateRewardPercent(150) == 30

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: level number must be existed"):
        configuration_contract.setMinMaxReferralForAdvocateLevel(
            level, new_min_referral, new_max_referral,
            {"from": configuration_owner}
        )


def test_failure__set_min_max_referral__min_greater_than_max(
        advocate_deployment
):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 2
    new_min_referral = 180
    new_max_referral = 120

    # Assert Before Action
    assert configuration_contract.calculateAdvocateRewardPercent(150) == 30

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: min referral must "
                         "be less than max referral"):
        configuration_contract.setMinMaxReferralForAdvocateLevel(
            level, new_min_referral, new_max_referral,
            {"from": configuration_owner}
        )


def test_failure__set_min_max_referral__min_max_still_same_current_value(
        advocate_deployment
):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 2
    new_min_referral = 100
    new_max_referral = 199

    # Assert Before Action
    assert configuration_contract.calculateAdvocateRewardPercent(150) == 30

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: min or max referral "
                         "must differ from current value"):
        configuration_contract.setMinMaxReferralForAdvocateLevel(
            level, new_min_referral, new_max_referral,
            {"from": configuration_owner}
        )