from typing import List

from constants import ContractName
from utils.common import read_json


def load_contract_names() -> List:
    contract_names = []
    for key, value in ContractName.__dict__.items():
        if not key.startswith('__'):
            contract_names.append(value)
    return contract_names


def load_contracts_from_deployment_output(deployment_output_file) -> dict:
    deployment_data = read_json(deployment_output_file)
    contracts = deployment_data.get('contracts', {})
    return contracts


def load_specific_contract_data_from_deployment_output(
        contract_name, deployment_output_file
) -> dict:
    contracts = load_contracts_from_deployment_output(deployment_output_file)
    return contracts[contract_name]
