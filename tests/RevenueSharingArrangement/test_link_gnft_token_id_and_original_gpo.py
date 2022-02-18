import brownie
import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__link_token_and_original_gpo(
    deployment, initial_life_treasury_and_pool, const
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    reserve_pool = deployment[const.RESERVE_POOL]
    gnft_token = deployment[const.GNFT_TOKEN]
    revenue_sharing = deployment[const.REVENUE_SHARING_ARRANGEMENT]

    investor1 = initial_life_treasury_and_pool['investor1']
    pool_id = initial_life_treasury_and_pool['pool_id']
    genetic_owner = accounts.add()
    gnft_token_id = 4356765432

    # Arrange: request co-investors
    reserve_pool.requestCoInvestors(
        genetic_owner, pool_id, 3e+18, {'from': gfn_owner1}
    )
    # Arrange: mint G-NFT token
    gnft_token.mintGNFT(genetic_owner, gnft_token_id, {"from": gfn_owner1})

    # Actions
    revenue_sharing.linkGNFTTokenIdAndOriginalGeneticProfileOwner(
        gnft_token_id, genetic_owner, {'from': gfn_owner1}
    )

    # Asserts: RevenueSharingArrangement status
    assert revenue_sharing.hasArrangementByGPO(genetic_owner) is True
    assert revenue_sharing.hasArrangementByTokenId(gnft_token_id) is True
    assert revenue_sharing.queryCoInvestorsByGPO(genetic_owner) == (investor1,)
    assert revenue_sharing.queryCoInvestorsByTokenId(gnft_token_id) == (investor1,)
    assert revenue_sharing.queryTotalAccumulatedRevenueByGPO(genetic_owner) == 0
    assert revenue_sharing.queryTotalAccumulatedRevenueByTokenId(gnft_token_id) == 0
    assert revenue_sharing.queryTotalInvestedLIFEOfInvestorsByGPO(genetic_owner) == 3e+18
    assert revenue_sharing.queryTotalInvestedLIFEOfInvestorsByTokenId(gnft_token_id) == 3e+18
    assert revenue_sharing.queryInvestedLIFEOfInvestorByGPO(genetic_owner, investor1) == 3e+18
    assert revenue_sharing.queryInvestedLIFEOfInvestorByTokenId(gnft_token_id, investor1) == 3e+18
