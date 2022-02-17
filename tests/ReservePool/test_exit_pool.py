import brownie
import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__exit_pool(deployment, initial_life_treasury_and_pool, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    reserve_pool = deployment[const.RESERVE_POOL]
    reserve_pool_wallet = deployment[const.RESERVE_POOL_WALLET]
    investor_wallet = deployment[const.INVESTOR_WALLET]

    investor1 = initial_life_treasury_and_pool['investor1']
    pool_id = initial_life_treasury_and_pool['pool_id']

    # Assert before actions
    assert life_token.balanceOf(gfn_wallet.address) == 6316e+18

    # Arrange data for pool
    reserve_pool.joinPool(investor1, pool_id, 12e+18, {'from': gfn_owner1})

    # Actions: request co-investors
    reserve_pool.exitPool(
        investor1, pool_id, 12e+18, {'from': gfn_owner1}
    )

    # Asserts: ReversePool status
    assert reserve_pool.getBalanceOfPool(pool_id) == 0
    assert reserve_pool.getBalanceOfInvestor(investor1, pool_id) == 0

    # Asserts: ReversePoolWallet status
    assert reserve_pool_wallet.getBalanceOfParticipant(investor1.address) == 0
    assert life_token.balanceOf(reserve_pool_wallet.address) == 0

    # Asserts: Investor Wallet Status
    assert investor_wallet.getBalanceOfParticipant(investor1.address) == 100e+18
    assert life_token.balanceOf(investor_wallet.address) == 350e+18
