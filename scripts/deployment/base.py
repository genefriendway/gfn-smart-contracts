#!/usr/bin/python3
from abc import ABC, abstractmethod
from utils.common import read_json, write_json
from scripts.settings import Setting
from constants import ContractName


def template_output(name: str, address: str, abi: dict):
    return {
        "name": name,
        "address": address,
        "abi": abi
    }


class BaseDeployment(ABC):
    name = None

    def __init__(self, setting: Setting):
        self.setting = setting

    def start(self):
        address = self._deploy()
        output = template_output(
            name=self.name, address=address, abi=self._load_abi()
        )
        self._write_env_settings()
        self._write_contract_section(self.name, output)

    @abstractmethod
    def _deploy(self):
        raise NotImplementedError

    def _write_env_settings(self):
        deployment_data = self._read_deployment_output(
            _from_file=self.setting.DEPLOYMENT_OUTPUT
        )

        deployment_data['datetime'] = self.setting.DEPLOYMENT_DATETIME
        deployment_data['env'] = self.setting.ENV_NAME
        deployment_data['network'] = self.setting.BLOCKCHAIN_NETWORK
        deployment_data['gfn_deployer'] = self.setting.GFN_DEPLOYER_ADDRESS
        deployment_data['gfn_owner'] = self.setting.GFN_OWNER_ADDRESS

    def _write_contract_section(self, name: str, output: dict):
        deployment_data = self._read_deployment_output(
            _from_file=self.setting.DEPLOYMENT_OUTPUT
        )
        # retrieve and update contract section
        contract_section = deployment_data.get('contracts', {})
        contract_section[name] = output

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

    def _load_registry(self, _from_file=None):
        deployment_data = self._read_deployment_output(_from_file)
        contracts = deployment_data.get('contracts', {})
        registry_data = contracts.get(ContractName.REGISTRY, {})

        if not registry_data:
            print(f"[WARNING]: Not found ContractRegistry "
                  f"from file '{_from_file}'")
            msg = "[?] Please select previous deployment output " \
                  "that contain the registry address you want to use: "
            _file = input(msg)
            registry_data = self._load_registry(_file)
            registry_data['from_deployment'] = _file
            self._write_contract_section(ContractName.REGISTRY, registry_data)
            return registry_data
        return registry_data

    def _load_registry_address(self):
        address = self._load_registry(self.setting.DEPLOYMENT_OUTPUT).get('address')
        if not address:
            raise Exception("ContractRegistry has no address")
        return address

    def _load_abi(self):
        return {}
