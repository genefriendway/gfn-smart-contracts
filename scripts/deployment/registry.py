#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import ContractRegistry


class RegistryDeployment(ContractDeployment):
    contract_name = ContractName.REGISTRY
    contract_class = ContractRegistry

    def deploy(self):
        print(f"==> Deploying {self.contract_name} .....")
        registry = self.contract_class.deploy(
            self.setting.GFN_DEPLOYER_ADDRESS,
            self.setting.TXN_SENDER
        )
        return registry
