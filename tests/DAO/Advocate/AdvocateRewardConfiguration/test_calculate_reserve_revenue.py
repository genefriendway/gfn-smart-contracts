import pytest


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__calculate_reserve_revenue__level_1__revenue_amount_10(advocate_deployment):
    # Arrange
    config = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    revenue = 10 * 10 ** 18
    referral = 1
    assert config.calculateRewardAmountForAdvocate(revenue, referral) == 2 * 10 ** 18


def test_success__calculate_reserve_revenue__level_2__revenue_amount_10(advocate_deployment):
    # Arrange
    config = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    revenue = 10 * 10 ** 18
    referral = 100
    assert config.calculateRewardAmountForAdvocate(revenue, referral) == 3 * 10 ** 18


def test_success__calculate_reserve_revenue__level_3__revenue_amount_10(advocate_deployment):
    # Arrange
    config = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    revenue = 10 * 10 ** 18
    referral = 200
    assert config.calculateRewardAmountForAdvocate(revenue, referral) == 4 * 10 ** 18


def test_success__calculate_reserve_revenue__level_4__revenue_amount_10(advocate_deployment):
    # Arrange
    config = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    revenue = 10 * 10 ** 18
    referral = 300
    assert config.calculateRewardAmountForAdvocate(revenue, referral) == 5 * 10 ** 18


def test_success__calculate_reserve_revenue__level_4_over__revenue_amount_10(advocate_deployment):
    # Arrange
    config = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    revenue = 10 * 10 ** 18
    referral = 888
    assert config.calculateRewardAmountForAdvocate(revenue, referral) == 5 * 10 ** 18