import brownie
import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__join_pool__one_investor_join(deployment, initial_life_treasury_and_pool, const):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    reserve_pool = deployment[const.RESERVE_POOL]
    reserve_pool_wallet = deployment[const.RESERVE_POOL_WALLET]
    investor_wallet = deployment[const.INVESTOR_WALLET]

    investor1 = initial_life_treasury_and_pool['investor1']
    pool_id = initial_life_treasury_and_pool['pool_id']

    # Actions
    reserve_pool.joinPool(investor1, pool_id, 12e+18, {"from": gfn_operator})

    # Asserts: ReversePool status
    assert reserve_pool.getBalanceOfPool(pool_id) == 12e+18
    assert reserve_pool.getBalanceOfInvestor(investor1, pool_id) == 12e+18

    # Asserts: InvestorWallet status
    assert investor_wallet.getBalanceOfParticipant(investor1.address) == 88e+18
    assert life_token.balanceOf(investor_wallet.address) == 1388e+18

    # Asserts: ReversePoolWallet status
    assert reserve_pool_wallet.getBalanceOfParticipant(investor1.address) == 12e+18
    assert life_token.balanceOf(reserve_pool_wallet.address) == 12e+18


def test_success__join_pool__two_investors_join(deployment, initial_life_treasury_and_pool, const):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    reserve_pool = deployment[const.RESERVE_POOL]
    reserve_pool_wallet = deployment[const.RESERVE_POOL_WALLET]
    investor_wallet = deployment[const.INVESTOR_WALLET]

    investor1 = initial_life_treasury_and_pool['investor1']
    investor2 = initial_life_treasury_and_pool['investor2']
    pool_id = initial_life_treasury_and_pool['pool_id']

    # Actions
    reserve_pool.joinPool(investor1, pool_id, 12e+18, {"from": gfn_operator})
    reserve_pool.joinPool(investor2, pool_id, 50e+18, {"from": gfn_operator})

    # Asserts: ReversePool status
    assert reserve_pool.getBalanceOfPool(pool_id) == 62e+18
    assert reserve_pool.getBalanceOfInvestor(investor1, pool_id) == 12e+18
    assert reserve_pool.getBalanceOfInvestor(investor2, pool_id) == 50e+18

    # Asserts: InvestorWallet status
    assert investor_wallet.getBalanceOfParticipant(investor1.address) == 88e+18
    assert investor_wallet.getBalanceOfParticipant(investor2.address) == 200e+18
    assert life_token.balanceOf(investor_wallet.address) == 1338e+18

    # Asserts: ReversePoolWallet status
    assert reserve_pool_wallet.getBalanceOfParticipant(investor1.address) == 12e+18
    assert reserve_pool_wallet.getBalanceOfParticipant(investor2.address) == 50e+18
    assert life_token.balanceOf(reserve_pool_wallet.address) == 62e+18
