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

    def transfer_contract_owner(self):
        print(f'==> Transferring Owner of {self.contract_name} '
              f'to {self.setting.GFN_REGISTRY_OWNER_ADDRESS}')
        self.contract_instance.transferOwnership(
            self.setting.GFN_REGISTRY_OWNER_ADDRESS,
            self.setting.TXN_SENDER
        )
