#!/usr/bin/python3
import os
from copy import copy
from dotenv import load_dotenv

from scripts.settings import Setting
from scripts.deployment.registry import RegistryDeployment
from scripts.deployment.configuration import ConfigurationDeployment
from scripts.deployment.gnft_token import GNFTTokenDeployment
from scripts.deployment.life_token import LIFETokenDeployment

ENV_LOCAL = 1
ENV_NIGHTLY = 2
ENV_PRODUCTION = 3

REGISTRY = 1
CONFIGURATION = 2
GNFT_TOKEN = 3
LIFE_TOKEN = 4

ENV_MENU = {
    ENV_LOCAL: '.env.local',
    ENV_NIGHTLY: '.env.nightly',
    ENV_PRODUCTION: '.env.production',
}

DEPLOYMENT_MENU = {
    REGISTRY: RegistryDeployment,
    CONFIGURATION: ConfigurationDeployment,
    GNFT_TOKEN: GNFTTokenDeployment,
    LIFE_TOKEN: LIFETokenDeployment,
}


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
    menu_list = [f"=> {index}. {deployment_cls.name}" for index, deployment_cls in DEPLOYMENT_MENU.items()]
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
        f"{item}. {DEPLOYMENT_MENU[int(item)].name}" for item in selection
    ]
    print(f"[==>] You selected contract deployments in the following order: "
          f"{' -> '.join(selection_info)}")
    print("===================================================================")
    print("\n")

    contract_deployments = [DEPLOYMENT_MENU[int(item)] for item in selection]
    return contract_deployments


def load_settings(env_file):
    load_dotenv(env_file)
    env = copy(dict(os.environ))
    env['ENV_MENU'] = ENV_MENU
    env['DEPLOYMENT_MENU'] = DEPLOYMENT_MENU
    return Setting(env)


def run_deployment_tests(setting: Setting):
    pass


def main():
    # show menu
    selected_env = display_env_menu()
    selected_contract_deployments = display_deployment_menu()
    # load env settings
    setting = load_settings(selected_env)

    print(f"=============== Settings for {setting.ENV_NAME} ==================")
    print(f'=> ENV         : {setting.ENV_NAME}')
    print(f'=> Network     : {setting.BLOCKCHAIN_NETWORK}')
    print(f'=> gfn_deployer: {setting.GFN_DEPLOYER_ADDRESS}')
    print(f'=> gfn_owner   : {setting.GFN_OWNER_ADDRESS}')
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

    # initialize Deployment object
    for deployment_class in selected_contract_deployments:
        deployment = deployment_class(setting)
        print(f"================ Deployment: {deployment.name} =================")
        deployment.start()

    if selected_env in [ENV_MENU[ENV_LOCAL], ENV_MENU[ENV_NIGHTLY]]:
        print("================ Running Deployment Tests ===================")
        run_deployment_tests(setting)
