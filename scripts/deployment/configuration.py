#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import Configuration


class ConfigurationDeployment(ContractDeployment):
    contract_name = ContractName.CONFIGURATION
    contract_class = Configuration

    def deploy(self):
        registry_instance = self.get_registry_instance()

        print(f"==> Deploying {self.contract_name} .....")
        configuration = self.contract_class.deploy(
            self.setting.GFN_OWNER_ADDRESS,
            registry_instance.address,
            self.setting.TXN_SENDER
        )
        print(f"==> Registering {self.contract_name} .....")
        registry_instance.registerContract(
            self.contract_name, configuration.address, self.setting.TXN_SENDER
        )

        return configuration
