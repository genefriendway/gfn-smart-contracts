#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import Configuration
from .mixins.transfer_ownership import TransferOwnershipMixin


class ConfigurationDeployment(ContractDeployment, TransferOwnershipMixin):
    contract_name = ContractName.CONFIGURATION
    contract_class = Configuration

    def validate(self):
        errors = super().validate()
        if not self.setting.GFN_CONFIGURATION_OWNER_ADDRESS:
            errors.append(
                "Please setup env: 'GFN_CONFIGURATION_OWNER_ADDRESS'")
        return errors

    def get_owner(self):
        return self.setting.GFN_CONFIGURATION_OWNER_ADDRESS

    def deploy(self):
        registry_instance = self.get_registry_instance()

        print(f"==> Deploying {self.contract_name} .....")
        configuration = self.contract_class.deploy(
            self.setting.GFN_DEPLOYER_ADDRESS,
            self.setting.GFN_NFT_HOLDER_ADDRESS,
            registry_instance.address,
            self.setting.TXN_SENDER
        )

        return configuration

    def transfer_contract_owner(self):
        print(f'==> Transferring Owner of {self.contract_name} '
              f'to {self.get_owner()}')
        self.contract_instance.transferOwnership(
            self.get_owner(),
            self.setting.TXN_SENDER
        )