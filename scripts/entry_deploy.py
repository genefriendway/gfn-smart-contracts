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

ALL = 0
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
    return int(selection)


def validate_deployment_selection(selection):
    selection = selection.replace(' ', '')
    return selection.split(',')


def display_env_menu():
    menu_list = [f"=> {index}. {env}" for index, env in ENV_MENU.items()]
    menu_string = '\n'.join(menu_list)
    print("=========================== ENV MENU ==============================")
    print(menu_string)

    selection = input("[?] Select Environment to deploy (Select One): ")
    # validate
    selection = validate_env_selection(selection)
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

    selection = input("[?] Select contracts you want to deploy"
                      "(Multiple selection separated by comma): ")
    # validate
    selection = validate_deployment_selection(selection)
    # print(f"[==>] You selected deployment: {DEPLOYMENT_MENU[selection[0]]}")
    print("===================================================================")
    print("\n")
    return [DEPLOYMENT_MENU[int(item)] for item in selection]


def load_settings(env_file):
    load_dotenv(env_file)
    env = copy(dict(os.environ))
    env['ENV_MENU'] = ENV_MENU
    env['DEPLOYMENT_MENU'] = DEPLOYMENT_MENU
    return Setting(env)


def main():
    # show menu
    selected_env = display_env_menu()
    selected_deployments = display_deployment_menu()
    # load env settings
    setting = load_settings(selected_env)

    # initialize Deployment object
    for deployment_class in selected_deployments:
        deployment = deployment_class(setting)
        print(f"================ Deployment: {deployment.name} ================= ")
        deployment.start()
