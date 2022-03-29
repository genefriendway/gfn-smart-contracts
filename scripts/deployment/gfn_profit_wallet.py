#!/usr/bin/python3
from scripts.deployment.base import ContractDeployment
from constants import ContractName
from brownie import GeneFriendNetworkWallet


class GFNProfitWalletDeployment(ContractDeployment):
    contract_name = ContractName.GFN_PROFIT_WALLET
    contract_class = GeneFriendNetworkWallet

    def validate(self):
        errors = super().validate()
        if not self.setting.GFN_PROFIT_WALLET_OPERATOR_ADDRESS:
            errors.append("Please setup env: 'GFN_PROFIT_WALLET_OPERATOR_ADDRESS'")
        return errors

    def get_owner(self):
        return self.setting.GFN_PROFIT_WALLET_OPERATOR_ADDRESS

    def deploy(self):
        registry_instance = self.get_registry_instance()

        print(f"==> Deploying {self.contract_name} .....")
        gfn_profit_wallet = self.contract_class.deploy(
            registry_instance.address,
            self.setting.TXN_SENDER
        )

        return gfn_profit_wallet
