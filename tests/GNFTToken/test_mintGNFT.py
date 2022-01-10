import brownie

from brownie import accounts


def test_success__mint_token__mint_01_new_GNFT_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id1 = 12345678
    genetic_profile_id = 'abcxyz'
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintGNFT(
        genetic_owner1, genetic_profile_id, token_id1, {"from": gfn_owner1}
    )

    # # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.getTotalCurrentTokens() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(token_id1) == genetic_owner1


def test_success__mint_token__mint_02_new_GNFT_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id1 = 12345678
    genetic_profile_id = 'abcxyz'
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintGNFT(
        genetic_owner1, genetic_profile_id, token_id1, {"from": gfn_owner1}
    )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.getTotalCurrentTokens() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(token_id1) == genetic_owner1

    # continue to mint another GNFT
    # Arranges
    token_id2 = 23456743
    genetic_profile_id2 = '123abc'
    genetic_owner2 = accounts[3]

    # Actions
    gnft_token.mintGNFT(
        genetic_owner2, genetic_profile_id2, token_id2, {"from": gfn_owner1}
    )

    # # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 2
    assert gnft_token.getTotalCurrentTokens() == 2
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.balanceOf(genetic_owner2) == 1
    assert gnft_token.ownerOf(token_id1) == genetic_owner1
    assert gnft_token.ownerOf(token_id2) == genetic_owner2


def test_failed__mint_token__not_gfn_owner_mint_token(deployment, const):
    # Arranges
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id1 = 12345678
    genetic_profile_id = 'abcxyz'
    genetic_owner1 = accounts[2]

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        gnft_token.mintGNFT(
            genetic_owner1, genetic_profile_id, token_id1, {"from": genetic_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 0
    assert gnft_token.getTotalCurrentTokens() == 0


def test_failed__mint_token__null_genetic_profile_address(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id1 = 12345678
    genetic_profile_id1 = 'abczyz'
    genetic_owner1 = '0x0000000000000000000000000000000000000000'

    # Actions
    with brownie.reverts('ERC721: mint to the zero address'):
        gnft_token.mintGNFT(
            genetic_owner1, genetic_profile_id1, token_id1, {"from": gfn_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 0
    assert gnft_token.getTotalCurrentTokens() == 0


def test_failed__mint_token__null_genetic_profile_id(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id1 = 12345678
    genetic_profile_id1 = ''
    genetic_owner1 = accounts[2]

    # Actions
    with brownie.reverts('GNFTToken: genetic profile id must not be null'):
        gnft_token.mintGNFT(
            genetic_owner1, genetic_profile_id1, token_id1, {"from": gfn_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 0
    assert gnft_token.getTotalCurrentTokens() == 0


def test_failed__mint_token__existed_token_id(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id1 = 12345678
    genetic_profile_id1 = 'abcxyz'
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintGNFT(
        genetic_owner1, genetic_profile_id1, token_id1, {"from": gfn_owner1}
    )

    # continue to mint same token id again for genetic_owner2
    # Arranges
    token_id2 = 12345678
    genetic_profile_id1 = 'mnqhtn'
    genetic_owner2 = accounts[3]
    # # Actions
    with brownie.reverts("ERC721: token already minted"):
        gnft_token.mintGNFT(
            genetic_owner2, genetic_profile_id1, token_id2, {"from": gfn_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.getTotalCurrentTokens() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(token_id1) == genetic_owner1
