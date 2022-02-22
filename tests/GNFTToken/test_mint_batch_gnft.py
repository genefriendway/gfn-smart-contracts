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


@pytest.fixture(scope="module")
def setup_base_gnft_uri(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    config = deployment[const.CONFIGURATION]

    # Asserts: before actions
    assert config.getBaseGNFTTokenURI() == ""

    # Actions
    config.setBaseGNFTTokenURI(
        'https://genetica.asia/gnft/', {"from": gfn_owner1}
    )

    # Asserts: before actions
    assert config.getBaseGNFTTokenURI() == "https://genetica.asia/gnft/"


def test_success__mint_batch_gnft__mint_01_new_token(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]
    config = deployment[const.CONFIGURATION]

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
    assert gnft_token.totalSupply() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(genetic_profile_id1) == genetic_owner1

    assert gnft_token.tokenURI(12345678) == ""

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 90000000e+18

    # Actions: Setup Token URI
    config.setBaseGNFTTokenURI(
        'https://genetica.asia/gnft/', {"from": gfn_owner1}
    )
    assert gnft_token.tokenURI(12345678) == "https://genetica.asia/gnft/12345678"


def test_success__mint_batch_gnft__mint_01_new_token_with_existed_token_uri(
        deployment, setup_base_gnft_uri, const, 
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_profile_id1 = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintBatchGNFT(
        [genetic_owner1], [genetic_profile_id1], {"from": gfn_owner1}
    )

    # Asserts: GNFTToken status
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.totalSupply() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(genetic_profile_id1) == genetic_owner1

    assert gnft_token.tokenURI(12345678) == "https://genetica.asia/gnft/12345678"

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
    assert gnft_token.totalSupply() == 2
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
    assert gnft_token.totalSupply() == 8

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
    assert gnft_token.totalSupply() == 24

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
    assert gnft_token.totalSupply() == 30

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
    assert gnft_token.totalSupply() == 60

    # Asserts: LIFEToken Status
    assert life_token.balanceOf(life_treasury) == 230000000e+18


def test_failure__mint_batch_token__not_gfn_owner_mint_gnft_token(
        deployment, const
):
    # Arranges
    gnft_token = deployment[const.GNFT_TOKEN]

    genetic_profile_id1 = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        gnft_token.mintBatchGNFT(
            [genetic_owner1], [genetic_profile_id1], {"from": genetic_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 0
    assert gnft_token.totalSupply() == 0


def test_failure__mint_batch_token__life_token_not_registered(const):
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
        gnft_token.mintBatchGNFT(
            [genetic_owner1], [genetic_profile_id1], {"from": gfn_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 0
    assert gnft_token.totalSupply() == 0


def test_failure__mint_batch_token__life_treasury_not_registered(const):
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
        gnft_token.mintBatchGNFT(
            [genetic_owner1], [genetic_profile_id1], {"from": gfn_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 0
    assert gnft_token.totalSupply() == 0


def test_failure__mint_batch_token__null_genetic_profile_address(
        deployment, const
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    genetic_profile_id1 = 12345678
    genetic_owner1 = '0x0000000000000000000000000000000000000000'

    genetic_profile_id2 = 876545678
    genetic_owner2 = accounts.add()

    # Actions
    with brownie.reverts('ERC721: mint to the zero address'):
        gnft_token.mintBatchGNFT(
            [genetic_owner1, genetic_owner2],
            [genetic_profile_id1, genetic_profile_id2],
            {"from": gfn_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 0
    assert gnft_token.totalSupply() == 0


def test_failure__mint_batch_token__existed_genetic_profile_id(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gnft_token = deployment[const.GNFT_TOKEN]

    genetic_profile_id1 = 12345678
    genetic_owner1 = accounts[2]

    # Actions
    gnft_token.mintBatchGNFT(
        [genetic_owner1], [genetic_profile_id1], {"from": gfn_owner1}
    )

    # continue to mint same token id again for genetic_owner2
    # Arranges
    genetic_owner2 = accounts.add()
    genetic_profile_id2 = 12345678

    genetic_owner3 = accounts.add()
    genetic_profile_id3 = 87654567

    # # Actions
    with brownie.reverts("ERC721: token already minted"):
        gnft_token.mintBatchGNFT(
            [genetic_owner2, genetic_owner3],
            [genetic_profile_id2, genetic_profile_id3],
            {"from": gfn_owner1}
        )

    # Asserts
    assert gnft_token.getTotalMintedGeneticProfiles() == 1
    assert gnft_token.totalSupply() == 1
    assert gnft_token.balanceOf(genetic_owner1) == 1
    assert gnft_token.ownerOf(genetic_profile_id1) == genetic_owner1