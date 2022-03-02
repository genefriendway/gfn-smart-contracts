import pytest

from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


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
    gnft_token.mintBatchGNFT([genetic_owner1], [12345678], True, {"from": gfn_owner1})
    assert life_token.balanceOf(life_treasury.address) == 90000000e+18

    # assert before actions
    assert life_treasury.numberOfRequiredConfirmation() == 2

    # Actions
    # gfn_owner1 make a transaction to change number of confirmation
    calldata = life_treasury.changeNumberOfConfirmationRequired.encode_input(1)
    tx = life_treasury.submitTransaction(
        life_treasury.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['SubmitTransaction']['transactionId']
    assert life_treasury.numberOfRequiredConfirmation() == 2

    # gnf_owner2 confirm the transaction that gfn_owner1 made
    life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # Assert: check balances after transferring
    assert life_treasury.numberOfRequiredConfirmation() == 1

    # gfn_owner1 make a new transaction to transfer LIFE to genetic_owner2
    # Actions
    calldata = life_token.transfer.encode_input(genetic_owner2, 888e+18)
    tx = life_treasury.submitTransaction(
        life_token.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['SubmitTransaction']['transactionId']

    # Assert: after second action
    assert life_treasury.isConfirmedTransaction(transaction_id) is True
    assert life_treasury.getConfirmationCount(transaction_id) == 1
    assert life_token.balanceOf(life_treasury.address) == 89999112e+18
    assert life_token.balanceOf(genetic_owner2) == 888e+18
