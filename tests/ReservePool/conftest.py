import pytest

from brownie import accounts


@pytest.fixture(scope="module")
def initial_life_treasury_and_pool(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    gfn_operator = deployment[const.GFN_OPERATOR]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    investor_wallet = deployment[const.INVESTOR_WALLET]
    reserve_pool = deployment[const.RESERVE_POOL]

    genetic_owner1 = accounts[3]
    investor1 = accounts.add()
    investor2 = accounts.add()
    investor3 = accounts.add()
    investor4 = accounts.add()
    investor5 = accounts.add()

    # mint LIFE to Treasury
    gnft_token.mintBatchGNFT([genetic_owner1], [12345678], True, {"from": gfn_operator})

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
    assert life_token.balanceOf(life_treasury.address) == 89993334e+18
    assert life_token.balanceOf(gfn_wallet.address) == 6666e+18
    assert life_token.balanceOf(investor_wallet.address) == 0

    # Actions: Transfer LIFE token to Investor1
    gfn_wallet.transferToParticipantWallet(
        investor_wallet, investor1, 100e+18, {"from": gfn_operator}
    )

    assert life_token.balanceOf(life_treasury.address) == 89993334e+18
    assert life_token.balanceOf(gfn_wallet.address) == 6566e+18
    assert life_token.balanceOf(investor_wallet.address) == 100e+18
    assert investor_wallet.getBalanceOfParticipant(investor1.address) == 100e+18

    # Actions: Transfer LIFE token to Investor2
    gfn_wallet.transferToParticipantWallet(
        investor_wallet, investor2, 250e+18, {"from": gfn_operator}
    )

    assert life_token.balanceOf(life_treasury.address) == 89993334e+18
    assert life_token.balanceOf(gfn_wallet.address) == 6316e+18
    assert life_token.balanceOf(investor_wallet.address) == 350e+18
    assert investor_wallet.getBalanceOfParticipant(investor2.address) == 250e+18

    # Actions: Transfer LIFE token to Investor3
    gfn_wallet.transferToParticipantWallet(
        investor_wallet, investor3, 400e+18, {"from": gfn_operator}
    )

    assert life_token.balanceOf(life_treasury.address) == 89993334e+18
    assert life_token.balanceOf(gfn_wallet.address) == 5916e+18
    assert life_token.balanceOf(investor_wallet.address) == 750e+18
    assert investor_wallet.getBalanceOfParticipant(investor3.address) == 400e+18

    # Actions: Transfer LIFE token to Investor4
    gfn_wallet.transferToParticipantWallet(
        investor_wallet, investor4, 600e+18, {"from": gfn_operator}
    )

    assert life_token.balanceOf(life_treasury.address) == 89993334e+18
    assert life_token.balanceOf(gfn_wallet.address) == 5316e+18
    assert life_token.balanceOf(investor_wallet.address) == 1350e+18
    assert investor_wallet.getBalanceOfParticipant(investor4.address) == 600e+18

    # Actions: Transfer LIFE token to Investor5
    gfn_wallet.transferToParticipantWallet(
        investor_wallet, investor5, 50e+18, {"from": gfn_operator}
    )

    assert life_token.balanceOf(life_treasury.address) == 89993334e+18
    assert life_token.balanceOf(gfn_wallet.address) == 5266e+18
    assert life_token.balanceOf(investor_wallet.address) == 1400e+18
    assert investor_wallet.getBalanceOfParticipant(investor5.address) == 50e+18

    # create a pool
    pool_id = 'Pool_ID_1'
    reserve_pool.createPool(pool_id, {"from": gfn_operator})

    return {
        'investor1': investor1,
        'investor2': investor2,
        'investor3': investor3,
        'investor4': investor4,
        'investor5': investor5,
        'pool_id': pool_id
    }
