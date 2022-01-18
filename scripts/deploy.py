#!/usr/bin/python3
import os
from dotenv import load_dotenv
from brownie import (
    network,
    accounts,
    ContractRegistry,
    GNFTToken,
    LIFEToken,
    LIFETreasury,
)
from constants import ContractName

# load environment variables from .env.
load_dotenv()

GFN_DEPLOYER_PRIVATE_KEY = os.getenv('GFN_DEPLOYER_PRIVATE_KEY')
GFN_OWNER_ADDRESS = os.getenv('GFN_OWNER_ADDRESS')
GFN_FOUNDER_ADDRESS_ONE = os.getenv('GFN_FOUNDER_ADDRESS_ONE')
GFN_FOUNDER_ADDRESS_TWO = os.getenv('GFN_FOUNDER_ADDRESS_TWO')
GFN_FOUNDER_ADDRESS_THREE = os.getenv('GFN_FOUNDER_ADDRESS_THREE')

# ========== always validate environment before deploy =======
errors = []
if not GFN_DEPLOYER_PRIVATE_KEY:
    errors.append("Please setup env: 'GFN_DEPLOYER_PRIVATE_KEY'")
if not GFN_OWNER_ADDRESS:
    errors.append("Please setup env: 'GFN_OWNER_ADDRESS'")
if not GFN_FOUNDER_ADDRESS_ONE:
    errors.append("Please setup env: 'GFN_FOUNDER_ADDRESS_ONE'")
if not GFN_FOUNDER_ADDRESS_TWO:
    errors.append("Please setup env: 'GFN_FOUNDER_ADDRESS_TWO'")
if not GFN_FOUNDER_ADDRESS_THREE:
    errors.append("Please setup env: 'GFN_FOUNDER_ADDRESS_THREE'")

if errors:
    raise EnvironmentError('\n'.join(errors))

# Load accounts from private keys
gfn_deployer = accounts.add(GFN_DEPLOYER_PRIVATE_KEY)
gfn_deployer_info = {'from': gfn_deployer}

print("===================== DEPLOYMENT INFORMATION =========================")
print(f'=> Network: {network.show_active()}')
print(f'=> gfn_deployer: {gfn_deployer}')
print(f'=> gfn_owner: {GFN_OWNER_ADDRESS}')
print(f'=> GFN_FOUNDER_ADDRESS_ONE: {GFN_FOUNDER_ADDRESS_ONE}')
print(f'=> GFN_FOUNDER_ADDRESS_TWO: {GFN_FOUNDER_ADDRESS_TWO}')
print(f'=> GFN_FOUNDER_ADDRESS_THREE: {GFN_FOUNDER_ADDRESS_THREE}')
print("======================================================================")
while True:
    confirmation = input("[?] Please confirm above information? [yes|no] ")
    if confirmation.lower().strip() == 'yes':
        print("=> You selected 'yes' to continue deployment.")
        break
    elif confirmation.lower().strip() == 'no':
        print("====> You selected 'no' to stop deployment.")
        exit(0)
    else:
        pass


# ======= function deploy smart contracts =======
def deploy_contract_registry():
    print("================== [Deploying ContractRegistry] ==================")
    return ContractRegistry.deploy(gfn_deployer, gfn_deployer_info)


def deploy_gnft_token(registry):
    print("================== [Deploying GNFTToken] ==================")
    gnft_token = GNFTToken.deploy(
        GFN_OWNER_ADDRESS,
        registry,
        "Gene Friend Network G-NFT Token",
        "GNFT",
        gfn_deployer_info
    )

    print("====> [Registering GNFTToken contract]")
    registry.registerContract(
        ContractName.GNFT_TOKEN, gnft_token.address, gfn_deployer_info
    )
    return gnft_token


def deploy_life_token(registry):
    print("================== [Deploying LIFEToken] ==================")
    life_token = LIFEToken.deploy(
        GFN_OWNER_ADDRESS,
        registry,
        "Gene Friend Network LIFE Token",
        "LIFE",
        gfn_deployer_info
    )
    print("====> [Registering LIFEToken contract]")
    registry.registerContract(
        ContractName.LIFE_TOKEN, life_token.address, gfn_deployer_info
    )
    return life_token


def deploy_life_treasury(registry):
    print("================== [Deploying LIFETreasury] ==================")
    life_treasury = LIFETreasury.deploy(
        [GFN_FOUNDER_ADDRESS_ONE, GFN_FOUNDER_ADDRESS_TWO, GFN_FOUNDER_ADDRESS_THREE],
        3,
        gfn_deployer_info
    )
    print("====> [Registering LIFETreasury contract]")
    registry.registerContract(
        ContractName.LIFE_TREASURY, life_treasury.address, gfn_deployer_info
    )
    return life_treasury


def main():
    registry = deploy_contract_registry()
    gnft_token = deploy_gnft_token(registry)
    life_token = deploy_life_token(registry)
    life_treasury = deploy_life_treasury(registry)

    print("========= RESULTS ==============")
    print(f'=> Network: {network.show_active()}')
    print(f'=> gfn_deployer: {gfn_deployer}')
    print(f'=> gfn_owner: {GFN_OWNER_ADDRESS}')
    print(f"=> ContractRegistry Address: {registry.address}")
    print(f"=> GNFTToken Address: {gnft_token.address}")
    print(f"=> LIFEToken Address: {life_token.address}")
    print(f"=> LIFETreasury Address: {life_treasury.address}")
    print("================================")
