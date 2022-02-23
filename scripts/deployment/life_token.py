#!/usr/bin/python3
from scripts.deployment.base import BaseDeployment
from constants import ContractName
from brownie import LIFEToken


class LIFETokenDeployment(BaseDeployment):
    name = ContractName.LIFE_TOKEN

    def _deploy(self):
        registry_contract = self._load_registry_address()
        life_token = LIFEToken.deploy(
            self.setting.GFN_OWNER_ADDRESS,
            registry_contract,
            self.setting.LIFE_TOKEN_NAME,
            self.setting.LIFE_TOKEN_SYMBOL,
            self.setting.TXN_SENDER
        )
        return life_token.address
