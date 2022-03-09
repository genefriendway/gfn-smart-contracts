import pytest


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


# eq = eq
# lt = less than
# gt = greater than

def test_success__accumulated_revenue_eq_0__new_revenue_inside_1st_range(
    deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 6
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 1

    assert results[0][0] == 0
    assert results[0][1] == 6
    assert results[0][2] == 100
    assert results[0][3] == 0


def test_success__accumulated_revenue_eq_0__new_revenue_eq_1st_range_upper(
        deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 12
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 1

    assert results[0][0] == 0
    assert results[0][1] == 12
    assert results[0][2] == 100
    assert results[0][3] == 0


def test_success__accumulated_revenue_eq_0__new_revenue_inside_2nd_range(
    deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 15
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 2

    assert results[0][0] == 3
    assert results[0][1] == 12
    assert results[0][2] == 100
    assert results[0][3] == 0

    assert results[1][0] == 0
    assert results[1][1] == 3
    assert results[1][2] == 80
    assert results[1][3] == 20


def test_success__accumulated_revenue_eq_0__new_revenue_eq_2nd_range_upper(
    deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 24
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 2

    assert results[0][0] == 12
    assert results[0][1] == 12
    assert results[0][2] == 100
    assert results[0][3] == 0

    assert results[1][0] == 0
    assert results[1][1] == 12
    assert results[1][2] == 80
    assert results[1][3] == 20


def test_success__accumulated_revenue_eq_0__new_revenue_inside_3rd_range(
    deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 29
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 3

    assert results[0][0] == 17
    assert results[0][1] == 12
    assert results[0][2] == 100
    assert results[0][3] == 0

    assert results[1][0] == 5
    assert results[1][1] == 12
    assert results[1][2] == 80
    assert results[1][3] == 20

    assert results[2][0] == 0
    assert results[2][1] == 5
    assert results[2][2] == 60
    assert results[2][3] == 40


def test_success__accumulated_revenue_eq_0__new_revenue_eq_3rd_range_upper(
    deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 36
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 3

    assert results[0][0] == 24
    assert results[0][1] == 12
    assert results[0][2] == 100
    assert results[0][3] == 0

    assert results[1][0] == 12
    assert results[1][1] == 12
    assert results[1][2] == 80
    assert results[1][3] == 20

    assert results[2][0] == 0
    assert results[2][1] == 12
    assert results[2][2] == 60
    assert results[2][3] == 40


def test_success__accumulated_revenue_eq_0__new_revenue_inside_4th_range(
    deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 37
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 4

    assert results[0][0] == 25
    assert results[0][1] == 12
    assert results[0][2] == 100
    assert results[0][3] == 0

    assert results[1][0] == 13
    assert results[1][1] == 12
    assert results[1][2] == 80
    assert results[1][3] == 20

    assert results[2][0] == 1
    assert results[2][1] == 12
    assert results[2][2] == 60
    assert results[2][3] == 40

    assert results[3][0] == 0
    assert results[3][1] == 1
    assert results[3][2] == 40
    assert results[3][3] == 60


def test_success__accumulated_revenue_eq_0__new_revenue_eq_4th_range_upper(
    deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 48
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 4

    assert results[0][0] == 36
    assert results[0][1] == 12
    assert results[0][2] == 100
    assert results[0][3] == 0

    assert results[1][0] == 24
    assert results[1][1] == 12
    assert results[1][2] == 80
    assert results[1][3] == 20

    assert results[2][0] == 12
    assert results[2][1] == 12
    assert results[2][2] == 60
    assert results[2][3] == 40

    assert results[3][0] == 0
    assert results[3][1] == 12
    assert results[3][2] == 40
    assert results[3][3] == 60


def test_success__accumulated_revenue_eq_0__new_revenue_inside_5th_range(
    deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 50
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 5

    assert results[0][0] == 38
    assert results[0][1] == 12
    assert results[0][2] == 100
    assert results[0][3] == 0

    assert results[1][0] == 26
    assert results[1][1] == 12
    assert results[1][2] == 80
    assert results[1][3] == 20

    assert results[2][0] == 14
    assert results[2][1] == 12
    assert results[2][2] == 60
    assert results[2][3] == 40

    assert results[3][0] == 2
    assert results[3][1] == 12
    assert results[3][2] == 40
    assert results[3][3] == 60

    assert results[4][0] == 0
    assert results[4][1] == 2
    assert results[4][2] == 20
    assert results[4][3] == 80


def test_success__accumulated_revenue_eq_0__new_revenue_eq_5th_range_upper(
    deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 60
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 5

    assert results[0][0] == 48
    assert results[0][1] == 12
    assert results[0][2] == 100
    assert results[0][3] == 0

    assert results[1][0] == 36
    assert results[1][1] == 12
    assert results[1][2] == 80
    assert results[1][3] == 20

    assert results[2][0] == 24
    assert results[2][1] == 12
    assert results[2][2] == 60
    assert results[2][3] == 40

    assert results[3][0] == 12
    assert results[3][1] == 12
    assert results[3][2] == 40
    assert results[3][3] == 60

    assert results[4][0] == 0
    assert results[4][1] == 12
    assert results[4][2] == 20
    assert results[4][3] == 80


def test_success__accumulated_revenue_eq_0__new_revenue_gt_5th_range_upper(
    deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 122
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 6

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


def test_success__accumulated_revenue_lt_1st_range_upper__new_revenue_inside_1st_range(
    deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 0
    new_revenue = 6
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 1

    assert results[0][0] == 0
    assert results[0][1] == 6
    assert results[0][2] == 100
    assert results[0][3] == 0


def test_success__accumulated_revenue_inside_1st_range__new_revenue_eq_1st_range_upper(
        deployment, const
):
    # Arranges
    config = deployment[const.CONFIGURATION]

    results = []
    total_invested_life = 12
    total_accumulated_revenue = 2
    new_revenue = 4
    remaining_revenue = new_revenue

    # Actions
    while remaining_revenue > 0:
        distributions = config.getRevenueDistributionRatios(
            total_invested_life, total_accumulated_revenue, remaining_revenue
        )
        remaining_revenue, distributed_revenue, _, _ = distributions
        total_accumulated_revenue += distributed_revenue
        results.append(distributions)

    # Asserts
    assert len(results) == 1

    assert results[0][0] == 0
    assert results[0][1] == 4
    assert results[0][2] == 100
    assert results[0][3] == 0
