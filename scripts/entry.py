#!/usr/bin/python3
import os
from copy import copy
from dotenv import load_dotenv

from constants.common import ContractName
from scripts.settings import Setting
from scripts.verify import verify_deployment
from scripts.deployment.registry import RegistryDeployment
from scripts.deployment.configuration import ConfigurationDeployment
from scripts.deployment.gnft_token import GNFTTokenDeployment
from scripts.deployment.life_token import LIFETokenDeployment

ENV_LOCAL = 1
ENV_NIGHTLY = 2
ENV_PRODUCTION = 3


ENV_MENU = {
    ENV_LOCAL: '.env.local',
    ENV_NIGHTLY: '.env.nightly',
    ENV_PRODUCTION: '.env.production',
}

REGISTRY = 1
CONFIGURATION = 2
GNFT_TOKEN = 3
LIFE_TOKEN = 4
LIFE_TREASURY = 5

DEPLOYMENT_MENU = {
    REGISTRY: RegistryDeployment,
    CONFIGURATION: ConfigurationDeployment,
    GNFT_TOKEN: GNFTTokenDeployment,
    LIFE_TOKEN: LIFETokenDeployment,
}

PUBLISH_MENU = DEPLOYMENT_MENU

DEPLOY_ACTION = 1
PUBLISH_ACTION = 2
MAIN_MENU = {
    DEPLOY_ACTION: "Deploy Contract",
    PUBLISH_ACTION: "Publish Contract",
}


def validate_main_action_selection(selection):
    selection = int(selection)
    valid_selections = [key for key, _ in MAIN_MENU.items()]
    if selection not in valid_selections:
        return None, False
    return selection, True


def validate_env_selection(selection):
    selection = int(selection)
    valid_selections = [key for key, _ in ENV_MENU.items()]
    if selection not in valid_selections:
        return None, False
    return selection, True


def validate_deployment_selection(selection):
    selection_str = selection.replace(' ', '')
    selection_list = selection_str.split(',')
    selection_list = [int(item) for item in selection_list if item]
    valid_selections = [key for key, _ in DEPLOYMENT_MENU.items()]

    for item in selection_list:
        if item not in valid_selections:
            return None, False
    return selection_list, True


def display_main_menu():
    menu_list = [f"=> {index}. {env}" for index, env in MAIN_MENU.items()]
    menu_string = '\n'.join(menu_list)
    print("======================= MAIN ACTION MENU =========================")
    print(menu_string)

    selection = input("[???] Select Main Action (Select One): ")
    # validate
    selection, is_valid = validate_main_action_selection(selection)
    if not is_valid:
        print("[***] [WARNING]: Your selection is invalid. Please select again!")
        return display_main_menu()

    # print the selection
    print(f"[==>] You selected Main Action: {MAIN_MENU[selection]}")
    print("===================================================================")
    print("\n")
    return selection


def display_env_menu():
    menu_list = [f"=> {index}. {env}" for index, env in ENV_MENU.items()]
    menu_string = '\n'.join(menu_list)
    print("=========================== ENV MENU ==============================")
    print(menu_string)

    selection = input("[???] Select Environment to deploy (Select One): ")
    # validate
    selection, is_valid = validate_env_selection(selection)
    if not is_valid:
        print("[***] [WARNING]: Your selection is invalid. Please select again!")
        return display_env_menu()

    # print the selection
    print(f"[==>] You selected ENV: {ENV_MENU[selection]}")
    print("===================================================================")
    print("\n")
    return ENV_MENU[selection]


def display_deployment_menu():
    menu_list = [
        f"=> {index}. {deployment_cls.contract_name}"
        for index, deployment_cls in DEPLOYMENT_MENU.items()
    ]
    menu_string = '\n'.join(menu_list)
    print("=========================== Deployment Menu =======================")
    print(menu_string)

    selection = input("[???] Select contracts you want to deploy"
                      "(Multiple selection separated by comma): ")
    # validate
    selection, is_valid = validate_deployment_selection(selection)
    if not is_valid:
        print("[***] [WARNING]: Your selection is invalid. Please select again!")
        return display_deployment_menu()

    selection_info = [
        f"{item}. {DEPLOYMENT_MENU[int(item)].contract_name}" for item in selection
    ]
    print(f"[==>] You selected contract deployments in the following order: "
          f"{' -> '.join(selection_info)}")
    print("===================================================================")
    print("\n")

    contract_deployments = [DEPLOYMENT_MENU[int(item)] for item in selection]
    return contract_deployments


def select_deployment_output():
    msg = "[?] Please select deployment output that you want to use: "
    return input(msg)


def display_publish_menu():
    menu_list = [
        f"=> {index}. {deployment_cls.contract_name}"
        for index, deployment_cls in PUBLISH_MENU.items()
    ]
    menu_string = '\n'.join(menu_list)
    print("=========================== Publish Menu =======================")
    print(menu_string)

    selection = input("[???] Select contracts you want to publish"
                      "(Multiple selection separated by comma): ")
    # validate
    selection, is_valid = validate_deployment_selection(selection)
    if not is_valid:
        print("[***] [WARNING]: Your selection is invalid. Please select again!")
        return display_publish_menu()

    selection_info = [
        f"{item}. {PUBLISH_MENU[int(item)].contract_name}"
        for item in selection
    ]
    print(f"[==>] You selected contracts to publish: "
          f"{' -> '.join(selection_info)}")
    print("===================================================================")
    print("\n")

    contract_deployments = [PUBLISH_MENU[int(item)] for item in selection]
    return contract_deployments


def load_settings(env_file):
    load_dotenv(env_file)
    env = copy(dict(os.environ))
    env['ENV_MENU'] = ENV_MENU
    env['DEPLOYMENT_MENU'] = DEPLOYMENT_MENU
    return Setting(env)


def main():
    main_action = display_main_menu()
    selected_env = display_env_menu()
    setting = load_settings(selected_env)

    print(f"=============== Settings for {setting.ENV_NAME} ==================")
    print(f'=> ENV         : {setting.ENV_NAME}')
    print(f'=> Network     : {setting.BLOCKCHAIN_NETWORK}')
    print('----------------------------------------------------------')
    print(f'=> GFN Deployer             : {setting.GFN_DEPLOYER_ADDRESS}')
    print(f'=> GFN Registry Owner       : {setting.GFN_REGISTRY_OWNER_ADDRESS}')
    print(f'=> GFN Configuration Owner  : {setting.GFN_CONFIGURATION_OWNER_ADDRESS}')
    print(f'=> GFN GNFTToken Operator   : {setting.GFN_GNFT_OPERATOR_ADDRESS}')
    print(f'=> GFN NFT Holder           : {setting.GFN_NFT_HOLDER_ADDRESS}')
    print(f'=> LIFE_TREASURY_ADDRESS    : {setting.LIFE_TREASURY_ADDRESS}')
    print('----------------------------------------------------------')
    print(f'=> NFT Token Name       : {setting.GNFT_TOKEN_NAME}')
    print(f'=> NFT Token SymBol     : {setting.GNFT_TOKEN_SYMBOL}')
    print(f'=> LIFE Token Name      : {setting.LIFE_TOKEN_NAME}')
    print(f'=> LIFE Token SymBol    : {setting.LIFE_TOKEN_SYMBOL}')
    print("===============================================================")
    while True:
        confirmation = input("[?] Please confirm above information before "
                             "staring deployment? [yes|no] ")
        if confirmation.lower().strip() == 'yes':
            print("=> You selected 'yes' to continue deployment.")
            break
        elif confirmation.lower().strip() == 'no':
            print("====> You selected 'no' to stop deployment.")
            exit(0)
        else:
            pass
    print("\n")

    if main_action == DEPLOY_ACTION:
        contract_instances = {}
        deployments = []
        selected_contract_deployments = display_deployment_menu()
        # initialize Deployment object
        for deployment_class in selected_contract_deployments:
            print(f"================ Deployment: {deployment_class.contract_name} =================")
            try:
                deployment = deployment_class(setting)
                contract_instance = deployment.start_deployment()
                contract_instances[deployment.contract_name] = contract_instance
                deployments.append(deployment)
            except Exception as ex:
                print("===== [ERROR] =======")
                print(str(ex))
                print("===== [ERROR] =======")
                while True:
                    confirmation = input(
                        "[?] Do you want to continue depoly? [yes|no] ")
                    if confirmation.lower().strip() == 'yes':
                        print("=> You selected 'yes' to continue deployment.")
                        break
                    elif confirmation.lower().strip() == 'no':
                        print("====> You selected 'no' to stop deployment.")
                        exit(0)
                    else:
                        pass
        print("================ Register Contract Operator ===================")
        configuration = contract_instances[ContractName.CONFIGURATION]
        for contract_name, operator in setting.CONTRACT_OPERATORS.items():
            print(f"--------- {contract_name} -----------")
            contract_instance = contract_instances[contract_name]
            configuration.setOperator(
                contract_instance.address,
                operator,
                setting.TXN_SENDER
            )

        print("================ Transferring Contract Owner ===================")
        for deployment in deployments:
            deployment.transfer_contract_owner()

        # if selected_env in [ENV_MENU[ENV_LOCAL], ENV_MENU[ENV_NIGHTLY]]:
        print("================ Verifying Deployment ===================")
        verify_deployment(setting, contract_instances)

    elif main_action == PUBLISH_ACTION:
        deployment_output = select_deployment_output()
        selected_contract_deployments = display_publish_menu()
        for deployment_class in selected_contract_deployments:
            deployment = deployment_class(setting)
            print(f"================ Publishing: {deployment.contract_name} =================")
            deployment.publish(deployment_output)
    else:
        raise Exception("Invalid Selected Main Action")
