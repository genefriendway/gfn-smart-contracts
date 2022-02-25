from utils.common import read_json


def load_contracts_from_deployment_output(deployment_output_file):
    deployment_data = read_json(deployment_output_file)
    contracts = deployment_data.get('contracts', {})
    return contracts


def load_specific_contract_data_from_deployment_output(
        contract_name, deployment_output_file
):
    contracts = load_contracts_from_deployment_output(deployment_output_file)
    return contracts[contract_name]
