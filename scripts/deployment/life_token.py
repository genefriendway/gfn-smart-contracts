#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import LIFEToken


class LIFETokenDeployment(ContractDeployment):
    contract_name = ContractName.LIFE_TOKEN
    contract_class = LIFEToken

    def validate_setting(self):
        errors = super().validate_setting()
        if not self.setting.LIFE_TOKEN_NAME:
            errors.append("Please setup env: 'LIFE_TOKEN_NAME'")
        if not self.setting.LIFE_TOKEN_SYMBOL:
            errors.append("Please setup env: 'LIFE_TOKEN_SYMBOL'")
        return errors

    def deploy(self):
        registry_instance = self.get_registry_instance()

        print(f"==> Deploying {self.contract_name} .....")
        life_token = self.contract_class.deploy(
            registry_instance.address,
            self.setting.LIFE_TOKEN_NAME,
            self.setting.LIFE_TOKEN_SYMBOL,
            self.setting.TXN_SENDER
        )

        print(f"==> Registering {self.contract_name} .....")
        registry_instance.registerContract(
            self.contract_name, life_token.address, self.setting.TXN_SENDER
        )
        return life_token
