#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import GNFTToken


class GNFTTokenDeployment(ContractDeployment):
    contract_name = ContractName.GNFT_TOKEN
    contract_class = GNFTToken

    def validate(self):
        errors = super().validate()
        if not self.setting.GNFT_TOKEN_NAME:
            errors.append("Please setup env: 'GNFT_TOKEN_NAME'")
        if not self.setting.GNFT_TOKEN_SYMBOL:
            errors.append("Please setup env: 'GNFT_TOKEN_SYMBOL'")
        return errors

    def get_owner(self):
        return self.setting.GFN_GNFT_OPERATOR_ADDRESS

    def deploy(self):
        registry_instance = self.get_registry_instance()

        print(f"==> Deploying {self.contract_name} .....")
        gnft_token = self.contract_class.deploy(
            registry_instance.address,
            self.setting.GNFT_TOKEN_NAME,
            self.setting.GNFT_TOKEN_SYMBOL,
            self.setting.TXN_SENDER
        )

        return gnft_token
