import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_reward_percent(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 3
    new_reward_percent = 45

    # Assert Before Action
    assert configuration_contract.calculateAdvocateRewardPercent(250) == 40

    # Action
    tx = configuration_contract.setRewardPercentForAdvocateLevel(
        level, new_reward_percent, {"from": configuration_owner}
    )

    # Assert Level Count
    assert configuration_contract.getLevelCount() == 4

    # Assert: SetRewardPercentForAdvocateLevel Event
    assert ('SetRewardPercentForAdvocateLevel' in tx.events) is True
    assert tx.events['SetRewardPercentForAdvocateLevel']['levelNumber'] == level
    assert tx.events['SetRewardPercentForAdvocateLevel']['rewardPercent'] == new_reward_percent

    # Assert
    assert configuration_contract.getAdvocateMinReferral(level) == 200
    assert configuration_contract.getAdvocateMaxReferral(level) == 299
    assert configuration_contract.getAdvocateRewardPercent(level) == 45
    assert configuration_contract.getAdvocateLevelStatus(level) is True

    # Assert: Calculation
    assert configuration_contract.calculateAdvocateRewardPercent(199) == 30
    assert configuration_contract.calculateAdvocateRewardPercent(200) == 45
    assert configuration_contract.calculateAdvocateRewardPercent(250) == 45
    assert configuration_contract.calculateAdvocateRewardPercent(299) == 45
    assert configuration_contract.calculateAdvocateRewardPercent(300) == 50


def test_failure__set_reward_percent__invalid_owner_make_txn(
        advocate_deployment
):
    # Arrange
    another_owner = accounts.add()
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 3
    new_reward_percent = 45

    # Assert Before Action
    assert configuration_contract.calculateAdvocateRewardPercent(250) == 40

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        configuration_contract.setRewardPercentForAdvocateLevel(
            level, new_reward_percent, {"from": another_owner}
        )
        
    assert configuration_contract.calculateAdvocateRewardPercent(250) == 40


def test_failure__set_reward_percent__not_existed_level(
        advocate_deployment
):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 10
    new_reward_percent = 250

    # Assert Before Action
    assert configuration_contract.calculateAdvocateRewardPercent(250) == 40

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: level number must be existed"):
        configuration_contract.setRewardPercentForAdvocateLevel(
            level, new_reward_percent, {"from": configuration_owner}
        )

    assert configuration_contract.calculateAdvocateRewardPercent(250) == 40


def test_failure__set_reward_percent__reward_percent_equal_to_zero(
        advocate_deployment
):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 3
    new_reward_percent = 0

    # Assert Before Action
    assert configuration_contract.calculateAdvocateRewardPercent(250) == 40

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: reward percent must "
                         "be greater than zero"):
        configuration_contract.setRewardPercentForAdvocateLevel(
            level, new_reward_percent, {"from": configuration_owner}
        )

    assert configuration_contract.calculateAdvocateRewardPercent(250) == 40


def test_failure__set_reward_percent__percent_same_current_value(
        advocate_deployment
):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 3
    new_reward_percent = 40  # current value is also 40

    # Assert Before Action
    assert configuration_contract.calculateAdvocateRewardPercent(250) == 40

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: reward percent must "
                         "differ from current value"):
        configuration_contract.setRewardPercentForAdvocateLevel(
            level, new_reward_percent,
            {"from": configuration_owner}
        )

    assert configuration_contract.calculateAdvocateRewardPercent(250) == 40