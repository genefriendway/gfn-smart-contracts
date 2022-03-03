import brownie
import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__make_arrangement(deployment, initial_life_treasury_and_pool, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    reserve_pool = deployment[const.RESERVE_POOL]
    reserve_pool_wallet = deployment[const.RESERVE_POOL_WALLET]
    revenue_sharing = deployment[const.REVENUE_SHARING_ARRANGEMENT]

    investor1 = initial_life_treasury_and_pool['investor1']
    pool_id = initial_life_treasury_and_pool['pool_id']
    genetic_owner = accounts.add()

    # Actions: request co-investors
    reserve_pool.requestCoInvestors(
        genetic_owner, pool_id, 3e+18, {'from': gfn_owner1}
    )

    # Asserts: ReversePool status
    assert reserve_pool.getBalanceOfPool(pool_id) == 9e+18
    assert reserve_pool.getBalanceOfInvestor(investor1, pool_id) == 9e+18

    # Asserts: ReversePoolWallet status
    assert reserve_pool_wallet.getBalanceOfParticipant(investor1.address) == 9e+18
    assert life_token.balanceOf(reserve_pool_wallet.address) == 9e+18

    # Asserts: GFN Wallet Status
    assert life_token.balanceOf(gfn_wallet.address) == 6019e+18

    # Asserts: RevenueSharingArrangement status
    assert revenue_sharing.hasArrangementByGPO(genetic_owner) is True
    assert revenue_sharing.queryCoInvestorsByGPO(genetic_owner) == (investor1,)
    assert revenue_sharing.queryTotalAccumulatedRevenueByGPO(genetic_owner) == 0
    assert revenue_sharing.queryTotalInvestedLIFEOfInvestorsByGPO(genetic_owner) == 3e+18
    assert revenue_sharing.queryInvestedLIFEOfInvestorByGPO(genetic_owner, investor1) == 3e+18
