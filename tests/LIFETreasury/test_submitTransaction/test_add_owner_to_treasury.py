from brownie import accounts


def test_success__submit_transaction__add_owner_to_treasury(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    life_treasury = deployment[const.LIFE_TREASURY]
    gfn_owner3 = accounts[3]

    # assert: before adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2

    # Actions
    calldata = life_treasury.addOwner.encode_input(gfn_owner3)
    tx = life_treasury.submitTransaction(
        life_treasury.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['Submission']['transactionId']
    assert life_treasury.isConfirmed(transaction_id) is False

    # Action: gnf_owner2 confirm the request
    life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})
    assert life_treasury.isConfirmed(transaction_id) is True

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 3
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2
    assert owners[2] == gfn_owner3
