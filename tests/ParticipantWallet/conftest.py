import pytest

from brownie import accounts


@pytest.fixture(scope="module")
def initial_life_treasury(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]

    genetic_owner1 = accounts[3]
    genetic_owner2 = accounts[4]

    # mint LIFE to Treasury
    gnft_token.mintGNFT(genetic_owner1, 12345678, {"from": gfn_owner1})

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
    assert life_token.balanceOf(gpo_wallet.address) == 0

    # Actions: Transfer LIFE token to GeneProfileOwnerWallet
    gfn_wallet.transferToParticipantWallet(
        gpo_wallet, genetic_owner2, 24e+18, {"from": gfn_owner1}
    )

    # Assert: check balances after transferring to genetic_owner2 in GeneProfileOwnerWallet
    assert life_token.balanceOf(life_treasury.address) == 89993334e+18
    assert life_token.balanceOf(gfn_wallet.address) == 6642e+18
    assert life_token.balanceOf(gpo_wallet.address) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2.address) == 24e+18
