#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import ContractRegistry


class RegistryDeployment(ContractDeployment):
    name = ContractName.REGISTRY

    def _deploy(self):
        print(f"==> Deploying {self.name} .....")
        registry = ContractRegistry.deploy(
            self.setting.GFN_DEPLOYER_ADDRESS,
            self.setting.TXN_SENDER
        )
        return registry
