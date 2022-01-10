import brownie

from brownie import accounts


def test_success__mint_token__mint_01_GNFT_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintGNFT(genetic_owner1, token_id, {"from": gfn_owner1})

    # # Asserts
    assert gnft_token.getTotalGeneticProfiles() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(token_id) == genetic_owner1


def test_success__mint_token__mint_02_GNFT_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintGNFT(genetic_owner1, token_id, {"from": gfn_owner1})

    # Asserts
    assert gnft_token.getTotalGeneticProfiles() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(token_id) == genetic_owner1

    # continue to mint another GNFT
    # Arranges
    token_id2 = 23456743
    genetic_owner2 = accounts[3]

    # Actions
    gnft_token.mintGNFT(genetic_owner2, token_id2, {"from": gfn_owner1})

    # # Asserts
    assert gnft_token.getTotalGeneticProfiles() == 2
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.balanceOf(genetic_owner2) == 1
    assert gnft_token.ownerOf(token_id) == genetic_owner1
    assert gnft_token.ownerOf(token_id2) == genetic_owner2


def test_failed__mint_token__not_gfn_owner_mint_token(deployment, const):
    # Arranges
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        gnft_token.mintGNFT(genetic_owner1, token_id, {"from": genetic_owner1})


def test_failed__mint_token__genetic_owner_had_minted_GNFT(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintGNFT(genetic_owner1, token_id, {"from": gfn_owner1})

    # continue to mint another GNFT for the same genetic_owner1
    # Arranges
    # token_id2 = 122432465464
    # # Actions
    # with brownie.reverts("GNFTToken: genetic owner had GNFT token."):
    #     gnft_token.mintGNFT(genetic_owner1, token_id2, {"from": gfn_owner1})

    # Asserts
    assert gnft_token.getTotalGeneticProfiles() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(token_id) == genetic_owner1


def test_failed__mint_token__existed_GNFT_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintGNFT(genetic_owner1, token_id, {"from": gfn_owner1})

    # continue to mint another GNFT for the same genetic_owner1
    # Arranges
    token_id2 = 12345678  # same token id above
    genetic_owner2 = accounts[3]
    # Actions
    with brownie.reverts("ERC721: token already minted"):
        gnft_token.mintGNFT(genetic_owner2, token_id2, {"from": gfn_owner1})

    # Asserts
    assert gnft_token.getTotalGeneticProfiles() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.balanceOf(genetic_owner2) == 0
    assert gnft_token.ownerOf(token_id) == genetic_owner1
