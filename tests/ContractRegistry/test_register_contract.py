import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__register_contract(registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]
    gnft_token = registry_deployment[const.GNFT_TOKEN]

    # Asserts: before registering Contract
    gnft_address = registry.getContractAddress('AnyName')
    gnft_name = registry.getContractName(gnft_token.address)
    assert gnft_address == '0x0000000000000000000000000000000000000000'
    assert gnft_name == ''

    # Actions
    tx = registry.registerContract(
        'AnyName', gnft_token.address, {"from": gfn_owner1}
    )

    # Assert: RegisterContract Event
    assert ('RegisterContract' in tx.events) is True
    assert tx.events['RegisterContract']['name'] == 'AnyName'
    assert tx.events['RegisterContract']['_address'] == gnft_token.address

    # # Asserts: after registering Contract
    gnft_address = registry.getContractAddress('AnyName')
    gnft_name = registry.getContractName(gnft_token.address)
    assert gnft_address == gnft_token.address
    assert gnft_name == 'AnyName'


def test_failure__register_contract__empty_contract_name(registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]
    gnft_token = registry_deployment[const.GNFT_TOKEN]

    # Actions
    with brownie.reverts('ContractRegistry: contract name must not be empty'):
        registry.registerContract('', gnft_token.address, {"from": gfn_owner1})


def test_failure__register_contract__duplicated_contract_name(registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]
    gnft_token = registry_deployment[const.GNFT_TOKEN]
    life_token = registry_deployment[const.LIFE_TOKEN]

    # Actions
    # register a GNFT contract with name GNFTContract
    registry.registerContract(
        'GNFTContract', gnft_token.address, {"from": gfn_owner1}
    )
    # continue to register a LIFE contract with existed name 'GNFTContract'
    with brownie.reverts('ContractRegistry: contract name is registered'):
        registry.registerContract(
            'GNFTContract', life_token.address, {"from": gfn_owner1}
        )


def test_failure__register_contract__empty_address(registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]

    # Actions
    with brownie.reverts('ContractRegistry: contract address is invalid'):
        registry.registerContract(
            'ValidName', '0x0000000000000000000000000000000000000000', {"from": gfn_owner1}
        )


def test_failure__register_contract__duplicated_contract_address(registry_deployment, const):
    # Arranges
    gfn_owner1 = registry_deployment[const.GFN_OWNER1]
    registry = registry_deployment[const.REGISTRY]
    gnft_token = registry_deployment[const.GNFT_TOKEN]

    # Actions
    # register a GNFT contract with name GNFTContract
    registry.registerContract(
        'GNFTContract', gnft_token.address, {"from": gfn_owner1}
    )
    # continue to register a LIFE contract with existed address
    with brownie.reverts('ContractRegistry: contract address is registered'):
        registry.registerContract(
            'LIFEContract', gnft_token.address, {"from": gfn_owner1}
        )


def test_failure__register_contract__not_owner_make_transaction(
        registry_deployment, const
):
    # Arranges
    registry = registry_deployment[const.REGISTRY]
    gnft_token = registry_deployment[const.GNFT_TOKEN]

    fake_owner = accounts.add()

    # Actions
    with brownie.reverts('Ownable: caller is not the owner'):
        registry.registerContract(
            'AnyName', gnft_token.address, {"from": fake_owner}
        )