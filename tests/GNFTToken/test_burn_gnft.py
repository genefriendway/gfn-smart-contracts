import brownie
import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.fixture(scope="function")
def setup(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_profile_id = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintBatchGNFT(
        [genetic_owner1], [genetic_profile_id], True, {"from": gfn_owner1}
    )

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 90000000e+18


def test_success__burn_gnft__gfn_owner_burn_existed_nft(setup, deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_profile_id = 12345678
    genetic_owner1 = accounts[2]

    # Assert before burning token
    # # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.totalSupply() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(12345678) == genetic_owner1

    # Actions
    tx = gnft_token.burnGNFT(genetic_profile_id, {"from": gfn_owner1})

    # Assert: BurnGNFT Event
    assert ('BurnGNFT' in tx.events) is True
    assert tx.events['BurnGNFT']['geneticProfileId'] == genetic_profile_id
    assert tx.events['BurnGNFT']['burnedBy'] == gfn_owner1.address

    # Assert: Approval Event
    assert ('Approval' in tx.events) is True
    assert tx.events['Approval']['owner'] == genetic_owner1
    assert tx.events['Approval']['approved'] == "0x0000000000000000000000000000000000000000"
    assert tx.events['Approval']['tokenId'] == genetic_profile_id

    # Assert: Approval Event
    assert ('Transfer' in tx.events) is True
    assert tx.events['Transfer']['from'] == genetic_owner1
    assert tx.events['Transfer']['to'] == "0x0000000000000000000000000000000000000000"
    assert tx.events['Transfer']['tokenId'] == genetic_profile_id

    # # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.totalSupply() == 0
    assert gnft_token.balanceOf(genetic_owner1) == 0
    with brownie.reverts("ERC721: owner query for nonexistent token"):
        assert gnft_token.ownerOf(12345678)

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 90000000e+18


def test_success__burn_gnft__nft_owner_burn_existed_nft(setup, deployment, const):
    # Arranges
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_profile_id = 12345678
    genetic_owner1 = accounts[2]

    # Assert before burning token
    # # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.totalSupply() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(12345678) == genetic_owner1

    # Actions
    tx = gnft_token.burnGNFT(genetic_profile_id, {"from": genetic_owner1})

    # Assert: BurnGNFT Event
    assert ('BurnGNFT' in tx.events) is True
    assert tx.events['BurnGNFT']['geneticProfileId'] == genetic_profile_id
    assert tx.events['BurnGNFT']['burnedBy'] == genetic_owner1.address

    # Assert: Approval Event
    assert ('Approval' in tx.events) is True
    assert tx.events['Approval']['owner'] == genetic_owner1
    assert tx.events['Approval']['approved'] == "0x0000000000000000000000000000000000000000"
    assert tx.events['Approval']['tokenId'] == genetic_profile_id

    # Assert: Approval Event
    assert ('Transfer' in tx.events) is True
    assert tx.events['Transfer']['from'] == genetic_owner1
    assert tx.events['Transfer']['to'] == "0x0000000000000000000000000000000000000000"
    assert tx.events['Transfer']['tokenId'] == genetic_profile_id

    # # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.totalSupply() == 0
    assert gnft_token.balanceOf(genetic_owner1) == 0
    with brownie.reverts("ERC721: owner query for nonexistent token"):
        assert gnft_token.ownerOf(12345678)

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 90000000e+18


def test_success__burn_gnft__burn_and_mint_again(setup, deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_profile_id = 12345678
    genetic_owner1 = accounts[2]

    # Assert before burning token
    # # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.totalSupply() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(12345678) == genetic_owner1

    # Actions
    gnft_token.burnGNFT(genetic_profile_id, {"from": gfn_owner1})

    # # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.totalSupply() == 0
    assert gnft_token.balanceOf(genetic_owner1) == 0
    with brownie.reverts("ERC721: owner query for nonexistent token"):
        assert gnft_token.ownerOf(12345678)

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 90000000e+18

    # Mint again the same token id
    # Arranges
    genetic_profile_id = 12345678
    genetic_owner1 = accounts[2]

    # Actions: remint GNFT
    gnft_token.mintBatchGNFT(
        [genetic_owner1], [genetic_profile_id], True, {"from": gfn_owner1}
    )

    # Asserts: LIFEToken Status
    # the number of LIFE not changed
    assert life_token.balanceOf(life_treasury) == 90000000e+18


def test_failure__burn_gnft__not_gfn_owner_and_not_approvee(setup, deployment, const):
    # Arranges
    gnft_token = deployment[const.GNFT_TOKEN]
    genetic_owner2 = accounts.add()

    # Actions
    # genetic_owner1 make a transaction to burn their token id
    with brownie.reverts("GNFTToken: caller is not NFT owner nor approved"):
        gnft_token.burnGNFT(12345678, {"from": genetic_owner2})


def test_failure__burn_gnft__not_existed_genetic_profile_id(setup, deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    other_genetic_profile_id = 88888888
    genetic_owner1 = accounts[2]

    # Assert before burning token
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.totalSupply() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(12345678) == genetic_owner1

    # Actions
    with brownie.reverts("ERC721: operator query for nonexistent token"):
        gnft_token.burnGNFT(other_genetic_profile_id, {"from": gfn_owner1})

    # Assert after burning token
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.totalSupply() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(12345678) == genetic_owner1