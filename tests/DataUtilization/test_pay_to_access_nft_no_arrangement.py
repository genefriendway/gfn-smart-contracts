import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__pay_to_access__gpo_has_no_arrangement(
        deployment, initial_life_treasury_and_pool, const
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    life_token = deployment[const.LIFE_TOKEN]
    gnft_token = deployment[const.GNFT_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    du_wallet = deployment[const.DATA_UTILIZER_WALLET]
    data_utilization = deployment[const.DATA_UTILIZATION]

    data_utilizer1 = initial_life_treasury_and_pool['data_utilizer1']
    genetic_owner1 = accounts.add()
    gnft_token_id1 = 4356765432  # this token has no arrangement

    # Arranges: Mint G-NFT Token
    gnft_token.mintBatchGNFT(
        [genetic_owner1], [gnft_token_id1], True, {'from': gfn_owner1}
    )

    # Asserts before actions
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner1) == 0
    assert du_wallet.getBalanceOfParticipant(data_utilizer1) == 300e+18
    assert life_token.balanceOf(gpo_wallet.address) == 0
    assert life_token.balanceOf(du_wallet.address) == 300e+18

    # Actions:
    tx = data_utilization.payToAccess(
        du_wallet,
        data_utilizer1,
        [gnft_token_id1],
        [20e+18],
        {'from': gfn_owner1}
    )

    # Assert: PayToAccess Event
    assert ('PayToAccess' in tx.events) is True
    assert tx.events['PayToAccess']['fromParticipantWallet'] == du_wallet.address
    assert tx.events['PayToAccess']['fromSender'] == data_utilizer1.address
    assert tx.events['PayToAccess']['receivedTokenIds'] == [gnft_token_id1]
    assert tx.events['PayToAccess']['receivedLIFEAmounts'] == [20e+18]
    # Asserts after actions
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner1) == 20e+18
    assert du_wallet.getBalanceOfParticipant(data_utilizer1) == 280e+18
    assert life_token.balanceOf(gpo_wallet.address) == 20e+18
    assert life_token.balanceOf(du_wallet.address) == 280e+18
