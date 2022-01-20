import brownie
import pytest

from brownie import accounts


def test_success__submit_transaction__transfer_life_from_treasury(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    life_treasury = deployment[const.LIFE_TREASURY]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    genetic_owner1 = accounts[3]
    genetic_owner2 = accounts[4]

    # mint LIFE to Treasury
    gnft_token.mintGNFT(genetic_owner1, 'abcxyz', 12345678, {"from": gfn_owner1})
    # check balance of Treasury after mint GFNT token
    assert life_token.balanceOf(life_treasury.address) == 90000000e+18
    assert life_token.balanceOf(genetic_owner2) == 0

    # Actions
    # gfn_owner1 make a transaction to transfer 888 LIFE to genetic_owner2
    calldata = life_token.transfer.encode_input(genetic_owner2, 888e+18)
    tx = life_treasury.submitTransaction(
        life_token.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['SubmitTransaction']['transactionId']

    # gnf_owner2 confirm the transaction that gfn_owner1 made
    life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # Assert: check balances after transferring
    assert life_token.balanceOf(life_treasury.address) == 89999112e+18
    assert life_token.balanceOf(genetic_owner2) == 888e+18
