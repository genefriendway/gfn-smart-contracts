import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__set_nft_holder(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    nft_holder = deployment[const.NFT_HOLDER]
    configuration = deployment[const.CONFIGURATION]

    new_nft_holder = accounts.add()

    # Asserts: after actions
    assert configuration.getNFTHolder() == nft_holder.address

    # Actions: set NFT Holder
    tx = configuration.setNFTHolder(
        new_nft_holder.address, {"from": gfn_owner1}
    )

    # Assert: RegisterContract Event
    assert ('SetNFTHolder' in tx.events) is True
    assert tx.events['SetNFTHolder']['holder'] == new_nft_holder.address

    # Asserts: after actions
    assert configuration.getNFTHolder() == new_nft_holder.address


def test_failure__set_nft_holder__not_gfn_owner_set(deployment, const):
    # Arranges
    nft_holder = deployment[const.NFT_HOLDER]
    configuration = deployment[const.CONFIGURATION]
    fake_gfn_owner = accounts.add()
    new_nft_holder = accounts.add()

    # Actions: set NFT Holder
    with brownie.reverts("Ownable: caller is not the owner"):
        configuration.setNFTHolder(
            new_nft_holder.address, {"from": fake_gfn_owner}
        )

    # Asserts: after actions
    assert configuration.getNFTHolder() == nft_holder.address


def test_failure__set_gfn_operator__invalid_gnf_operator(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    nft_holder = deployment[const.NFT_HOLDER]
    configuration = deployment[const.CONFIGURATION]

    new_nft_holder = '0x0000000000000000000000000000000000000000'

    # Actions:
    with brownie.reverts("Configuration: NFT holder's address must be not empty"):
        configuration.setNFTHolder(
            new_nft_holder, {"from": gfn_owner1}
        )

    # # Asserts: after actions
    assert configuration.getNFTHolder() == nft_holder.address
