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

    # # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.getTotalCurrentTokens() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(genetic_profile_id1) == genetic_owner1


def test_success__mint_batch_gnft__mint_02_new_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

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

    # # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 2
    assert gnft_token.getTotalCurrentTokens() == 2
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.balanceOf(genetic_owner2) == 1
    assert gnft_token.ownerOf(genetic_profile_id1) == genetic_owner1
    assert gnft_token.ownerOf(genetic_profile_id2) == genetic_owner2


def test_success__mint_batch_gnft__mint_08_new_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

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

    # # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 8
    assert gnft_token.getTotalCurrentTokens() == 8

    for i in range(2, 10):
        assert gnft_token.balanceOf(accounts[i]) == 1
        assert gnft_token.ownerOf(12345678 + i) == accounts[i]
