import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__add_advocate_level__level_5(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    min_referral = 100000000
    max_referral = 200000000
    reward_percent = 60
    is_active = True

    # Assert Before Actions
    assert configuration_contract.getLevelCount() == 4

    # Action
    tx = configuration_contract.addAdvocateLevel(
        min_referral, max_referral, reward_percent, is_active,
        {"from": configuration_owner}
    )

    # Assert: Level Count
    assert configuration_contract.getLevelCount() == 5

    # Assert: AddAdvocateLevel Event
    assert ('AddAdvocateLevel' in tx.events) is True
    assert tx.events['AddAdvocateLevel']['levelNumber'] == 5
    assert tx.events['AddAdvocateLevel']['minReferral'] == min_referral
    assert tx.events['AddAdvocateLevel']['maxReferral'] == max_referral
    assert tx.events['AddAdvocateLevel']['rewardPercent'] == reward_percent
    assert tx.events['AddAdvocateLevel']['isActive'] is True

    # Assert Detail Advocate Level
    assert configuration_contract.getAdvocateMinReferral(5) == min_referral
    assert configuration_contract.getAdvocateMaxReferral(5) == max_referral
    assert configuration_contract.getAdvocateRewardPercent(5) == reward_percent
    assert configuration_contract.getAdvocateLevelStatus(5) is True

    # New Arranges
    min_referral = 200000001
    max_referral = 300000000
    reward_percent = 60
    is_active = True

    # Next Action
    tx = configuration_contract.addAdvocateLevel(
        min_referral, max_referral, reward_percent, is_active,
        {"from": configuration_owner}
    )

    # Assert: Level Count
    assert configuration_contract.getLevelCount() == 6

    # Assert: AddAdvocateLevel Event
    assert ('AddAdvocateLevel' in tx.events) is True
    assert tx.events['AddAdvocateLevel']['levelNumber'] == 6
    assert tx.events['AddAdvocateLevel']['minReferral'] == min_referral
    assert tx.events['AddAdvocateLevel']['maxReferral'] == max_referral
    assert tx.events['AddAdvocateLevel']['rewardPercent'] == reward_percent
    assert tx.events['AddAdvocateLevel']['isActive'] is True

    # Assert Detail Advocate Level
    assert configuration_contract.getAdvocateMinReferral(6) == min_referral
    assert configuration_contract.getAdvocateMaxReferral(6) == max_referral
    assert configuration_contract.getAdvocateRewardPercent(6) == reward_percent
    assert configuration_contract.getAdvocateLevelStatus(6) is True


def test_failure__add_advocate_level__invalid_owner_make_txn(
        advocate_deployment
):
    # Arrange
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']
    another_owner = accounts.add()

    min_referral = 100000000
    max_referral = 200000000
    reward_percent = 60
    is_active = True

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        configuration_contract.addAdvocateLevel(
            min_referral, max_referral, reward_percent, is_active,
            {"from": another_owner}
        )


def test_failure__add_advocate_level__reward_percent_is_0(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    min_referral = 100000000
    max_referral = 200000000
    reward_percent = 0
    is_active = True

    # Assert Before Actions
    assert configuration_contract.getLevelCount() == 4

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: reward percent "
                         "must be greater than zero"):
        configuration_contract.addAdvocateLevel(
            min_referral, max_referral, reward_percent, is_active,
            {"from": configuration_owner}
        )

    # Assert: Level Count
    assert configuration_contract.getLevelCount() == 4


def test_failure__add_advocate_level__min_equal_max(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    min_referral = 100000000
    max_referral = 100000000
    reward_percent = 25
    is_active = True

    # Assert Before Actions
    assert configuration_contract.getLevelCount() == 4

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: min referral must "
                         "be less than max referral"):
        configuration_contract.addAdvocateLevel(
            min_referral, max_referral, reward_percent, is_active,
            {"from": configuration_owner}
        )

    # Assert: Level Count
    assert configuration_contract.getLevelCount() == 4


def test_failure__add_advocate_level__min_over_max(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    min_referral = 100000000
    max_referral = 99999999
    reward_percent = 25
    is_active = True

    # Assert Before Actions
    assert configuration_contract.getLevelCount() == 4

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: min referral must "
                         "be less than max referral"):
        configuration_contract.addAdvocateLevel(
            min_referral, max_referral, reward_percent, is_active,
            {"from": configuration_owner}
        )

    # Assert: Level Count
    assert configuration_contract.getLevelCount() == 4


def test_failure__add_advocate_level__min_referral_not_continuous(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    min_referral = 30000
    max_referral = 40000
    reward_percent = 25
    is_active = True

    # Assert Before Actions
    assert configuration_contract.getLevelCount() == 4

    # Action
    with brownie.reverts("AdvocateRewardConfiguration: min referral must "
                         "be continuous number from max referral of latest level"):
        configuration_contract.addAdvocateLevel(
            min_referral, max_referral, reward_percent, is_active,
            {"from": configuration_owner}
        )

    # Assert: Level Count
    assert configuration_contract.getLevelCount() == 4
