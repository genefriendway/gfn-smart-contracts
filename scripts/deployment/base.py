#!/usr/bin/python3
from abc import ABC, abstractmethod
from typing import List
from brownie import accounts, Contract

from utils.common import read_json, write_json
from scripts.settings import Setting
from constants import ContractName
from utils.contract import (
    load_specific_contract_data_from_deployment_output
)


def template_of_contract_data(name: str, address: str, owner: str, abi: List):
    return {
        "name": name,
        "address": address,
        "owner": owner,
        "abi": abi
    }


class ContractDeployment(ABC):
    contract_name = None
    contract_class = None

    def __init__(self, setting: Setting):
        self.setting = setting
        self.contract_instance = None
        errors = self.validate()
        if errors:
            raise EnvironmentError('\n'.join(errors))

    def validate(self):
        errors = []
        if not self.setting.ENV_NAME:
            errors.append("Please setup env: 'ENV_NAME'")
        if not self.setting.GFN_DEPLOYER_PRIVATE_KEY:
            errors.append("Please setup env: 'GFN_DEPLOYER_PRIVATE_KEY'")
        if not self.setting.GFN_REGISTRY_OWNER_ADDRESS:
            errors.append("Please setup env: 'GFN_REGISTRY_OWNER_ADDRESS'")
        if not self.setting.GFN_GNFT_OPERATOR_ADDRESS:
            errors.append("Please setup env: 'GFN_GNFT_OPERATOR_ADDRESS'")
        if not self.setting.GFN_NFT_HOLDER_ADDRESS:
            errors.append("Please setup env: 'GFN_NFT_HOLDER_ADDRESS'")
        return errors

    def start_deployment(self):
        instance = self.deploy()
        contract_data = template_of_contract_data(
            name=self.contract_name,
            address=instance.address,
            owner=self.get_owner(),
            abi=instance.abi
        )
        self.contract_instance = instance
        if not self.contract_instance:
            raise ValueError("No contract instance after deployment!")

        self._write_env_settings()
        self._write_contract_section(self.contract_name, contract_data)

        return instance

    @abstractmethod
    def deploy(self):
        raise NotImplementedError

    @abstractmethod
    def get_owner(self):
        raise NotImplementedError

    def publish(self, deployment_output):
        instance = self.get_contract_instance(deployment_output)
        self.contract_class.publish_source(instance)
        return instance

    def _write_env_settings(self):
        deployment_data = self._read_deployment_output(
            _from_file=self.setting.DEPLOYMENT_OUTPUT
        )
        deployment_data.update(self.setting.__dict__)

        # write to deployment output again
        write_json(self.setting.DEPLOYMENT_OUTPUT, deployment_data)

    def _write_contract_section(self, name: str, contract_data: dict):
        deployment_data = self._read_deployment_output(
            _from_file=self.setting.DEPLOYMENT_OUTPUT
        )
        # retrieve and update contract section
        contract_section = deployment_data.get('contracts', {})
        contract_section[name] = contract_data

        # replace by new contract section
        deployment_data['contracts'] = contract_section

        # write to deployment output again
        write_json(self.setting.DEPLOYMENT_OUTPUT, deployment_data)

    def _read_deployment_output(self, _from_file):
        try:
            deployment_data = read_json(_from_file)
        except FileNotFoundError:
            deployment_data = {}

        return deployment_data

    def _load_registry_data_from_file(self, _from_file=None):
        deployment_data = self._read_deployment_output(_from_file)
        contracts = deployment_data.get('contracts', {})
        registry_data = contracts.get(ContractName.REGISTRY, {})

        if not registry_data:
            print(f"[WARNING]: Not found ContractRegistry "
                  f"from file '{_from_file}'")
            msg = "[?] Please select previous deployment output " \
                  "that contain the registry address you want to use: "
            _file = input(msg)
            registry_data = self._load_registry_data_from_file(_file)
            registry_data['from_deployment'] = _file
            self._write_contract_section(ContractName.REGISTRY, registry_data)
            return registry_data
        return registry_data

    def get_registry_instance(self):
        registry_data = self._load_registry_data_from_file(self.setting.DEPLOYMENT_OUTPUT)
        return Contract.from_abi(
            name=registry_data['name'],
            address=registry_data['address'],
            abi=registry_data['abi'],
            owner=accounts.add(self.setting.GFN_DEPLOYER_PRIVATE_KEY)
        )

    def get_contract_instance(self, deployment_output):
        contract_data = load_specific_contract_data_from_deployment_output(
            self.contract_name, deployment_output
        )
        return Contract.from_abi(
            name=contract_data['name'],
            address=contract_data['address'],
            abi=contract_data['abi'],
            owner=accounts.add(self.setting.GFN_DEPLOYER_PRIVATE_KEY)
        )
