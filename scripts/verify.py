from constants import ContractName
from scripts.settings import Setting
from scripts.utils import assert_equal


def verify_deployment(setting: Setting, contract_instances: dict):
    registry = contract_instances[ContractName.REGISTRY]
    configuration = contract_instances[ContractName.CONFIGURATION]
    gnft_token = contract_instances[ContractName.GNFT_TOKEN]
    life_token = contract_instances[ContractName.LIFE_TOKEN]

    # Verify Registry Contract
    assert_equal(
        title="Verify Owner of Registry",
        value1=registry.owner(),
        value2=setting.GFN_REGISTRY_OWNER_ADDRESS
    )
    assert_equal(
        title=f"Verify Register Contract {ContractName.CONFIGURATION}",
        value1=registry.getContractAddress(ContractName.CONFIGURATION),
        value2=configuration.address
    )
    assert_equal(
        title=f"Verify Register Contract{ContractName.GNFT_TOKEN}",
        value1=registry.getContractAddress(ContractName.GNFT_TOKEN),
        value2=gnft_token.address
    )
    assert_equal(
        title=f"Verify Register Contract {ContractName.LIFE_TOKEN}",
        value1=registry.getContractAddress(ContractName.LIFE_TOKEN),
        value2=life_token.address
    )

    # Verify Configuration contract
    print("-------------------------")
    assert_equal(
        title="Verify Owner of Configuration",
        value1=configuration.owner(),
        value2=setting.GFN_CONFIGURATION_OWNER_ADDRESS
    )
    assert_equal(
        title="Verify NFT Holder",
        value1=configuration.getNFTHolder(),
        value2=setting.GFN_NFT_HOLDER_ADDRESS
    )
    assert_equal(
        title="Verify operator of GFNTToken",
        value1=configuration.getOperator(gnft_token.address),
        value2=setting.GFN_GNFT_OPERATOR_ADDRESS
    )
