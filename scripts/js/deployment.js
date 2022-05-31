const hre = require("hardhat");
const fs = require('fs');
const lib = require('./lib.js');

const print = console.log


async function _updateDeploymentOutput(contractName, contractAddress, contractOwner, artifactFile) {
    // load current data of deployment file
    const deploymentOutput = await lib.readFromJSON(process.env.DEPLOYMENT_OUTPUT_FILE);
    // load artifacts of the contract
    const artifacts = await lib.readFromJSON(artifactFile);

    // build deployment data of the contract
    const deploymentData = {
        name: contractName,
        address: contractAddress,
        owner: contractOwner,
        abi: artifacts['abi'],

    }
    // add deployed contracts
    const contracts = deploymentOutput.contracts;
    contracts[contractName] = deploymentData;

    // set contracts data back to deployment ouput
    deploymentOutput.contracts = contracts;

    await lib.writeToJSON(deploymentOutput, process.env.DEPLOYMENT_OUTPUT_FILE)
}

async function _getRegistryAddress() {
    const deploymentOutput = await lib.readFromJSON(process.env.DEPLOYMENT_OUTPUT_FILE);
    return deploymentOutput.contracts.ContractRegistry.address
}

async function deployContractRegistry() {
    const CONTRACT_NAME = 'ContractRegistry'
    const CONTRACT_CLASS = 'ContractRegistry'
    const ARTIFACT_FILE = 'artifacts/contracts/ContractRegistry.sol/ContractRegistry.json'

    // log to screen
    print(`Starting Deploy Contract ${CONTRACT_NAME}`);

    // start deploy contract to blockchain network
    const Contract = await hre.ethers.getContractFactory(CONTRACT_CLASS);
    const instance = await Contract.deploy(
        process.env.GFN_REGISTRY_OWNER_ADDRESS
    );
    await instance.deployed();
    // log to screen
    print(`Contract ${CONTRACT_NAME} deployed at: ${instance.address}`);
    print('------------------------------------------');

    // update updateDeploymentOutput
    await _updateDeploymentOutput(
        CONTRACT_NAME,
        instance.address,
        process.env.GFN_REGISTRY_OWNER_ADDRESS,
        ARTIFACT_FILE
    )
}

async function deployConfiguration() {
    const CONTRACT_NAME = 'Configuration'
    const CONTRACT_CLASS = 'Configuration'
    const ARTIFACT_FILE = 'artifacts/contracts/Configuration.sol/Configuration.json'
    const registryAddress = await _getRegistryAddress();

    // log to screen
    print(`Starting Deploy Contract ${CONTRACT_NAME}`);

    // start deploy contract to blockchain network
    const Contract = await hre.ethers.getContractFactory(CONTRACT_CLASS);
    const instance = await Contract.deploy(
        process.env.GFN_CONFIGURATION_OWNER_ADDRESS,
        process.env.GFN_NFT_HOLDER_ADDRESS,
        registryAddress,
    );
    await instance.deployed();
    // log to screen
    print(`Contract ${CONTRACT_NAME} deployed at: ${instance.address}`);
    print('------------------------------------------');

    // update updateDeploymentOutput
    await _updateDeploymentOutput(
        CONTRACT_NAME,
        instance.address,
        process.env.GFN_CONFIGURATION_OWNER_ADDRESS,
        ARTIFACT_FILE
    )
}

async function deployGeneNFTToken() {
    const CONTRACT_NAME = 'GNFTToken'
    const CONTRACT_CLASS = 'GNFTToken'
    const ARTIFACT_FILE = 'artifacts/contracts/GNFTToken.sol/GNFTToken.json'
    const registryAddress = await _getRegistryAddress();

    // log to screen
    print(`Starting Deploy Contract ${CONTRACT_NAME}`);

    // start deploy contract to blockchain network
    const Contract = await hre.ethers.getContractFactory(CONTRACT_CLASS);
    const instance = await Contract.deploy(
        registryAddress,
        process.env.GNFT_TOKEN_NAME,
        process.env.GNFT_TOKEN_SYMBOL,
    );
    await instance.deployed();
    // log to screen
    print(`Contract ${CONTRACT_NAME} deployed at: ${instance.address}`);
    print('------------------------------------------');

    // update updateDeploymentOutput
    await _updateDeploymentOutput(
        CONTRACT_NAME,
        instance.address,
        '',
        ARTIFACT_FILE
    )
}


async function deployLIFEToken() {
    const CONTRACT_NAME = 'LIFEToken'
    const CONTRACT_CLASS = 'LIFEToken'
    const ARTIFACT_FILE = 'artifacts/contracts/LIFEToken.sol/LIFEToken.json'
    const registryAddress = await _getRegistryAddress();

    // log to screen
    print(`Starting Deploy Contract ${CONTRACT_NAME}`);

    // start deploy contract to blockchain network
    const Contract = await hre.ethers.getContractFactory(CONTRACT_CLASS);
    const instance = await Contract.deploy(
        registryAddress,
        process.env.LIFE_TOKEN_NAME,
        process.env.LIFE_TOKEN_SYMBOL,
    );
    await instance.deployed();
    // log to screen
    print(`Contract ${CONTRACT_NAME} deployed at: ${instance.address}`);
    print('------------------------------------------');

    // update updateDeploymentOutput
    await _updateDeploymentOutput(
        CONTRACT_NAME,
        instance.address,
        '',
        ARTIFACT_FILE
    )
}

async function deployGFNExchangeLIFEBank() {
    const CONTRACT_NAME = 'GFNExchangeLIFEBank'
    const CONTRACT_CLASS = 'GeneFriendNetworkWallet'
    const ARTIFACT_FILE = 'artifacts/contracts/GeneFriendNetworkWallet.sol/GeneFriendNetworkWallet.json'
    const registryAddress = await _getRegistryAddress();

    // log to screen
    print(`Starting Deploy Contract ${CONTRACT_NAME}`);

    // start deploy contract to blockchain network
    const Contract = await hre.ethers.getContractFactory(CONTRACT_CLASS);
    const instance = await Contract.deploy(registryAddress)

    await instance.deployed();
    // log to screen
    print(`Contract ${CONTRACT_NAME} deployed at: ${instance.address}`);
    print('------------------------------------------');

    // update updateDeploymentOutput
    await _updateDeploymentOutput(CONTRACT_NAME, instance.address, '', ARTIFACT_FILE)
}

async function deployGFNExchangeWallet() {
    const CONTRACT_NAME = 'GFNExchangeWallet'
    const CONTRACT_CLASS = 'GeneFriendNetworkWallet'
    const ARTIFACT_FILE = 'artifacts/contracts/GeneFriendNetworkWallet.sol/GeneFriendNetworkWallet.json'
    const registryAddress = await _getRegistryAddress();

    // log to screen
    print(`Starting Deploy Contract ${CONTRACT_NAME}`);

    // start deploy contract to blockchain network
    const Contract = await hre.ethers.getContractFactory(CONTRACT_CLASS);
    const instance = await Contract.deploy(registryAddress)

    await instance.deployed();
    // log to screen
    print(`Contract ${CONTRACT_NAME} deployed at: ${instance.address}`);
    print('------------------------------------------');

    // update updateDeploymentOutput
    await _updateDeploymentOutput(CONTRACT_NAME, instance.address, '', ARTIFACT_FILE)
}

async function deployGFNProfitWallet() {
    const CONTRACT_NAME = 'GFNProfitWallet'
    const CONTRACT_CLASS = 'GeneFriendNetworkWallet'
    const ARTIFACT_FILE = 'artifacts/contracts/GeneFriendNetworkWallet.sol/GeneFriendNetworkWallet.json'
    const registryAddress = await _getRegistryAddress();

    // log to screen
    print(`Starting Deploy Contract ${CONTRACT_NAME}`);

    // start deploy contract to blockchain network
    const Contract = await hre.ethers.getContractFactory(CONTRACT_CLASS);
    const instance = await Contract.deploy(registryAddress)

    await instance.deployed();
    // log to screen
    print(`Contract ${CONTRACT_NAME} deployed at: ${instance.address}`);
    print('------------------------------------------');

    // update updateDeploymentOutput
    await _updateDeploymentOutput(CONTRACT_NAME, instance.address, '', ARTIFACT_FILE)
}

async function deployGenomicDAOToken() {
    const CONTRACT_NAME = 'GenomicDAOToken'
    const CONTRACT_CLASS = 'GenomicDAOToken'
    const ARTIFACT_FILE = 'artifacts/contracts/dao/GenomicDAOToken.sol/GenomicDAOToken.json'

    // log to screen
    print(`Starting Deploy Contract ${CONTRACT_NAME}`);

    // start deploy contract to blockchain network
    const Contract = await hre.ethers.getContractFactory(CONTRACT_CLASS);
    const instance = await Contract.deploy(
        process.env.DAO_TOKEN_OWNER,
        process.env.DAO_TOKEN_NAME,
        process.env.DAO_TOKEN_SYMBOL,
        process.env.DAO_TOKEN_CAP,
    )

    await instance.deployed();
    // log to screen
    print(`Contract ${CONTRACT_NAME} deployed at: ${instance.address}`);
    print('------------------------------------------');

    // update updateDeploymentOutput
    await _updateDeploymentOutput(
        CONTRACT_NAME,
        instance.address,
        process.env.DAO_TOKEN_OWNER,
        ARTIFACT_FILE
    )
}


async function deployGenomicDAOToken2LIFE() {
    const CONTRACT_NAME = 'GenomicDAOToken2LIFE'
    const CONTRACT_CLASS = 'GenomicDAOToken2LIFE'
    const ARTIFACT_FILE = 'artifacts/contracts/dao/GenomicDAOToken2LIFE.sol/GenomicDAOToken2LIFE.json'

    // log to screen
    print(`Starting Deploy Contract ${CONTRACT_NAME}`);

    // start deploy contract to blockchain network
    const Contract = await hre.ethers.getContractFactory(CONTRACT_CLASS);
    const instance = await Contract.deploy(
        process.env.GENOMIC_DAO_TOKEN_2_LIFE_OWNER,
        process.env.GENOMIC_DAO_TOKEN_ADDRESS,
        process.env.LIFE_TOKEN_ADDRESS,
        process.env.RESERVATION_LIFE_ADDRESS,
    )

    await instance.deployed();
    // log to screen
    print(`Contract ${CONTRACT_NAME} deployed at: ${instance.address}`);
    print('------------------------------------------');

    // update updateDeploymentOutput
    await _updateDeploymentOutput(
        CONTRACT_NAME,
        instance.address,
        process.env.GENOMIC_DAO_TOKEN_2_LIFE_OWNER,
        ARTIFACT_FILE
    )
}


async function deployLIFE2GenomicDAOToken() {
    const CONTRACT_NAME = 'LIFE2GenomicDAOToken'
    const CONTRACT_CLASS = 'LIFE2GenomicDAOToken'
    const ARTIFACT_FILE = 'artifacts/contracts/dao/LIFE2GenomicDAOToken.sol/LIFE2GenomicDAOToken.json'

    // log to screen
    print(`Starting Deploy Contract ${CONTRACT_NAME}`);

    // start deploy contract to blockchain network
    const Contract = await hre.ethers.getContractFactory(CONTRACT_CLASS);
    const instance = await Contract.deploy(
        process.env.LIFE_2_GENOMIC_DAO_TOKEN_OWNER,
        process.env.LIFE_TOKEN_ADDRESS,
        process.env.GENOMIC_DAO_TOKEN_ADDRESS,
        process.env.RESERVATION_DAO_TOKEN_ADDRESS,
    )

    await instance.deployed();
    // log to screen
    print(`Contract ${CONTRACT_NAME} deployed at: ${instance.address}`);
    print('------------------------------------------');

    // update updateDeploymentOutput
    await _updateDeploymentOutput(
        CONTRACT_NAME,
        instance.address,
        process.env.LIFE_2_GENOMIC_DAO_TOKEN_OWNER,
        ARTIFACT_FILE
    )
}


module.exports = {
    deployContractRegistry: deployContractRegistry,
    deployConfiguration: deployConfiguration,
    deployGeneNFTToken: deployGeneNFTToken,
    deployLIFEToken: deployLIFEToken,
    deployGFNExchangeLIFEBank: deployGFNExchangeLIFEBank,
    deployGFNExchangeWallet: deployGFNExchangeWallet,
    deployGFNProfitWallet: deployGFNProfitWallet,
    deployGenomicDAOToken: deployGenomicDAOToken,
    deployGenomicDAOToken2LIFE: deployGenomicDAOToken2LIFE,
    deployLIFE2GenomicDAOToken: deployLIFE2GenomicDAOToken,
};