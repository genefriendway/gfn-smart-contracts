import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__transfer_ownership__right_owner_transfer(registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]

    new_owner = accounts.add()

    # assert before actions
    assert registry.owner() == gfn_owner1

    # Actions
    tx = registry.transferOwnership(new_owner.address, {"from": gfn_owner1})

    # Assert: RegisterContract Event
    assert ('OwnershipTransferred' in tx.events) is True
    assert tx.events['OwnershipTransferred']['previousOwner'] == gfn_owner1.address
    assert tx.events['OwnershipTransferred']['newOwner'] == new_owner.address

    # Asserts: after actions
    assert registry.owner() == new_owner


def test_failure__transfer_ownership__not_owner_transfer(registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]

    new_owner = accounts.add()

    # assert before actions
    assert registry.owner() == gfn_owner1

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        registry.transferOwnership(new_owner.address, {"from": new_owner})

    # Asserts: after actions
    assert registry.owner() == gfn_owner1


def test_failure__transfer_ownership__right_owner_transfer_to_invalid_new_owner(
        registry_deployment, const
):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]

    new_owner = "0x0000000000000000000000000000000000000000"

    # assert before actions
    assert registry.owner() == gfn_owner1

    # Actions
    with brownie.reverts("Ownable: new owner is the zero address"):
        registry.transferOwnership(new_owner, {"from": gfn_owner1})

    # Asserts: after actions
    assert registry.owner() == gfn_owner1
