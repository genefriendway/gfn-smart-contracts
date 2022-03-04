import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__set_gfn_operator(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_operator = deployment[const.GFN_OPERATOR]
    registry = deployment[const.REGISTRY]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]

    old_gfn_operator = gfn_operator
    gnft_operator = accounts.add()
    life_operator = accounts.add()

    # Actions: set GFN Operator for GNFTToken contract
    tx = registry.setGFNOperator(
        gnft_token.address, gnft_operator, {"from": gfn_owner1}
    )

    # Assert: RegisterContract Event
    assert ('SetGFNOperator' in tx.events) is True
    assert tx.events['SetGFNOperator']['oldGFNOperator'] == old_gfn_operator.address
    assert tx.events['SetGFNOperator']['newGFNOperator'] == gnft_operator.address

    # # Asserts: after actions
    assert registry.getGFNOperator(gnft_token.address) == gnft_operator.address

    # Actions: set GFN Operator for LIFEToken contract
    tx = registry.setGFNOperator(
        life_token.address, life_operator, {"from": gfn_owner1}
    )

    # Assert: RegisterContract Event
    assert ('SetGFNOperator' in tx.events) is True
    assert tx.events['SetGFNOperator']['oldGFNOperator'] == old_gfn_operator.address
    assert tx.events['SetGFNOperator']['newGFNOperator'] == life_operator.address

    # # Asserts: after actions
    assert registry.getGFNOperator(life_token.address) == life_operator.address


def test_failure__set_gfn_operator__not_gfn_owner_set(deployment, const):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    registry = deployment[const.REGISTRY]
    gnft_token = deployment[const.GNFT_TOKEN]
    fake_gfn_owner = accounts.add()

    gnft_operator = accounts.add()

    # Actions: set GFN Operator for GNFTToken contract
    with brownie.reverts("Ownable: caller is not the owner"):
        registry.setGFNOperator(
            gnft_token.address, gnft_operator, {"from": fake_gfn_owner}
        )

    # # Asserts: after actions
    assert registry.getGFNOperator(gnft_token.address) == gfn_operator.address


def test_failure__set_gfn_operator__invalid_gnf_operator(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_operator = deployment[const.GFN_OPERATOR]
    gnft_token = deployment[const.GNFT_TOKEN]
    registry = deployment[const.REGISTRY]

    gnft_operator = '0x0000000000000000000000000000000000000000'

    # Actions: set GFN Operator for GNFTToken contract
    with brownie.reverts("ContractRegistry: new GFN operator must be not empty"):
        registry.setGFNOperator(
            gnft_token.address, gnft_operator, {"from": gfn_owner1}
        )

    # # Asserts: after actions
    assert registry.getGFNOperator(gnft_token.address) == gfn_operator.address
