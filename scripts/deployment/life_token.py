#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import LIFEToken


class LIFETokenDeployment(ContractDeployment):
    name = ContractName.LIFE_TOKEN

    def _deploy(self):
        registry_instance = self.get_registry_instance()

        print(f"==> Deploying {self.name} .....")
        life_token = LIFEToken.deploy(
            self.setting.GFN_OWNER_ADDRESS,
            registry_instance.address,
            self.setting.LIFE_TOKEN_NAME,
            self.setting.LIFE_TOKEN_SYMBOL,
            self.setting.TXN_SENDER
        )

        print(f"==> Registering {self.name} .....")
        registry_instance.registerContract(
            self.name, life_token.address, self.setting.TXN_SENDER
        )
        return life_token
