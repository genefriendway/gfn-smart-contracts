#!/usr/bin/python3
from scripts.deployment.base import BaseDeployment
from constants import ContractName
from brownie import ContractRegistry


class RegistryDeployment(BaseDeployment):
    name = ContractName.REGISTRY

    def _deploy(self):
        registry = ContractRegistry.deploy(
            self.setting.GFN_OWNER_ADDRESS,
            self.setting.TXN_SENDER
        )
        return registry.address
