import pytest
import brownie

from brownie import (
    accounts,
    MultiSignature
)


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


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
    assert life_treasury.getTransactionCount(True, True) == 0
    assert life_treasury.getTransactionCount(False, True) == 0
    assert life_treasury.getTransactionCount(True, False) == 0

    # Actions
    calldata = life_treasury.addOwner.encode_input(gfn_owner3)
    tx = life_treasury.submitTransaction(
        life_treasury.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['SubmitTransaction']['transactionId']
    assert transaction_id == 0
    assert life_treasury.isConfirmedTransaction(transaction_id) is False
    assert life_treasury.getConfirmationCount(transaction_id) == 1
    assert life_treasury.getConfirmations(transaction_id) == [gfn_owner1.address]
    assert life_treasury.getTransactionCount(True, False) == 1
    assert life_treasury.getTransactionCount(False, True) == 0
    assert life_treasury.getTransactionCount(True, True) == 1

    # Action: gnf_owner2 confirm the request
    life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})
    assert life_treasury.isConfirmedTransaction(transaction_id) is True
    assert life_treasury.getConfirmationCount(transaction_id) == 2
    assert life_treasury.getConfirmations(transaction_id) == [gfn_owner1.address, gfn_owner2.address]
    assert life_treasury.getTransactionCount(True, False) == 0
    assert life_treasury.getTransactionCount(False, True) == 1
    assert life_treasury.getTransactionCount(True, True) == 1

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 3
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2
    assert owners[2] == gfn_owner3


def test_failure__add_owner__not_treasury_call(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    life_treasury = deployment[const.LIFE_TREASURY]
    gfn_owner3 = accounts[3]

    # Actions
    with brownie.reverts("MultiSignature: caller must be MultiSignature"):
        life_treasury.addOwner(gfn_owner3, {"from": gfn_owner1})

    with brownie.reverts("MultiSignature: caller must be MultiSignature"):
        life_treasury.removeOwner(gfn_owner1, {"from": gfn_owner1})

    with brownie.reverts("MultiSignature: caller must be MultiSignature"):
        life_treasury.changeNumberOfConfirmationRequired(5, {"from": gfn_owner1})

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2


def test_failure__add_owner__not_owner_submit_transaction(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    life_treasury = deployment[const.LIFE_TREASURY]
    gfn_owner3 = accounts.add()
    fake_owner = accounts.add()

    # assert: before adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2

    # Actions
    calldata = life_treasury.addOwner.encode_input(gfn_owner3)
    with brownie.reverts("MultiSignature: owner must exist"):
        life_treasury.submitTransaction(
            life_treasury.address, 0, calldata, {"from": fake_owner}
        )

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2


def test_failure__add_owner__not_owner_confirm_transaction(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    life_treasury = deployment[const.LIFE_TREASURY]
    gfn_owner3 = accounts.add()
    fake_owner = accounts.add()

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
    assert transaction_id == 0

    # Action: fake owner confirm the request
    with brownie.reverts("MultiSignature: owner must exist"):
        life_treasury.confirmTransaction(transaction_id, {"from": fake_owner})

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2


def test_failure__add_owner__owner_confirm_wrong_transaction_id(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    life_treasury = deployment[const.LIFE_TREASURY]
    gfn_owner3 = accounts.add()
    fake_owner = accounts.add()

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
    assert transaction_id == 0

    # Action: owner2 confirm the request that wrong transaction id
    wrong_transaction_id = 10
    with brownie.reverts("MultiSignature: transaction id must exist"):
        life_treasury.confirmTransaction(wrong_transaction_id, {"from": gfn_owner2})

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2


def test_failure__add_owner__owner_double_confirm_transaction_id(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    life_treasury = deployment[const.LIFE_TREASURY]
    gfn_owner3 = accounts.add()

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
    assert transaction_id == 0

    # Action: owner1 confirm the request again
    with brownie.reverts("MultiSignature: transaction id must not be confirmed by owner"):
        life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner1})

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2


def test_failure__add_owner__owner_confirm_executed_transaction_again(
        deployment, const
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    life_treasury = deployment[const.LIFE_TREASURY]
    gfn_owner3 = accounts.add()

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
    assert transaction_id == 0

    # Action: owner2 confirm the request
    life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 3
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2
    assert owners[2] == gfn_owner3

    # Action: owner2 continue to confirm the executed request again
    with brownie.reverts("MultiSignature: transaction id must not be confirmed by owner"):
        life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})


def test_failure__add_owner__null_owner_address(deployment, const):
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
    with brownie.reverts("MultiSignature: execute transaction failed"):
        life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2


def test_failure__add_owner__existed_owner_address(deployment, const):
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
    with brownie.reverts("MultiSignature: execute transaction failed"):
        life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # assert: after adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2


def test_failure__add_owner__exceed_max_owner(deployment, const):
    # Arranges
    gfn_owner1 = accounts[0]
    gfn_owner2 = accounts[1]
    gfn_owner3 = accounts[2]
    gfn_owner4 = accounts[3]
    gfn_owner5 = accounts[4]
    gfn_owner6 = accounts[5]

    # deploy LIFE Treasury contract
    life_treasury = MultiSignature.deploy(
        [gfn_owner1, gfn_owner2, gfn_owner3, gfn_owner4],
        2,
        {"from": gfn_owner1}
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
    with brownie.reverts("MultiSignature: execute transaction failed"):
        life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # assert: after add owner gfn_owner6
    owners = life_treasury.getOwners()
    assert len(owners) == 5
