#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import GNFTToken


class GNFTTokenDeployment(ContractDeployment):
    contract_name = ContractName.GNFT_TOKEN
    contract_class = GNFTToken

    def deploy(self):
        registry_instance = self.get_registry_instance()

        print(f"==> Deploying {self.contract_name} .....")
        gnft_token = self.contract_class.deploy(
            self.setting.GFN_OWNER_ADDRESS,
            registry_instance.address,
            self.setting.GNFT_TOKEN_NAME,
            self.setting.GNFT_TOKEN_SYMBOL,
            self.setting.TXN_SENDER
        )

        print(f"==> Registering {self.contract_name} .....")
        registry_instance.registerContract(
            self.contract_name, gnft_token.address, self.setting.TXN_SENDER
        )
        return gnft_token
