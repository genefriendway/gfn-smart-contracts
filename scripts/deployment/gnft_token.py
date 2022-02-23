#!/usr/bin/python3
from scripts.deployment.base import BaseDeployment
from constants import ContractName
from brownie import GNFTToken


class GNFTTokenDeployment(BaseDeployment):
    name = ContractName.GNFT_TOKEN

    def _deploy(self):
        registry_contract = self._load_registry_address()
        gnft_token = GNFTToken.deploy(
            self.setting.GFN_OWNER_ADDRESS,
            registry_contract,
            self.setting.GNFT_TOKEN_NAME,
            self.setting.GNFT_TOKEN_SYMBOL,
            self.setting.TXN_SENDER
        )
        return gnft_token.address
