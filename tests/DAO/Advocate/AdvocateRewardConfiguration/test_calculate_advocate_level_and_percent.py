import pytest


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__calculate_advocate_level_and_percent__0_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 0
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 0
    assert percent == 0


def test_success__calculate_advocate_level_and_percent__1_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 1
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 1
    assert percent == 20


def test_success__calculate_advocate_level_and_percent__2_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 2
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 1
    assert percent == 20


def test_success__calculate_advocate_level_and_percent__10_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 10
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 1
    assert percent == 20


def test_success__calculate_advocate_level_and_percent__99_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 99
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 1
    assert percent == 20


def test_success__calculate_advocate_level_and_percent__100_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 100
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 2
    assert percent == 30


def test_success__calculate_advocate_level_and_percent__150_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 150
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 2
    assert percent == 30


def test_success__calculate_advocate_level_and_percent__199_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 199
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 2
    assert percent == 30


def test_success__calculate_advocate_level_and_percent__200_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 200
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 3
    assert percent == 40


def test_success__calculate_advocate_level_and_percent__250_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 250
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 3
    assert percent == 40


def test_success__calculate_advocate_level_and_percent__299_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 299
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 3
    assert percent == 40


def test_success__calculate_advocate_level_and_percent__300_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 300
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 4
    assert percent == 50


def test_success__calculate_advocate_level_and_percent__350_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 350
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 4
    assert percent == 50


def test_success__calculate_advocate_level_and_percent__1000_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 1000
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 4
    assert percent == 50


def test_success__calculate_advocate_level_and_percent__10000_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 10000
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 4
    assert percent == 50


def test_success__calculate_advocate_level_and_percent__99999999_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 99999999
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 4
    assert percent == 50


def test_success__calculate_advocate_level_and_percent__100000000_referral(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    number_of_referral = 100000000
    level = configuration_contract.calculateAdvocateLevelNumber(
        number_of_referral, {"from": configuration_owner}
    )
    percent = configuration_contract.calculateAdvocateRewardPercent(
        number_of_referral, {"from": configuration_owner}
    )
    assert level == 0
    assert percent == 0