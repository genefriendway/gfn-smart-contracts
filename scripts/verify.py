from constants import ContractName
from scripts.settings import Setting
from scripts.utils import assert_equal


def verify_deployment(setting: Setting, contract_instances: dict):
    registry = contract_instances[ContractName.REGISTRY]
    configuration = contract_instances[ContractName.CONFIGURATION]
    gnft_token = contract_instances[ContractName.GNFT_TOKEN]
    life_token = contract_instances[ContractName.LIFE_TOKEN]
    gfn_exchange_wallet = contract_instances[ContractName.GFN_EXCHANGE_WALLET]
    gfn_profit_wallet = contract_instances[ContractName.GFN_PROFIT_WALLET]
    gfn_exchange_life_bank = contract_instances[ContractName.GFN_EXCHANGE_LIFE_BANK]

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
    assert_equal(
        title=f"Verify Register Contract {ContractName.LIFE_TREASURY}",
        value1=registry.getContractAddress(ContractName.LIFE_TREASURY),
        value2=setting.LIFE_TREASURY_ADDRESS
    )
    assert_equal(
        title=f"Verify Register Contract {ContractName.GFN_EXCHANGE_WALLET}",
        value1=registry.getContractAddress(ContractName.GFN_EXCHANGE_WALLET),
        value2=gfn_exchange_wallet.address
    )
    assert_equal(
        title=f"Verify Register Contract {ContractName.GFN_PROFIT_WALLET}",
        value1=registry.getContractAddress(ContractName.GFN_PROFIT_WALLET),
        value2=gfn_profit_wallet.address
    )
    assert_equal(
        title=f"Verify Register Contract {ContractName.GFN_EXCHANGE_LIFE_BANK}",
        value1=registry.getContractAddress(ContractName.GFN_EXCHANGE_LIFE_BANK),
        value2=gfn_exchange_life_bank.address
    )

    # Verify Configuration contract
    print("-------------------------")
    assert_equal(
        title="Verify Owner of Configuration",
        value1=configuration.owner(),
        value2=setting.GFN_CONFIGURATION_OWNER_ADDRESS
    )
    assert_equal(
        title="Verify Holder of Gene-NFT",
        value1=configuration.getNFTHolder(),
        value2=setting.GFN_NFT_HOLDER_ADDRESS
    )
    assert_equal(
        title="Verify Operator of GFNTToken",
        value1=configuration.getOperator(gnft_token.address),
        value2=setting.GFN_GNFT_OPERATOR_ADDRESS
    )
    assert_equal(
        title="Verify Operator of GFN Exchange Wallet",
        value1=configuration.getOperator(gfn_exchange_wallet.address),
        value2=setting.GFN_EXCHANGE_WALLET_OPERATOR_ADDRESS
    )

    assert_equal(
        title="Verify Operator of GFN Profit Wallet",
        value1=configuration.getOperator(gfn_profit_wallet.address),
        value2=setting.GFN_PROFIT_WALLET_OPERATOR_ADDRESS
    )

    assert_equal(
        title="Verify Operator of GFN Exchange LIFE Bank",
        value1=configuration.getOperator(gfn_exchange_life_bank.address),
        value2=setting.GFN_EXCHANGE_LIFE_BANK_OPERATOR_ADDRESS
    )
