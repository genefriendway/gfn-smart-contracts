import pytest

from brownie import (
    accounts,
    MultiSignature
)


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__submit_transaction__remove_owner_from_treasury(const):
    # Arranges
    gfn_owner1 = accounts[0]
    gfn_owner2 = accounts[1]
    gfn_owner3 = accounts[2]

    # deploy LIFE Treasury contract
    life_treasury = MultiSignature.deploy(
        [gfn_owner1, gfn_owner2, gfn_owner3], 2, {"from": gfn_owner1}
    )

    # assert: before adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 3
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2
    assert owners[2] == gfn_owner3

    # Actions: gfn_owner1 make a request to remove gfn_owner2
    calldata = life_treasury.removeOwner.encode_input(gfn_owner2)
    tx = life_treasury.submitTransaction(
        life_treasury.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['SubmitTransaction']['transactionId']
    assert life_treasury.isConfirmedTransaction(transaction_id) is False

    # Action: gnf_owner3 confirm the request
    life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner3})
    assert life_treasury.isConfirmedTransaction(transaction_id) is True

    # assert: after remove gfn_owner2
    owners = life_treasury.getOwners()
    assert len(owners) == 2
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner3
