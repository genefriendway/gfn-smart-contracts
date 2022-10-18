import pytest


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__calculate_reserve_revenue__revenue_0_dot_1(advocate_deployment):
    # Arrange
    config = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    revenue = 1 * 10 ** 17
    assert config.calculateReservedRevenueForCustomerReward(revenue) == 0.2 * 10 ** 17
    assert config.calculateReserveRevenueForPlatformFee(revenue) == 0.15 * 10 ** 17
    assert config.calculateReserveRevenueForCommunityCampaign(revenue) == 0.1 * 10 ** 17
    assert config.calculateReserveRevenueForQuarterReferralReward(revenue) == 0.05 * 10 ** 17
    assert config.calculateReserveRevenueForAdvocateReward(revenue) == 0.5 * 10 ** 17


def test_success__calculate_reserve_revenue__revenue_1(advocate_deployment):
    # Arrange
    config = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    revenue = 1 * 10 ** 18
    assert config.calculateReservedRevenueForCustomerReward(revenue) == 0.2 * 10 ** 18
    assert config.calculateReserveRevenueForPlatformFee(revenue) == 0.15 * 10 ** 18
    assert config.calculateReserveRevenueForCommunityCampaign(revenue) == 0.1 * 10 ** 18
    assert config.calculateReserveRevenueForQuarterReferralReward(revenue) == 0.05 * 10 ** 18
    assert config.calculateReserveRevenueForAdvocateReward(revenue) == 0.5 * 10 ** 18


def test_success__calculate_reserve_revenue__revenue_10(advocate_deployment):
    # Arrange
    config = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    revenue = 10 * 10 ** 18
    assert config.calculateReservedRevenueForCustomerReward(revenue) == 2 * 10 ** 18
    assert config.calculateReserveRevenueForPlatformFee(revenue) == 1.5 * 10 ** 18
    assert config.calculateReserveRevenueForCommunityCampaign(revenue) == 1 * 10 ** 18
    assert config.calculateReserveRevenueForQuarterReferralReward(revenue) == 0.5 * 10 ** 18
    assert config.calculateReserveRevenueForAdvocateReward(revenue) == 5 * 10 ** 18


def test_success__calculate_reserve_revenue__revenue_100(advocate_deployment):
    # Arrange
    config = advocate_deployment['advocate_reward_configuration_contract']

    # Action
    revenue = 100 * 10 ** 18
    assert config.calculateReservedRevenueForCustomerReward(revenue) == 20 * 10 ** 18
    assert config.calculateReserveRevenueForPlatformFee(revenue) == 15 * 10 ** 18
    assert config.calculateReserveRevenueForCommunityCampaign(revenue) == 10 * 10 ** 18
    assert config.calculateReserveRevenueForQuarterReferralReward(revenue) == 5 * 10 ** 18
    assert config.calculateReserveRevenueForAdvocateReward(revenue) == 50 * 10 ** 18
