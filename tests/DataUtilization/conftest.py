import pytest

from brownie import accounts


@pytest.fixture(scope="module")
def initial_life_treasury_and_pool(deployment, const):
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

    genetic_owner1 = accounts.add()
    genetic_owner2 = accounts.add()
    investor1 = accounts.add()
    investor2 = accounts.add()
    investor3 = accounts.add()
    data_utilizer1 = accounts.add()
    gnft_token_id1 = 345645332424
    gnft_token_id2 = 885647569876

    # mint LIFE to Treasury
    gnft_token.mintBatchGNFT(
        [genetic_owner1, genetic_owner2],
        [gnft_token_id1, gnft_token_id2],
        True,
        {"from": gfn_owner1}
    )

    # Actions
    # gfn_owner1 make a transaction to transfer 6666 LIFE to gfn_wallet
    calldata = life_token.transfer.encode_input(gfn_wallet, 6666e+18)
    tx = life_treasury.submitTransaction(
        life_token.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['SubmitTransaction']['transactionId']

    # gnf_owner2 confirm the transaction that gfn_owner1 made
    life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # Assert: check balances after transferring to GFN Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6666e+18
    assert life_token.balanceOf(investor_wallet.address) == 0

    # Actions: Transfer LIFE token to Investor1
    gfn_wallet.transferToParticipantWallet(
        investor_wallet, investor1, 100e+18, {"from": gfn_owner1}
    )

    assert life_token.balanceOf(gfn_wallet.address) == 6566e+18
    assert life_token.balanceOf(investor_wallet.address) == 100e+18
    assert investor_wallet.getBalanceOfParticipant(investor1.address) == 100e+18

    # Actions: Transfer LIFE token to Investor2
    gfn_wallet.transferToParticipantWallet(
        investor_wallet, investor2, 250e+18, {"from": gfn_owner1}
    )

    # Actions: Transfer LIFE token to DataUtilizer1
    gfn_wallet.transferToParticipantWallet(
        du_wallet, data_utilizer1, 300e+18, {"from": gfn_owner1}
    )

    assert life_token.balanceOf(gfn_wallet.address) == 6016e+18
    assert life_token.balanceOf(investor_wallet.address) == 350e+18
    assert life_token.balanceOf(du_wallet.address) == 300e+18
    assert investor_wallet.getBalanceOfParticipant(investor2.address) == 250e+18
    assert du_wallet.getBalanceOfParticipant(data_utilizer1.address) == 300e+18

    # create a pool
    pool_id = 'Pool_ID_1'
    reserve_pool.createPool(pool_id, {"from": gfn_owner1})
    # investor 1 join the pool
    reserve_pool.joinPool(investor1, pool_id, 12e+18, {'from': gfn_owner1})

    return {
        'genetic_owner1': genetic_owner1,
        'genetic_owner2': genetic_owner2,
        'gnft_token_id1': gnft_token_id1,
        'gnft_token_id2': gnft_token_id2,
        'investor1': investor1,
        'investor2': investor2,
        'investor3': investor3,
        'data_utilizer1': data_utilizer1,
        'pool_id': pool_id
    }
