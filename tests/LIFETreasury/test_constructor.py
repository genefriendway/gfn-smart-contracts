import brownie
import pytest

from brownie import (
    accounts,
    MultiSignature
)


def test_success__initialize_contract(const):
    # Arranges
    gfn_owner1 = accounts[0]
    gfn_owner2 = accounts[1]
    gfn_owner3 = accounts[2]

    # deploy LIFE Treasury contract
    life_treasury = MultiSignature.deploy(
        [gfn_owner1, gfn_owner2, gfn_owner3], 3, {"from": gfn_owner1}
    )

    # assert: before adding one more owner
    owners = life_treasury.getOwners()
    assert len(owners) == 3
    assert owners[0] == gfn_owner1
    assert owners[1] == gfn_owner2
    assert owners[2] == gfn_owner3
    with pytest.raises(IndexError):
        assert owners[3]

    assert life_treasury.numberOfRequiredConfirmation() == 3
    assert life_treasury.transactionCount() == 0

    assert life_treasury.getTransactionCount(False, False) == 0
    assert life_treasury.getTransactionCount(True, False) == 0
    assert life_treasury.getTransactionCount(False, True) == 0
    assert life_treasury.getTransactionCount(True, True) == 0
