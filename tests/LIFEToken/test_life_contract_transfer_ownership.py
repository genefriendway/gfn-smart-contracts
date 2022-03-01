import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__transfer_ownership__right_owner_transfer(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    life_token = deployment[const.LIFE_TOKEN]

    new_owner = accounts.add()

    # assert before actions
    assert life_token.owner() == gfn_owner1

    # Actions
    tx = life_token.transferOwnership(new_owner.address, {"from": gfn_owner1})

    # Assert: RegisterContract Event
    assert ('OwnershipTransferred' in tx.events) is True
    assert tx.events['OwnershipTransferred']['previousOwner'] == gfn_owner1.address
    assert tx.events['OwnershipTransferred']['newOwner'] == new_owner.address

    # Asserts: after actions
    assert life_token.owner() == new_owner


def test_failure__transfer_ownership__not_owner_transfer(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    life_token = deployment[const.LIFE_TOKEN]

    new_owner = accounts.add()

    # assert before actions
    assert life_token.owner() == gfn_owner1

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        life_token.transferOwnership(new_owner.address, {"from": new_owner})

    # Asserts: after actions
    assert life_token.owner() == gfn_owner1


def test_failure__transfer_ownership__right_owner_transfer_to_invalid_new_owner(
        deployment, const
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    life_token = deployment[const.LIFE_TOKEN]

    new_owner = "0x0000000000000000000000000000000000000000"

    # assert before actions
    assert life_token.owner() == gfn_owner1

    # Actions
    with brownie.reverts("Ownable: new owner is the zero address"):
        life_token.transferOwnership(new_owner, {"from": gfn_owner1})

    # Asserts: after actions
    assert life_token.owner() == gfn_owner1
