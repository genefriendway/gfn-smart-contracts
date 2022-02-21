import pytest

from brownie import (
    accounts,
    ContractRegistry,
    GNFTToken,
    LIFEToken,
    LIFETreasury,
)


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__mint_batch_gnft__mint_01_new_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_profile_id1 = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    tx = gnft_token.mintBatchGNFT(
        [genetic_owner1], [genetic_profile_id1], {"from": gfn_owner1}
    )

    # Assert: MintBatchGNFT Event
    assert ('MintBatchGNFT' in tx.events) is True
    # Assert: MintGNFT Event
    assert ('MintGNFT' in tx.events) is True
    assert tx.events['MintGNFT']['geneticProfileOwner'] == genetic_owner1
    assert tx.events['MintGNFT']['geneticProfileId'] == 12345678

    # Assert: MintLIFE Event
    assert ('MintLIFE' in tx.events) is True
    assert tx.events['MintLIFE']['to'] == life_treasury
    assert tx.events['MintLIFE']['geneticProfileId'] == 12345678

    # Assert: Events of Transaction
    assert ('Transfer' in tx.events) is True
    assert len(tx.events['Transfer']) == 2  # Transfer of ERC20 and ERC721

    # Asserts: GNFTToken status
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.getTotalCurrentTokens() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(genetic_profile_id1) == genetic_owner1

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 90000000e+18


def test_success__mint_batch_gnft__mint_02_new_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_profile_id1 = 12345678
    genetic_profile_id2 = 3454567
    genetic_owner1 = accounts[2]
    genetic_owner2 = accounts[3]

    # Actions
    gnft_token.mintBatchGNFT(
        [genetic_owner1, genetic_owner2],
        [genetic_profile_id1, genetic_profile_id2],
        {"from": gfn_owner1}
    )

    # Asserts: GNFTToken status
    assert gnft_token.getTotalMintedGeneticProfiles() == 2
    assert gnft_token.getTotalCurrentTokens() == 2
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.balanceOf(genetic_owner2) == 1
    assert gnft_token.ownerOf(genetic_profile_id1) == genetic_owner1
    assert gnft_token.ownerOf(genetic_profile_id2) == genetic_owner2

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 100000000e+18


def test_success__mint_batch_gnft__mint_08_new_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_profile_ids = []
    genetic_profile_owners = []

    # i = 2,3,4,5,6,7,8,9
    for i in range(2, 10):
        genetic_profile_ids.append(12345678 + i)
        genetic_profile_owners.append(accounts[i])

    # Actions
    gnft_token.mintBatchGNFT(
        genetic_profile_owners,
        genetic_profile_ids,
        {"from": gfn_owner1}
    )

    # Asserts: GNFTToken status
    assert gnft_token.getTotalMintedGeneticProfiles() == 8
    assert gnft_token.getTotalCurrentTokens() == 8

    for i in range(2, 10):
        assert gnft_token.balanceOf(accounts[i]) == 1
        assert gnft_token.ownerOf(12345678 + i) == accounts[i]

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 160000000e+18


def test_success__mint_batch_gnft__mint_24_new_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_profile_ids = []
    genetic_profile_owners = []

    # i = 0 -> 23
    for i in range(0, 24):
        genetic_profile_ids.append(123 + i)
        genetic_profile_owners.append(accounts.add())

    # Actions
    gnft_token.mintBatchGNFT(
        genetic_profile_owners,
        genetic_profile_ids,
        {"from": gfn_owner1}
    )

    # Asserts: GNFTToken status
    assert gnft_token.getTotalMintedGeneticProfiles() == 24
    assert gnft_token.getTotalCurrentTokens() == 24

    for i in range(0, 24):
        assert gnft_token.balanceOf(genetic_profile_owners[i]) == 1
        assert gnft_token.ownerOf(123 + i) == genetic_profile_owners[i]

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 194000000e+18


def test_success__mint_batch_gnft__mint_double_30_new_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    #  ===== first 30 new token =====
    genetic_profile_ids = []
    genetic_profile_owners = []

    for i in range(0, 30):
        genetic_profile_ids.append(123 + i)
        genetic_profile_owners.append(accounts.add())

    # Actions
    gnft_token.mintBatchGNFT(
        genetic_profile_owners, genetic_profile_ids, {"from": gfn_owner1}
    )

    # Asserts: GNFTToken status
    assert gnft_token.getTotalMintedGeneticProfiles() == 30
    assert gnft_token.getTotalCurrentTokens() == 30

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 200000000e+18

    #  ===== second 30 new token =====
    genetic_profile_ids = []
    genetic_profile_owners = []

    for i in range(30, 60):
        genetic_profile_ids.append(123 + i)
        genetic_profile_owners.append(accounts.add())

    # Actions
    gnft_token.mintBatchGNFT(
        genetic_profile_owners, genetic_profile_ids, {"from": gfn_owner1}
    )

    # Asserts: GNFTToken status
    assert gnft_token.getTotalMintedGeneticProfiles() == 60
    assert gnft_token.getTotalCurrentTokens() == 60

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 230000000e+18
