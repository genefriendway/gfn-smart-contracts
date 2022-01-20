import brownie

from brownie import (
    accounts,
    LIFETreasury
)


def test_success__add_owner(deployment, const):
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
    transaction_id = tx.events['SubmitTransaction']['transactionId']
    assert life_treasury.isConfirmedTransaction(transaction_id) is False

    # Action: gnf_owner2 confirm the request
    life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})
    assert life_treasury.isConfirmedTransaction(transaction_id) is True

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 3
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2
    assert owners[2] == gfn_owner3


def test_failed__add_owner__not_treasury_call(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    life_treasury = deployment[const.LIFE_TREASURY]
    gfn_owner3 = accounts[3]

    # Actions
    with brownie.reverts("LIFETreasury: caller must be LIFETreasury"):
        life_treasury.addOwner(gfn_owner3, {"from": gfn_owner1})

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2


def test_failed__add_owner__null_owner_address(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    life_treasury = deployment[const.LIFE_TREASURY]
    gfn_owner3 = '0x0000000000000000000000000000000000000000'

    # Actions
    calldata = life_treasury.addOwner.encode_input(gfn_owner3)
    tx = life_treasury.submitTransaction(
        life_treasury.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['SubmitTransaction']['transactionId']

    # Action: gnf_owner2 confirm the request
    with brownie.reverts("LIFETreasury: execute transaction failed"):
        life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2


def test_failed__add_owner__existed_owner_address(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    life_treasury = deployment[const.LIFE_TREASURY]

    # Actions
    # add gfn_owner2 to treasury again
    calldata = life_treasury.addOwner.encode_input(gfn_owner2)
    tx = life_treasury.submitTransaction(
        life_treasury.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['SubmitTransaction']['transactionId']
    assert life_treasury.isConfirmedTransaction(transaction_id) is False

    # Action: gnf_owner2 confirm the request
    with brownie.reverts("LIFETreasury: execute transaction failed"):
        life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2


def test_failed__add_owner__exceed_max_owner(deployment, const):
    # Arranges
    gfn_owner1 = accounts[0]
    gfn_owner2 = accounts[1]
    gfn_owner3 = accounts[2]
    gfn_owner4 = accounts[3]
    gfn_owner5 = accounts[4]
    gfn_owner6 = accounts[5]

    # deploy LIFE Treasury contract
    life_treasury = LIFETreasury.deploy(
        [gfn_owner1, gfn_owner2, gfn_owner3, gfn_owner4],
        2,
        {'from': gfn_owner1}
    )

    # assert: before adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 4
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2
    assert owners[2] == gfn_owner3
    assert owners[3] == gfn_owner4

    # Actions: gfn_owner1 make a transaction to add owner gfn_owner5
    calldata = life_treasury.addOwner.encode_input(gfn_owner5)
    tx = life_treasury.submitTransaction(
        life_treasury.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['SubmitTransaction']['transactionId']

    # Action: gnf_owner2 confirm the transaction that add gfn_owner5
    life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # assert: after add owner gfn_owner6
    owners = life_treasury.getOwners()
    assert len(owners) == 5

    # Actions: gfn_owner1 make a transaction to add owner gfn_owner6
    calldata = life_treasury.addOwner.encode_input(gfn_owner6)
    tx = life_treasury.submitTransaction(
        life_treasury.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['SubmitTransaction']['transactionId']

    # Action: gnf_owner2 confirm the transaction that add gfn_owner6
    with brownie.reverts("LIFETreasury: execute transaction failed"):
        life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # assert: after add owner gfn_owner6
    owners = life_treasury.getOwners()
    assert len(owners) == 5
