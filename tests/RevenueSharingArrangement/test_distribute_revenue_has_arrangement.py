import brownie
import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.fixture(scope="module")
def arrangement_setup(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    investor_wallet = deployment[const.INVESTOR_WALLET]
    reserve_pool = deployment[const.RESERVE_POOL]
    du_wallet = deployment[const.DATA_UTILIZER_WALLET]
    revenue_sharing = deployment[const.REVENUE_SHARING_ARRANGEMENT]

    # ======== initialize LIFE token for LIFE Treasury =====
    gnft_token.mintBatchGNFT([accounts.add()], [876545678], True, {"from": gfn_owner1})

    # ======== initialize LIFE token for GFNWallet =========
    calldata = life_token.transfer.encode_input(gfn_wallet, 6000e+18)
    tx = life_treasury.submitTransaction(
        life_token.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['SubmitTransaction']['transactionId']

    # gnf_owner2 confirm the transaction that gfn_owner1 made
    life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # Assert: check balances after transferring to GFN Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6000e+18

    # ======= initialize LIFE token for investors
    investor1 = accounts.add()
    investor2 = accounts.add()
    investor3 = accounts.add()
    investor4 = accounts.add()
    investor5 = accounts.add()

    gfn_wallet.transferToParticipantWallet(
        investor_wallet, investor1, 100e+18, {"from": gfn_owner1}
    )
    gfn_wallet.transferToParticipantWallet(
        investor_wallet, investor2, 200e+18, {"from": gfn_owner1}
    )
    gfn_wallet.transferToParticipantWallet(
        investor_wallet, investor3, 300e+18, {"from": gfn_owner1}
    )
    gfn_wallet.transferToParticipantWallet(
        investor_wallet, investor4, 400e+18, {"from": gfn_owner1}
    )
    gfn_wallet.transferToParticipantWallet(
        investor_wallet, investor5, 500e+18, {"from": gfn_owner1}
    )
    assert life_token.balanceOf(gfn_wallet.address) == 4500e+18
    assert life_token.balanceOf(investor_wallet.address) == 1500e+18

    # ========== Initialize LIFE token for Data Utilizer =======
    data_utilizer1 = accounts.add()
    gfn_wallet.transferToParticipantWallet(
        du_wallet, data_utilizer1, 500e+18, {"from": gfn_owner1}
    )
    assert life_token.balanceOf(gfn_wallet.address) == 4000e+18
    assert life_token.balanceOf(du_wallet.address) == 500e+18

    # =========== create Reserve Pool ====
    pool_id1 = 'Pool_ID_1'
    pool_id2 = 'Pool_ID_2'
    reserve_pool.createPool(pool_id1, {"from": gfn_owner1})
    reserve_pool.createPool(pool_id2, {"from": gfn_owner1})

    # =========== Investor Join Pools ====
    reserve_pool.joinPool(investor1, pool_id1, 10e+18, {'from': gfn_owner1})
    reserve_pool.joinPool(investor2, pool_id1, 35e+18, {'from': gfn_owner1})
    reserve_pool.joinPool(investor3, pool_id1, 24e+18, {'from': gfn_owner1})
    reserve_pool.joinPool(investor4, pool_id1, 50e+18, {'from': gfn_owner1})
    reserve_pool.joinPool(investor5, pool_id2, 100e+18, {'from': gfn_owner1})

    assert reserve_pool.getBalanceOfPool(pool_id1) == 119e+18
    assert reserve_pool.getBalanceOfPool(pool_id2) == 100e+18

    # ========== GPO request Co-Investors ========
    genetic_owner1 = accounts.add()
    genetic_owner2 = accounts.add()
    genetic_owner3 = accounts.add()

    reserve_pool.requestCoInvestors(
        genetic_owner1, pool_id1, 3e+18, {"from": gfn_owner1}
    )
    reserve_pool.requestCoInvestors(
        genetic_owner2, pool_id1, 18e+18, {"from": gfn_owner1}
    )
    reserve_pool.requestCoInvestors(
        genetic_owner3, pool_id1, 55e+18, {"from": gfn_owner1}
    )

    co_investors1 = revenue_sharing.queryCoInvestorsByGPO(genetic_owner1)
    co_investors2 = revenue_sharing.queryCoInvestorsByGPO(genetic_owner2)
    co_investors3 = revenue_sharing.queryCoInvestorsByGPO(genetic_owner3)
    # (investor1,) = (3, )
    assert co_investors1 == (investor1.address,)
    # (investor1, investor2,) = (7, 11,)
    assert co_investors2 == (investor1.address, investor2.address,)
    # (investor2, investor3, investor4) = (24 , 24, 7)
    assert co_investors3 == (investor2.address, investor3.address, investor4.address,)

    assert revenue_sharing.hasArrangementByGPO(genetic_owner1) is True
    assert revenue_sharing.hasArrangementByGPO(genetic_owner2) is True
    assert revenue_sharing.hasArrangementByGPO(genetic_owner3) is True

    # ========== Mint G-NFT Token for GPO  ========
    gnft_token_id1 = 345645332424
    gnft_token_id2 = 885647569876
    gnft_token_id3 = 876546756764

    gnft_token.mintBatchGNFT(
        [genetic_owner1, genetic_owner2, genetic_owner3],
        [gnft_token_id1, gnft_token_id2, gnft_token_id3],
        True,
        {"from": gfn_owner1}
    )

    # ========== Link G-NFT Token and Arrangement ========
    revenue_sharing.linkGNFTTokenIdAndOriginalGeneticProfileOwner(
        gnft_token_id1, genetic_owner1, {"from": gfn_owner1}
    )
    revenue_sharing.linkGNFTTokenIdAndOriginalGeneticProfileOwner(
        gnft_token_id2, genetic_owner2, {"from": gfn_owner1}
    )
    revenue_sharing.linkGNFTTokenIdAndOriginalGeneticProfileOwner(
        gnft_token_id3, genetic_owner3, {"from": gfn_owner1}
    )
    assert revenue_sharing.hasArrangementByTokenId(gnft_token_id1) is True
    assert revenue_sharing.hasArrangementByTokenId(gnft_token_id2) is True
    assert revenue_sharing.hasArrangementByTokenId(gnft_token_id3) is True

    return {
        'data_utilizer1': data_utilizer1,
        'genetic_owner1': genetic_owner1,
        'genetic_owner2': genetic_owner2,
        'genetic_owner3': genetic_owner3,
        'gnft_token_id1': gnft_token_id1,
        'gnft_token_id2': gnft_token_id2,
        'gnft_token_id3': gnft_token_id3,
        'investor1': investor1,
        'investor2': investor2,
        'investor3': investor3,
        'investor4': investor4,
        'investor5': investor5,
        'pool_id1': pool_id1,
        'pool_id2': pool_id2,
    }


def test_success__distribute_revenue__one_co_investor(
        deployment, arrangement_setup, const
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    investor_wallet = deployment[const.INVESTOR_WALLET]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    du_wallet = deployment[const.DATA_UTILIZER_WALLET]
    revenue_sharing = deployment[const.REVENUE_SHARING_ARRANGEMENT]

    genetic_owner1 = arrangement_setup['genetic_owner1']
    gnft_token_id1 = arrangement_setup['gnft_token_id1']
    data_utilizer1 = arrangement_setup['data_utilizer1']
    investor1 = arrangement_setup['investor1']

    # Asserts before actions
    assert revenue_sharing.queryTotalAccumulatedRevenueByTokenId(gnft_token_id1) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner1) == 0
    assert investor_wallet.getBalanceOfParticipant(investor1) == 90e+18

    # Actions
    revenue_sharing.distributeRevenue(
        du_wallet,
        data_utilizer1,
        gnft_token_id1,
        10e+18,
        {'from': gfn_owner1}
    )
    # X = 3, Revenue = 10
    # 3 - 100:0  => 3 - 3:0
    # 6 - 80:20  => 3 - 2.4:0.6
    # 9 - 60:40  => 3 - 1.8:1.2
    # 12 - 40:60 => 1 - 0.4:0.6
    # 15 - 20:80 =>

    # Asserts: Arrangement status
    assert revenue_sharing.queryTotalAccumulatedRevenueByTokenId(gnft_token_id1) == 10e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner1) == 2.4e+18
    assert investor_wallet.getBalanceOfParticipant(investor1) == 90e+18 + 7.6e+18


def test_success__distribute_revenue__two_co_investors(
        deployment, arrangement_setup, const
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    investor_wallet = deployment[const.INVESTOR_WALLET]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    du_wallet = deployment[const.DATA_UTILIZER_WALLET]
    revenue_sharing = deployment[const.REVENUE_SHARING_ARRANGEMENT]

    genetic_owner2 = arrangement_setup['genetic_owner2']
    gnft_token_id2 = arrangement_setup['gnft_token_id2']
    data_utilizer1 = arrangement_setup['data_utilizer1']
    investor1 = arrangement_setup['investor1']
    investor2 = arrangement_setup['investor2']

    # Asserts before actions
    assert revenue_sharing.queryTotalAccumulatedRevenueByTokenId(gnft_token_id2) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 0
    assert investor_wallet.getBalanceOfParticipant(investor1) == 90e+18
    assert investor_wallet.getBalanceOfParticipant(investor2) == 165e+18

    # Actions
    tx = revenue_sharing.distributeRevenue(
        du_wallet,
        data_utilizer1,
        gnft_token_id2,
        12e+18,
        {'from': gfn_owner1}
    )
    # X = 18, Revenue = 12
    # 18 - 100:0 => 12 - 12:0
    # 36 - 80:20 -
    # 54 - 60:40 -
    # 72 - 40:60 -
    # 90 - 20:80 -

    # Asserts: Arrangement status
    assert revenue_sharing.queryTotalAccumulatedRevenueByTokenId(gnft_token_id2) == 12e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 0

    # Calculate total distributed revenue
    total_distributed_revenue = 0
    for event in tx.events['DistributeRevenueToInvestor']:
        total_distributed_revenue += event['revenue']

    assert total_distributed_revenue == 12e+18 - 0

    assert investor_wallet.getBalanceOfParticipant(investor1) == 90 * 10 ** 18 + 4666666666666666666


def test_success__distribute_revenue__three_co_investors(
        deployment, arrangement_setup, const
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    investor_wallet = deployment[const.INVESTOR_WALLET]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    du_wallet = deployment[const.DATA_UTILIZER_WALLET]
    revenue_sharing = deployment[const.REVENUE_SHARING_ARRANGEMENT]

    genetic_owner3 = arrangement_setup['genetic_owner3']
    gnft_token_id3 = arrangement_setup['gnft_token_id3']
    data_utilizer1 = arrangement_setup['data_utilizer1']
    investor2 = arrangement_setup['investor2']
    investor3 = arrangement_setup['investor3']
    investor4 = arrangement_setup['investor4']

    # Asserts before actions
    assert revenue_sharing.queryTotalAccumulatedRevenueByTokenId(gnft_token_id3) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner3) == 0
    assert investor_wallet.getBalanceOfParticipant(investor2) == 165e+18
    assert investor_wallet.getBalanceOfParticipant(investor3) == 276e+18
    assert investor_wallet.getBalanceOfParticipant(investor4) == 350e+18

    # Actions
    tx = revenue_sharing.distributeRevenue(
        du_wallet,
        data_utilizer1,
        gnft_token_id3,
        140e+18,
        {'from': gfn_owner1}
    )

    # Calculate total distributed revenue
    total_distributed_revenue = 0
    for event in tx.events['DistributeRevenueToInvestor']:
        total_distributed_revenue += event['revenue']

    # X = 55, Revenue = 140
    # 55 - 100:0 => 55 - 55:0
    # 110 - 80:20 - 55 - 44:11
    # 165 - 60:40 - 30 - 18:12
    # 230 - 40:60 -
    # 285 - 20:80 -

    # Asserts: Arrangement status
    assert revenue_sharing.queryTotalAccumulatedRevenueByTokenId(gnft_token_id3) == 140e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner3) == 11e+18 + 12e+18
    assert total_distributed_revenue == 140e+18 - (11e+18 + 12e+18)
    assert investor_wallet.getBalanceOfParticipant(investor2) == 216054545454545454545
    # assert investor_wallet.getBalanceOfParticipant(investor3) ==
    # assert investor_wallet.getBalanceOfParticipant(investor4) ==
