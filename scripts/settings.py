#!/usr/bin/python3
from utils.datetime import DateTimeUtil
from brownie import accounts, network


OUTPUT_FILE = "deployment_{env}_{time}.json"


class Setting:

    def __init__(self, env_settings: dict):
        now = DateTimeUtil.now()

        self.ENV_NAME = env_settings['ENV_NAME']
        self.ENV_MENU = env_settings['ENV_MENU']
        self.DEPLOYMENT_MENU = env_settings['DEPLOYMENT_MENU']
        self.BLOCKCHAIN_NETWORK = network.show_active()
        self.GFN_DEPLOYER_PRIVATE_KEY = env_settings['GFN_DEPLOYER_PRIVATE_KEY']
        self.GFN_OWNER_ADDRESS = env_settings['GFN_OWNER_ADDRESS']
        self.GNFT_TOKEN_NAME = env_settings['GNFT_TOKEN_NAME']
        self.GNFT_TOKEN_SYMBOL = env_settings['GNFT_TOKEN_SYMBOL']
        self.LIFE_TOKEN_NAME = env_settings['LIFE_TOKEN_NAME']
        self.LIFE_TOKEN_SYMBOL = env_settings['LIFE_TOKEN_SYMBOL']

        # validate settings
        errors = []
        if not self.ENV_NAME:
            errors.append("Please setup env: 'ENV_NAME'")
        if not self.ENV_MENU:
            errors.append("Please no setting: 'ENV_MENU'")
        if not self.DEPLOYMENT_MENU:
            errors.append("Please no setting: 'DEPLOYMENT_MENU'")
        if not self.GFN_DEPLOYER_PRIVATE_KEY:
            errors.append("Please setup env: 'GFN_DEPLOYER_PRIVATE_KEY'")
        if not self.GFN_OWNER_ADDRESS:
            errors.append("Please setup env: 'GFN_OWNER_ADDRESS'")

        if errors:
            raise EnvironmentError('\n'.join(errors))

        self.DEPLOYMENT_OUTPUT = OUTPUT_FILE.format(
            env=self.ENV_NAME.lower(),
            time=DateTimeUtil.date_to_text(now, '%Y_%m_%d_%H_%M_%S')
        )
        self.DEPLOYMENT_DATETIME = DateTimeUtil.date_to_text(
            now, fmt='%d/%m/%Y %H:%M:%S'
        )
        self.GFN_DEPLOYER = accounts.add(self.GFN_DEPLOYER_PRIVATE_KEY)
        self.GFN_DEPLOYER_ADDRESS = self.GFN_DEPLOYER.address
        self.TXN_SENDER = {'from': self.GFN_DEPLOYER_ADDRESS}
