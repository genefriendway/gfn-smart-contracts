import brownie
import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__get_distribution_revenue_ratios(deployment, const):
    # Arranges
    revenue_sharing = deployment[const.REVENUE_SHARING_ARRANGEMENT]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 122
    remaining_revenue = new_revenue

    while remaining_revenue > 0:
        distributions = revenue_sharing.getDistributionRevenueRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # [(110, 12, 100, 0), (98, 12, 80, 20), (86, 12, 60, 40), (74, 12, 40, 60),
    #  (62, 12, 20, 80), (0, 62, 20, 80)]
    print(results)
    assert results[0][0] == 110
    assert results[0][1] == 12
    assert results[0][2] == 100
    assert results[0][3] == 0

    assert results[1][0] == 98
    assert results[1][1] == 12
    assert results[1][2] == 80
    assert results[1][3] == 20

    assert results[2][0] == 86
    assert results[2][1] == 12
    assert results[2][2] == 60
    assert results[2][3] == 40

    assert results[3][0] == 74
    assert results[3][1] == 12
    assert results[3][2] == 40
    assert results[3][3] == 60

    assert results[4][0] == 62
    assert results[4][1] == 12
    assert results[4][2] == 20
    assert results[4][3] == 80

    assert results[5][0] == 0
    assert results[5][1] == 62
    assert results[5][2] == 20
    assert results[5][3] == 80
