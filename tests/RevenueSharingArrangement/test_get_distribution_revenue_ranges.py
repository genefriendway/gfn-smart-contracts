import brownie
import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__get_distribution_revenue_ranges(deployment, const):
    # Arranges
    revenue_sharing = deployment[const.REVENUE_SHARING_ARRANGEMENT]

    # Actions:
    revenue_ranges = revenue_sharing.getDistributionRevenueRanges(2)

    # Asserts
    # ((2, 100, 0), (4, 80, 20), (6, 60, 40), (8, 40, 60), (10, 20, 80))
    assert revenue_ranges[0][0] == 2
    assert revenue_ranges[0][1] == 100
    assert revenue_ranges[0][2] == 0

    assert revenue_ranges[1][0] == 4
    assert revenue_ranges[1][1] == 80
    assert revenue_ranges[1][2] == 20

    assert revenue_ranges[2][0] == 6
    assert revenue_ranges[2][1] == 60
    assert revenue_ranges[2][2] == 40

    assert revenue_ranges[3][0] == 8
    assert revenue_ranges[3][1] == 40
    assert revenue_ranges[3][2] == 60

    assert revenue_ranges[4][0] == 10
    assert revenue_ranges[4][1] == 20
    assert revenue_ranges[4][2] == 80
