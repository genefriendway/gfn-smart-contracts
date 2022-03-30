#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import ContractRegistry
from .mixins.transfer_ownership import TransferOwnershipMixin


class RegistryDeployment(ContractDeployment, TransferOwnershipMixin):
    contract_name = ContractName.REGISTRY
    contract_class = ContractRegistry

    def validate(self):
        errors = super().validate()
        if not self.setting.GFN_REGISTRY_OWNER_ADDRESS:
            errors.append(
                "Please setup env: 'GFN_REGISTRY_OWNER_ADDRESS'")
        return errors

    def get_owner(self):
        return self.setting.GFN_REGISTRY_OWNER_ADDRESS

    def deploy(self):
        print(f"==> Deploying {self.contract_name} .....")
        registry = self.contract_class.deploy(
            self.setting.GFN_DEPLOYER_ADDRESS,
            self.setting.TXN_SENDER
        )
        return registry
