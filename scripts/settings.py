#!/usr/bin/python3
from utils.datetime import DateTimeUtil
from brownie import accounts, network


OUTPUT_FILE = "deployment_{env}_{network}_{time}.json"


class Setting:

    def __init__(self, env_settings: dict):
        now = DateTimeUtil.now()

        self.ENV_NAME = env_settings['ENV_NAME']
        self.BLOCKCHAIN_NETWORK = network.show_active()
        self.GFN_DEPLOYER_PRIVATE_KEY = env_settings['GFN_DEPLOYER_PRIVATE_KEY']
        self.GFN_OWNER_ADDRESS = env_settings['GFN_OWNER_ADDRESS']

        self.GNFT_TOKEN_NAME = env_settings.get('GNFT_TOKEN_NAME')
        self.GNFT_TOKEN_SYMBOL = env_settings.get('GNFT_TOKEN_SYMBOL')

        self.LIFE_TOKEN_NAME = env_settings.get('LIFE_TOKEN_NAME')
        self.LIFE_TOKEN_SYMBOL = env_settings.get('LIFE_TOKEN_SYMBOL')

        self.GFN_FOUNDER_ADDRESS_ONE = env_settings.get('GFN_FOUNDER_ADDRESS_ONE')
        self.GFN_FOUNDER_ADDRESS_TWO = env_settings.get('GFN_FOUNDER_ADDRESS_TWO')
        self.GFN_FOUNDER_ADDRESS_THREE = env_settings.get('GFN_FOUNDER_ADDRESS_THREE')

        self.DEPLOYMENT_OUTPUT = OUTPUT_FILE.format(
            env=self.ENV_NAME.lower(),
            network=self.BLOCKCHAIN_NETWORK,
            time=DateTimeUtil.date_to_text(now, '%Y_%m_%d_%H_%M_%S')
        )
        self.DEPLOYMENT_DATETIME = DateTimeUtil.date_to_text(
            now, fmt='%d/%m/%Y %H:%M:%S'
        )
        self.GFN_DEPLOYER = accounts.add(self.GFN_DEPLOYER_PRIVATE_KEY)
        self.GFN_DEPLOYER_ADDRESS = self.GFN_DEPLOYER.address
        self.TXN_SENDER = {'from': self.GFN_DEPLOYER_ADDRESS}
