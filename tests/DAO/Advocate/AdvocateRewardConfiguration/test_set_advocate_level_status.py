import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_status(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 4
    new_status = False

    # Assert Before Action
    assert configuration_contract.getAdvocateLevelStatus(level) is True
    assert configuration_contract.calculateAdvocateRewardPercent(300) == 50

    # Action
    tx = configuration_contract.setAdvocateLevelStatus(
        level, new_status, {"from": configuration_owner}
    )

    # Assert Level Count
    assert configuration_contract.getLevelCount() == 4

    # Assert: SetAdvocateLevelStatus Event
    assert ('SetAdvocateLevelStatus' in tx.events) is True
    assert tx.events['SetAdvocateLevelStatus']['levelNumber'] == level
    assert tx.events['SetAdvocateLevelStatus']['isActive'] == new_status

    # Assert
    assert configuration_contract.getAdvocateMinReferral(level) == 300
    assert configuration_contract.getAdvocateMaxReferral(level) == 99999999
    assert configuration_contract.getAdvocateRewardPercent(level) == 50
    assert configuration_contract.getAdvocateLevelStatus(level) is False

    # Assert: Calculation
    assert configuration_contract.calculateAdvocateRewardPercent(300) == 0


def test_failure__set_status__invalid_owner_make_txn(
        advocate_deployment
):
    # Arrange
    another_owner = accounts.add()
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 4
    new_status = False

    # Assert Before Action
    assert configuration_contract.getAdvocateLevelStatus(level) is True
    assert configuration_contract.calculateAdvocateRewardPercent(300) == 50

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        configuration_contract.setAdvocateLevelStatus(
            level, new_status, {"from": another_owner}
        )
        
    assert configuration_contract.calculateAdvocateRewardPercent(350) == 50


def test_failure__set_status__not_existed_level(
        advocate_deployment
):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 10
    new_status = False

    # Assert Before Action
    assert configuration_contract.getAdvocateLevelStatus(level) is False

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: level number must be existed"):
        configuration_contract.setAdvocateLevelStatus(
            level, new_status, {"from": configuration_owner}
        )

    assert configuration_contract.getAdvocateLevelStatus(level) is False


def test_failure__set_status__status_same_current_value(
        advocate_deployment
):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    level = 4
    new_status = True

    # Assert Before Action
    assert configuration_contract.getAdvocateLevelStatus(level) is True
    assert configuration_contract.calculateAdvocateRewardPercent(300) == 50

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: status must differ "
                         "from current value"):
        configuration_contract.setAdvocateLevelStatus(
            level, new_status,
            {"from": configuration_owner}
        )

    assert configuration_contract.calculateAdvocateRewardPercent(350) == 50