from constants import ContractName
from scripts.settings import Setting
from scripts.utils import assert_equal


class Verification:

    def __init__(self, setting: Setting, contract_instances: dict):
        self.setting = setting
        self.contract_instances = contract_instances
        self.registry = contract_instances.get(ContractName.REGISTRY)
        self.configuration = contract_instances.get(ContractName.CONFIGURATION)
        self.gnft_token = contract_instances.get(ContractName.GNFT_TOKEN)
        self.life_token = contract_instances.get(ContractName.LIFE_TOKEN)
        self.gfn_exchange_wallet = contract_instances.get(
            ContractName.GFN_EXCHANGE_WALLET
        )
        self.gfn_profit_wallet = contract_instances.get(
            ContractName.GFN_PROFIT_WALLET
        )
        self.gfn_exchange_life_bank = contract_instances.get(
            ContractName.GFN_EXCHANGE_LIFE_BANK
        )

    def start(self):
        self.verify_contract_registry()
        self.verify_configuration_contract()
        self.verify_gnft_token_contract()
        self.verify_life_token_contract()
        self.verify_life_treasury_contract()
        self.verify_gfn_profit_wallet_contract()
        self.verify_gfn_exchange_wallet_contract()
        self.verify_gfn_exchange_life_bank_contract()

    def verify_contract_registry(self):
        assert_equal(
            title="Registry: Verify Owner",
            value1=self.registry.owner(),
            value2=self.setting.GFN_REGISTRY_OWNER_ADDRESS
        )

    def verify_configuration_contract(self):
        assert_equal(
            title=f"Configuration: Verify Register Contract",
            value1=self.registry.getContractAddress(ContractName.CONFIGURATION),
            value2=self.configuration.address
        )
        assert_equal(
            title="Configuration: Verify Owner",
            value1=self.configuration.owner(),
            value2=self.setting.GFN_CONFIGURATION_OWNER_ADDRESS
        )

    def verify_gnft_token_contract(self):
        assert_equal(
            title=f"GNFTToken: Verify Register Contract",
            value1=self.registry.getContractAddress(ContractName.GNFT_TOKEN),
            value2=self.gnft_token.address
        )
        assert_equal(
            title="GFNTToken: Verify Operator",
            value1=self.configuration.getOperator(self.gnft_token.address),
            value2=self.setting.GFN_GNFT_OPERATOR_ADDRESS
        )
        assert_equal(
            title="GFNTToken: Verify Holder of Gene-NFT",
            value1=self.configuration.getNFTHolder(),
            value2=self.setting.GFN_NFT_HOLDER_ADDRESS
        )

    def verify_life_token_contract(self):
        assert_equal(
            title=f"LIFEToken: Verify Register Contract",
            value1=self.registry.getContractAddress(ContractName.LIFE_TOKEN),
            value2=self.life_token.address
        )

    def verify_life_treasury_contract(self):
        assert_equal(
            title=f"LIFETreasury: Verify Register Contract",
            value1=self.registry.getContractAddress(ContractName.LIFE_TREASURY),
            value2=self.setting.LIFE_TREASURY_ADDRESS
        )

    def verify_gfn_exchange_wallet_contract(self):
        assert_equal(
            title=f"GFNExchangeWallet: Verify Register Contract",
            value1=self.registry.getContractAddress(ContractName.GFN_EXCHANGE_WALLET),
            value2=self.gfn_exchange_wallet.address
        )
        assert_equal(
            title="GFNExchangeWallet: Verify Operator",
            value1=self.configuration.getOperator(self.gfn_exchange_wallet.address),
            value2=self.setting.GFN_EXCHANGE_WALLET_OPERATOR_ADDRESS
        )

    def verify_gfn_profit_wallet_contract(self):
        assert_equal(
            title=f"GFNProfitWallet: Verify Register Contract",
            value1=self.registry.getContractAddress(ContractName.GFN_PROFIT_WALLET),
            value2=self.gfn_profit_wallet.address
        )
        assert_equal(
            title="GFNProfitWallet: Verify Operator",
            value1=self.configuration.getOperator(self.gfn_profit_wallet.address),
            value2=self.setting.GFN_PROFIT_WALLET_OPERATOR_ADDRESS
        )

    def verify_gfn_exchange_life_bank_contract(self):
        assert_equal(
            title=f"GFNExchangeLIFEBank: Verify Register Contract",
            value1=self.registry.getContractAddress(
                ContractName.GFN_EXCHANGE_LIFE_BANK),
            value2=self.gfn_exchange_life_bank.address
        )
        assert_equal(
            title="GFNExchangeLIFEBank: Verify Operator",
            value1=self.configuration.getOperator(self.gfn_exchange_life_bank.address),
            value2=self.setting.GFN_EXCHANGE_LIFE_BANK_OPERATOR_ADDRESS
        )
