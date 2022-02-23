#!/usr/bin/python3
from scripts.deployment.base import BaseDeployment
from constants import ContractName
from brownie import Configuration


class ConfigurationDeployment(BaseDeployment):
    name = ContractName.CONFIGURATION

    def _deploy(self):
        registry_contract = self._load_registry_address()
        configuration = Configuration.deploy(
            self.setting.GFN_OWNER_ADDRESS,
            registry_contract,
            self.setting.TXN_SENDER
        )
        return configuration.address
