#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import Configuration


class ConfigurationDeployment(ContractDeployment):
    name = ContractName.CONFIGURATION

    def _deploy(self):
        registry_instance = self.get_registry_instance()

        print(f"==> Deploying {self.name} .....")
        configuration = Configuration.deploy(
            self.setting.GFN_OWNER_ADDRESS,
            registry_instance.address,
            self.setting.TXN_SENDER
        )
        print(f"==> Registering {self.name} .....")
        registry_instance.registerContract(
            self.name, configuration.address, self.setting.TXN_SENDER
        )

        return configuration
