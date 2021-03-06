#!/usr/bin/python3
from utils.datetime import DateTimeUtil
from brownie import accounts, network

from constants.common import ContractName


OUTPUT_FILE = "deployment_{env}_{network}_{time}.json"


class Setting:

    def __init__(self, env_settings: dict):
        now = DateTimeUtil.now()

        self.ENV_NAME = env_settings['ENV_NAME']
        self.BLOCKCHAIN_NETWORK = network.show_active()
        self.GFN_DEPLOYER_PRIVATE_KEY = env_settings['GFN_DEPLOYER_PRIVATE_KEY']
        self.GFN_REGISTRY_OWNER_ADDRESS = env_settings['GFN_REGISTRY_OWNER_ADDRESS']
        self.GFN_CONFIGURATION_OWNER_ADDRESS = env_settings['GFN_CONFIGURATION_OWNER_ADDRESS']
        self.GFN_GNFT_OPERATOR_ADDRESS = env_settings['GFN_GNFT_OPERATOR_ADDRESS']
        self.GFN_EXCHANGE_WALLET_OPERATOR_ADDRESS = env_settings.get('GFN_EXCHANGE_WALLET_OPERATOR_ADDRESS')
        self.GFN_PROFIT_WALLET_OPERATOR_ADDRESS = env_settings.get('GFN_PROFIT_WALLET_OPERATOR_ADDRESS')
        self.GFN_EXCHANGE_LIFE_BANK_OPERATOR_ADDRESS = env_settings.get('GFN_EXCHANGE_LIFE_BANK_OPERATOR_ADDRESS')
        self.GFN_NFT_HOLDER_ADDRESS = env_settings['GFN_NFT_HOLDER_ADDRESS']

        self.GNFT_TOKEN_NAME = env_settings.get('GNFT_TOKEN_NAME')
        self.GNFT_TOKEN_SYMBOL = env_settings.get('GNFT_TOKEN_SYMBOL')

        self.LIFE_TOKEN_NAME = env_settings.get('LIFE_TOKEN_NAME')
        self.LIFE_TOKEN_SYMBOL = env_settings.get('LIFE_TOKEN_SYMBOL')

        self.GFN_FOUNDER_ADDRESS_ONE = env_settings.get('GFN_FOUNDER_ADDRESS_ONE')
        self.GFN_FOUNDER_ADDRESS_TWO = env_settings.get('GFN_FOUNDER_ADDRESS_TWO')
        self.GFN_FOUNDER_ADDRESS_THREE = env_settings.get('GFN_FOUNDER_ADDRESS_THREE')

        self.LIFE_TREASURY_ADDRESS = env_settings['LIFE_TREASURY_ADDRESS']

        self.DEPLOYMENT_OUTPUT = OUTPUT_FILE.format(
            env=self.ENV_NAME.lower(),
            network=self.BLOCKCHAIN_NETWORK,
            time=DateTimeUtil.date_to_text(now, '%Y_%m_%d_%H_%M_%S')
        )
        self.DEPLOYMENT_DATETIME = DateTimeUtil.date_to_text(
            now, fmt='%d/%m/%Y %H:%M:%S'
        )
        gfn_deployer = accounts.add(self.GFN_DEPLOYER_PRIVATE_KEY)
        self.GFN_DEPLOYER_ADDRESS = gfn_deployer.address
        self.TXN_SENDER = {'from': self.GFN_DEPLOYER_ADDRESS}
        self.CONTRACT_OPERATORS = {
            ContractName.GNFT_TOKEN: self.GFN_GNFT_OPERATOR_ADDRESS,
            ContractName.GFN_EXCHANGE_WALLET: self.GFN_EXCHANGE_WALLET_OPERATOR_ADDRESS,
            ContractName.GFN_PROFIT_WALLET: self.GFN_PROFIT_WALLET_OPERATOR_ADDRESS,
            ContractName.GFN_EXCHANGE_LIFE_BANK: self.GFN_EXCHANGE_LIFE_BANK_OPERATOR_ADDRESS,
        }
