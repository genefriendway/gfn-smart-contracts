#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import MultiSignature


class LIFETreasuryDeployment(ContractDeployment):
    contract_name = ContractName.LIFE_TREASURY
    contract_class = MultiSignature

    def validate(self):
        errors = super().validate()
        if not self.setting.GFN_FOUNDER_ADDRESS_ONE:
            errors.append("Please setup env: 'GFN_FOUNDER_ADDRESS_ONE'")
        if not self.setting.GFN_FOUNDER_ADDRESS_TWO:
            errors.append("Please setup env: 'GFN_FOUNDER_ADDRESS_TWO'")
        if not self.setting.GFN_FOUNDER_ADDRESS_THREE:
            errors.append("Please setup env: 'GFN_FOUNDER_ADDRESS_THREE'")
        return errors

    def get_owner(self):
        """LIFEToken contract has no operator"""
        pass

    def deploy(self):
        registry_instance = self.get_registry_instance()

        print(f"==> Deploying {self.contract_name} .....")
        life_treasury = self.contract_class.deploy(
            [self.setting.GFN_FOUNDER_ADDRESS_ONE,
             self.setting.GFN_FOUNDER_ADDRESS_TWO,
             self.setting.GFN_FOUNDER_ADDRESS_THREE],
            3,
            self.setting.TXN_SENDER
        )

        print(f"==> Registering {self.contract_name} .....")
        registry_instance.registerContract(
            self.contract_name, life_treasury.address, self.setting.TXN_SENDER
        )
        return life_treasury
