import pytest
import brownie

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


def test_success__mint_token__mint_01_new_gnft_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_profile_id1 = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    tx = gnft_token.mintGNFT(
        genetic_owner1, genetic_profile_id1, {"from": gfn_owner1}
    )

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


def test_success__mint_token__mint_02_new_gnft_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_profile_id1 = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintGNFT(
        genetic_owner1, genetic_profile_id1, {"from": gfn_owner1}
    )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.getTotalCurrentTokens() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(genetic_profile_id1) == genetic_owner1

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 90000000e+18

    # continue to mint another GNFT
    # Arranges
    genetic_profile_id2 = 23456743
    genetic_owner2 = accounts[3]

    # Actions
    gnft_token.mintGNFT(
        genetic_owner2, genetic_profile_id2, {"from": gfn_owner1}
    )

    # # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 2
    assert gnft_token.getTotalCurrentTokens() == 2
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.balanceOf(genetic_owner2) == 1
    assert gnft_token.ownerOf(genetic_profile_id1) == genetic_owner1
    assert gnft_token.ownerOf(genetic_profile_id2) == genetic_owner2

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 100000000e+18


def test_failure__mint_token__not_gfn_owner_mint_gnft_token(deployment, const):
    # Arranges
    gnft_token = deployment[const.GNFT_TOKEN]

    genetic_profile_id1 = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        gnft_token.mintGNFT(
            genetic_owner1, genetic_profile_id1, {"from": genetic_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 0
    assert gnft_token.getTotalCurrentTokens() == 0


def test_failure__mint_token__life_token_not_registered(const):
    # Arranges
    gfn_deployer = accounts[0]
    gfn_owner1 = accounts[1]

    # deploy smart contracts and get instance of them
    registry = ContractRegistry.deploy(
        gfn_owner1, {'from': gfn_deployer}
    )
    gnft_token = GNFTToken.deploy(
        gfn_owner1, registry, "GNFT", "GNFT", {'from': gfn_deployer}
    )

    # add deployed smart contracts to ContractRegistry
    registry.registerContract(
        const.GNFT_TOKEN, gnft_token.address, {'from': gfn_owner1}
    )

    genetic_profile_id1 = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    with brownie.reverts("GNFTToken: Please register LIFEToken on ContractRegistry"):
        gnft_token.mintGNFT(
            genetic_owner1, genetic_profile_id1, {"from": gfn_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 0
    assert gnft_token.getTotalCurrentTokens() == 0


def test_failure__mint_token__life_treasury_not_registered(const):
    # Arranges
    gfn_deployer = accounts[0]
    gfn_owner1 = accounts[1]

    # deploy smart contracts and get instance of them
    registry = ContractRegistry.deploy(
        gfn_owner1, {'from': gfn_deployer}
    )
    gnft_token = GNFTToken.deploy(
        gfn_owner1, registry, "GNFT", "GNFT", {'from': gfn_deployer}
    )
    life_token = LIFEToken.deploy(
        gfn_owner1, registry, "LIFE", "LIFE", {'from': gfn_deployer}
    )

    # add deployed smart contracts to ContractRegistry
    registry.registerContract(
        const.GNFT_TOKEN, gnft_token.address, {'from': gfn_owner1}
    )
    registry.registerContract(
        const.LIFE_TOKEN, life_token.address, {'from': gfn_owner1}
    )

    genetic_profile_id1 = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    with brownie.reverts("GNFTToken: Please register LIFETreasury on ContractRegistry"):
        gnft_token.mintGNFT(
            genetic_owner1, genetic_profile_id1, {"from": gfn_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 0
    assert gnft_token.getTotalCurrentTokens() == 0


def test_failure__mint_token__null_genetic_profile_address(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    genetic_profile_id1 = 12345678
    genetic_owner1 = '0x0000000000000000000000000000000000000000'

    # Actions
    with brownie.reverts('ERC721: mint to the zero address'):
        gnft_token.mintGNFT(
            genetic_owner1, genetic_profile_id1, {"from": gfn_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 0
    assert gnft_token.getTotalCurrentTokens() == 0


def test_failure__mint_token__existed_genetic_profile_id(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    genetic_profile_id1 = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintGNFT(
        genetic_owner1, genetic_profile_id1, {"from": gfn_owner1}
    )

    # continue to mint same token id again for genetic_owner2
    # Arranges
    genetic_profile_id2 = 12345678
    genetic_owner2 = accounts[3]
    # # Actions
    with brownie.reverts("ERC721: token already minted"):
        gnft_token.mintGNFT(
            genetic_owner2, genetic_profile_id1, {"from": gfn_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.getTotalCurrentTokens() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(genetic_profile_id1) == genetic_owner1
