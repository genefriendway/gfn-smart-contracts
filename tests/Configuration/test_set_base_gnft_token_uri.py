import pytest
import brownie


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__set_base_gnft_token_uri(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    config = deployment[const.CONFIGURATION]

    # Asserts: before actions
    assert config.getBaseGNFTTokenURI() == ""

    # Actions
    tx = config.setBaseGNFTTokenURI(
        'https://genetica.asis/gnft/', {"from": gfn_owner1}
    )

    # Assert: SetBaseGNFTTokenURI Event
    assert ('SetBaseGNFTTokenURI' in tx.events) is True
    assert tx.events['SetBaseGNFTTokenURI']['uri'] == 'https://genetica.asis/gnft/'

    # # Asserts: after actions
    assert config.getBaseGNFTTokenURI() == "https://genetica.asis/gnft/"

    # Actions: continue settings
    tx = config.setBaseGNFTTokenURI('abc-xyz', {"from": gfn_owner1})

    # Assert: SetBaseGNFTTokenURI Event
    assert ('SetBaseGNFTTokenURI' in tx.events) is True
    assert tx.events['SetBaseGNFTTokenURI']['uri'] == 'abc-xyz'

    # # Asserts: after actions
    assert config.getBaseGNFTTokenURI() == 'abc-xyz'


def test_failure__set_base_gnft_token_uri(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    config = deployment[const.CONFIGURATION]

    # Asserts: before actions
    assert config.getBaseGNFTTokenURI() == ""

    # Actions
    with brownie.reverts("Configuration: base G-NFT token URI must be not empty"):
        config.setBaseGNFTTokenURI('', {"from": gfn_owner1})

    assert config.getBaseGNFTTokenURI() == ""
