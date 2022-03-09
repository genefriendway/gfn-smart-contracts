import brownie
import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass

@pytest.fixture(scope="module")
def pool_setup(deployment, initial_life_treasury_and_pool, const):
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    reserve_pool = deployment[const.RESERVE_POOL]
    reserve_pool_wallet = deployment[const.RESERVE_POOL_WALLET]
    investor_wallet = deployment[const.INVESTOR_WALLET]

    investor1 = initial_life_treasury_and_pool['investor1']
    investor2 = initial_life_treasury_and_pool['investor2']
    investor3 = initial_life_treasury_and_pool['investor3']
    investor4 = initial_life_treasury_and_pool['investor4']
    investor5 = initial_life_treasury_and_pool['investor5']
    pool_id = initial_life_treasury_and_pool['pool_id']

    # Arrange data for pool
    reserve_pool.joinPool(investor1, pool_id, 12e+18, {"from": gfn_operator})
    reserve_pool.joinPool(investor2, pool_id, 50e+18, {"from": gfn_operator})
    reserve_pool.joinPool(investor1, pool_id, 10e+18, {"from": gfn_operator})
    reserve_pool.joinPool(investor2, pool_id, 30e+18, {"from": gfn_operator})
    reserve_pool.joinPool(investor3, pool_id, 30e+18, {"from": gfn_operator})
    reserve_pool.joinPool(investor1, pool_id, 60e+18, {"from": gfn_operator})
    reserve_pool.joinPool(investor4, pool_id, 80e+18, {"from": gfn_operator})
    reserve_pool.joinPool(investor4, pool_id, 80e+18, {"from": gfn_operator})
    reserve_pool.joinPool(investor3, pool_id, 150e+18, {"from": gfn_operator})
    reserve_pool.joinPool(investor5, pool_id, 50e+18, {"from": gfn_operator})

    assert reserve_pool.getBalanceOfInvestor(investor1, pool_id) == 82e+18
    assert reserve_pool.getBalanceOfInvestor(investor2, pool_id) == 80e+18
    assert reserve_pool.getBalanceOfInvestor(investor3, pool_id) == 180e+18
    assert reserve_pool.getBalanceOfInvestor(investor4, pool_id) == 160e+18
    assert reserve_pool.getBalanceOfInvestor(investor5, pool_id) == 50e+18

    assert reserve_pool_wallet.getBalanceOfParticipant(investor1) == 82e+18
    assert reserve_pool_wallet.getBalanceOfParticipant(investor2) == 80e+18
    assert reserve_pool_wallet.getBalanceOfParticipant(investor3) == 180e+18
    assert reserve_pool_wallet.getBalanceOfParticipant(investor4) == 160e+18
    assert reserve_pool_wallet.getBalanceOfParticipant(investor5) == 50e+18

    assert investor_wallet.getBalanceOfParticipant(investor1) == 18e+18
    assert investor_wallet.getBalanceOfParticipant(investor2) == 170e+18
    assert investor_wallet.getBalanceOfParticipant(investor3) == 220e+18
    assert investor_wallet.getBalanceOfParticipant(investor4) == 440e+18
    assert investor_wallet.getBalanceOfParticipant(investor5) == 0

    assert life_token.balanceOf(reserve_pool_wallet.address) == 552e+18
    assert life_token.balanceOf(investor_wallet.address) == 848e+18
    assert reserve_pool.getBalanceOfPool(pool_id) == 552e+18


def test_success__join_pool__request_one_co_investor(
        deployment, initial_life_treasury_and_pool, pool_setup, const
):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    reserve_pool = deployment[const.RESERVE_POOL]
    reserve_pool_wallet = deployment[const.RESERVE_POOL_WALLET]
    investor_wallet = deployment[const.INVESTOR_WALLET]

    investor1 = initial_life_treasury_and_pool['investor1']
    pool_id = initial_life_treasury_and_pool['pool_id']
    genetic_owner1 = accounts[6]

    # Assert before actions
    assert life_token.balanceOf(gfn_wallet.address) == 5266e+18

    # Actions: request co-investors
    reserve_pool.requestCoInvestors(
        genetic_owner1, pool_id, 3e+18, {"from": gfn_operator}
    )

    # Asserts: ReversePool status
    assert reserve_pool.getBalanceOfPool(pool_id) == 549e+18
    assert reserve_pool.getBalanceOfInvestor(investor1, pool_id) == 79e+18

    # Asserts: ReversePoolWallet status
    assert reserve_pool_wallet.getBalanceOfParticipant(investor1.address) == 79e+18
    assert life_token.balanceOf(reserve_pool_wallet.address) == 549e+18

    # Asserts: GFN Wallet Status
    assert life_token.balanceOf(gfn_wallet.address) == 5269e+18


def test_success__join_pool__request_two_co_investor(deployment, initial_life_treasury_and_pool, const):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    reserve_pool = deployment[const.RESERVE_POOL]
    reserve_pool_wallet = deployment[const.RESERVE_POOL_WALLET]
    investor_wallet = deployment[const.INVESTOR_WALLET]

    investor1 = initial_life_treasury_and_pool['investor1']
    investor2 = initial_life_treasury_and_pool['investor2']
    pool_id = initial_life_treasury_and_pool['pool_id']
    genetic_owner1 = accounts[6]

    # Assert before actions
    assert life_token.balanceOf(gfn_wallet.address) == 5266e+18

    # Actions: request co-investors
    reserve_pool.requestCoInvestors(
        genetic_owner1, pool_id, 25e+18, {"from": gfn_operator}
    )

    # Asserts: ReversePool status
    assert reserve_pool.getBalanceOfPool(pool_id) == 527e+18
    assert reserve_pool.getBalanceOfInvestor(investor1, pool_id) == 70e+18
    assert reserve_pool.getBalanceOfInvestor(investor2, pool_id) == 67e+18

    # Asserts: ReversePoolWallet status
    assert reserve_pool_wallet.getBalanceOfParticipant(investor1.address) == 70e+18
    assert reserve_pool_wallet.getBalanceOfParticipant(investor2.address) == 67e+18
    assert life_token.balanceOf(reserve_pool_wallet.address) == 527e+18

    # Asserts: GFN Wallet Status
    assert life_token.balanceOf(gfn_wallet.address) == 5291e+18
