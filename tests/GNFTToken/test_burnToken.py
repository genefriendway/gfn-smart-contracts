import brownie
import pytest
from brownie import accounts


@pytest.fixture(scope="function")
def setup(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintToken(genetic_owner1, token_id, {"from": gfn_owner1})


def test_success__burn_token(setup, deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    token_id = 12345678
    genetic_owner1 = accounts[2]

    # Assert before burning token
    # # Asserts
    assert gnft_token.getTotalTokens() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(12345678) == genetic_owner1

    # Actions
    gnft_token.burnToken(token_id, {"from": gfn_owner1})

    # # Asserts
    assert gnft_token.getTotalTokens() == 0
    assert gnft_token.balanceOf(genetic_owner1) == 0
    with brownie.reverts("ERC721: owner query for nonexistent token"):
        assert gnft_token.ownerOf(12345678)


def test_failed__burn_token__not_gfn_owner_burn_token(setup, deployment, const):
    # Arranges
    gnft_token = deployment[const.GNFT_TOKEN]
    genetic_owner1 = accounts[2]

    # Actions
    # genetic_owner1 make a transaction to burn their token id
    with brownie.reverts("Ownable: caller is not the owner"):
        gnft_token.burnToken(12345678, {"from": genetic_owner1})


def test_failed__burn_token__not_existed_token_id(setup, deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    other_token_id = 88888888
    genetic_owner1 = accounts[2]

    # Assert before burning token
    assert gnft_token.getTotalTokens() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(12345678) == genetic_owner1

    # Actions
    with brownie.reverts("GNFTToken: token id must exist for burning"):
        gnft_token.burnToken(other_token_id, {"from": gfn_owner1})

    # Assert after burning token
    assert gnft_token.getTotalTokens() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(12345678) == genetic_owner1