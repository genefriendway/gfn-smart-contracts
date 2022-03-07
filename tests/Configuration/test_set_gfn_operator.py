import pytest
import brownie
from brownie import accounts, GNFTToken


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__set_gfn_operator(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_operator = deployment[const.GFN_OPERATOR]
    configuration = deployment[const.CONFIGURATION]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_token = deployment[const.LIFE_TOKEN]

    old_gfn_operator = gfn_operator
    gnft_operator = accounts.add()
    life_operator = accounts.add()

    # Actions: set GFN Operator for GNFTToken contract
    tx = configuration.setOperator(
        gnft_token.address, gnft_operator, {"from": gfn_owner1}
    )

    # Assert: RegisterContract Event
    assert ('SetOperator' in tx.events) is True
    assert tx.events['SetOperator']['contractAddress'] == gnft_token.address
    assert tx.events['SetOperator']['oldOperator'] == old_gfn_operator.address
    assert tx.events['SetOperator']['newOperator'] == gnft_operator.address

    # # Asserts: after actions
    assert configuration.getOperator(gnft_token.address) == gnft_operator.address

    # Actions: set GFN Operator for LIFEToken contract
    tx = configuration.setOperator(
        life_token.address, life_operator, {"from": gfn_owner1}
    )

    # Assert: RegisterContract Event
    assert ('SetOperator' in tx.events) is True
    assert tx.events['SetOperator']['oldOperator'] == old_gfn_operator.address
    assert tx.events['SetOperator']['newOperator'] == life_operator.address

    # # Asserts: after actions
    assert configuration.getOperator(life_token.address) == life_operator.address


def test_failure__set_gfn_operator__not_gfn_owner_set(deployment, const):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    configuration = deployment[const.CONFIGURATION]
    gnft_token = deployment[const.GNFT_TOKEN]
    fake_gfn_owner = accounts.add()

    gnft_operator = accounts.add()

    # Actions: set GFN Operator for GNFTToken contract
    with brownie.reverts("Ownable: caller is not the owner"):
        configuration.setOperator(
            gnft_token.address, gnft_operator, {"from": fake_gfn_owner}
        )

    # # Asserts: after actions
    assert configuration.getOperator(gnft_token.address) == gfn_operator.address


def test_failure__set_gfn_operator__invalid_contract_address(deployment, const):
    # Arranges
    gfn_deployer = deployment[const.GFN_DEPLOYER]
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_operator = deployment[const.GFN_OPERATOR]
    registry = deployment[const.REGISTRY]
    configuration = deployment[const.CONFIGURATION]

    not_registered_gnft_token = GNFTToken.deploy(
        registry, "GNFT", "GNFT", {"from": gfn_deployer}
    )

    # Actions: set GFN Operator for not registered GNFTToken contract
    with brownie.reverts("Configuration: contract address must be registered "
                         "in registry"):
        configuration.setOperator(
            not_registered_gnft_token.address,
            gfn_operator,
            {"from": gfn_owner1}
        )

    # # Asserts: after actions
    assert configuration.getOperator(not_registered_gnft_token.address) == '0x0000000000000000000000000000000000000000'


def test_failure__set_gfn_operator__invalid_gnf_operator(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_operator = deployment[const.GFN_OPERATOR]
    gnft_token = deployment[const.GNFT_TOKEN]
    configuration = deployment[const.CONFIGURATION]

    gnft_operator = '0x0000000000000000000000000000000000000000'

    # Actions: set GFN Operator for GNFTToken contract
    with brownie.reverts("Configuration: new operator must be not empty"):
        configuration.setOperator(
            gnft_token.address, gnft_operator, {"from": gfn_owner1}
        )

    # # Asserts: after actions
    assert configuration.getOperator(gnft_token.address) == gfn_operator.address
