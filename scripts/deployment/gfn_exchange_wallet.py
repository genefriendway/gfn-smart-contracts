#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import GeneFriendNetworkWallet


class GFNExchangeWalletDeployment(ContractDeployment):
    contract_name = ContractName.GFN_EXCHANGE_WALLET
    contract_class = GeneFriendNetworkWallet

    def validate(self):
        errors = super().validate()
        if not self.setting.GFN_EXCHANGE_WALLET_OPERATOR_ADDRESS:
            errors.append("Please setup env: 'GFN_EXCHANGE_WALLET_OPERATOR_ADDRESS'")
        return errors

    def get_owner(self):
        return self.setting.GFN_EXCHANGE_WALLET_OPERATOR_ADDRESS

    def deploy(self):
        registry_instance = self.get_registry_instance()

        print(f"==> Deploying {self.contract_name} .....")
        gfn_exchange_wallet = self.contract_class.deploy(
            registry_instance.address,
            self.setting.TXN_SENDER
        )

        return gfn_exchange_wallet
