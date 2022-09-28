const hre = require("hardhat");
const fs = require('fs');
const lib = require('./lib.js');
const deployment = require('./deployment.js');
const { prompt } = require('enquirer');

const print = console.log


async function verifyEnvironment() {
    const deployer = await web3.eth.accounts.privateKeyToAccount(process.env.GFN_DEPLOYER_PRIVATE_KEY);
    print('================ Environment Variables ==================');
    print(`ENV_NAME             : ${process.env.ENV_NAME}`);
    print(`Deployer Address                 : ${deployer.address}`);
    print(`GFN_REGISTRY_OWNER_ADDRESS       : ${process.env.GFN_REGISTRY_OWNER_ADDRESS}`);
    print(`GFN_CONFIGURATION_OWNER_ADDRESS  : ${process.env.GFN_CONFIGURATION_OWNER_ADDRESS}`);
    print(`GFN_GNFT_OPERATOR_ADDRESS        : ${process.env.GFN_GNFT_OPERATOR_ADDRESS}`);
    print(`GFN_NFT_HOLDER_ADDRESS           : ${process.env.GFN_NFT_HOLDER_ADDRESS}`);
    print(`LIFE_TREASURY_ADDRESS            : ${process.env.LIFE_TREASURY_ADDRESS}`);
    print('-----------------------------------------------------------')
    print(`GFN_EXCHANGE_WALLET_OPERATOR_ADDRESS     : ${process.env.GFN_EXCHANGE_WALLET_OPERATOR_ADDRESS}`);
    print(`GFN_PROFIT_WALLET_OPERATOR_ADDRESS       : ${process.env.GFN_PROFIT_WALLET_OPERATOR_ADDRESS}`);
    print(`GFN_EXCHANGE_LIFE_BANK_OPERATOR_ADDRESS  : ${process.env.GFN_EXCHANGE_LIFE_BANK_OPERATOR_ADDRESS}`);
    print('-----------------------------------------------------------')
    print(`GNFT_TOKEN_NAME      : ${process.env.GNFT_TOKEN_NAME}`);
    print(`GNFT_TOKEN_SYMBOL    : ${process.env.GNFT_TOKEN_SYMBOL}`);
    print(`LIFE_TOKEN_NAME      : ${process.env.LIFE_TOKEN_NAME}`);
    print(`LIFE_TOKEN_SYMBOL    : ${process.env.LIFE_TOKEN_SYMBOL}`);
    print('-----------------------------------------------------------')
    print(`DAO_TOKEN_OWNER      : ${process.env.DAO_TOKEN_OWNER}`);
    print(`DAO_TOKEN_NAME       : ${process.env.DAO_TOKEN_NAME}`);
    print(`DAO_TOKEN_SYMBOL     : ${process.env.DAO_TOKEN_SYMBOL}`);
    print(`DAO_TOKEN_CAP        : ${process.env.DAO_TOKEN_CAP}`);
    print('-----------------------------------------------------------')
    print(`GENOMIC_DAO_TOKEN_ADDRESS        : ${process.env.GENOMIC_DAO_TOKEN_ADDRESS}`);
    print(`LIFE_TOKEN_ADDRESS               : ${process.env.LIFE_TOKEN_ADDRESS}`);
    print('-----------------------------------------------------------')
    print(`GENOMIC_DAO_TOKEN_2_LIFE_OWNER   : ${process.env.GENOMIC_DAO_TOKEN_2_LIFE_OWNER}`);
    print(`RESERVATION_LIFE_ADDRESS         : ${process.env.RESERVATION_LIFE_ADDRESS}`);
    print('-----------------------------------------------------------')
    print(`LIFE_2_GENOMIC_DAO_TOKEN_OWNER   : ${process.env.LIFE_2_GENOMIC_DAO_TOKEN_OWNER}`);
    print(`RESERVATION_DAO_TOKEN_ADDRESS    : ${process.env.RESERVATION_DAO_TOKEN_ADDRESS}`);
    print('-----------------------------------------------------------')
    print(`TOKEN_WALLET_OF_ERC20_CODE       :${process.env.TOKEN_WALLET_OF_ERC20_CODE}`)
    print(`TOKEN_WALLET_OF_ERC20_ADDRESS    :${process.env.TOKEN_WALLET_OF_ERC20_ADDRESS}`)
    print(`TOKEN_WALLET_OWNER               :${process.env.TOKEN_WALLET_OWNER}`)
    print('-----------------------------------------------------------')
    print(`PCSP_CONFIGURATION_OWNER         :${process.env.PCSP_CONFIGURATION_OWNER}`)
    print('-----------------------------------------------------------')
    print(`PCSP_REWARD_OWNER                    :${process.env.PCSP_REWARD_OWNER}`)
    print(`PCSP_REWARD_CONFIGURATION_ADDRESS    :${process.env.PCSP_REWARD_CONFIGURATION_ADDRESS}`)
    print('=======================================================');

    const response = await prompt({
        type: 'input',
        name: 'selection',
        message: `Verify ENV: ${process.env.ENV_NAME} [yes|no]?`
    });
    if (response['selection'].toLowerCase() === 'yes') {
        print(`=> Continue processing ENV: ${process.env.ENV_NAME}`);
    } else {
        print(`=> Stop processing ENV: ${process.env.ENV_NAME}`);
        process.exit(0);
    }
}

async function getDefaultDeploymentOutput() {
    const deployer = await web3.eth.accounts.privateKeyToAccount(process.env.GFN_DEPLOYER_PRIVATE_KEY);
    const env = process.env
    env['GFN_DEPLOYER_PRIVATE_KEY'] = 'xxxxxxxxxx'
    env['GFN_DEPLOYER'] = deployer.address
    return {
        env_name: process.env.ENV_NAME,
        network: hre.network.name,
        chainId: hre.network.config.chainId,
        environments: env,
        contracts: {}
    }
}

async function initDeploymentOutputFile() {
    print("======= Deployment Output File Menu ========")
    print('1. Create a new deployment output file');
    print('2. Input an existed deployment output file');
    print('99. Exit!');
    print("==============================")

    const response = await prompt({
        type: 'input',
        name: 'selection',
        message: 'Select deployment output file menu?'
    });

    let deploymentOutputFile;
    let number = parseInt(response.selection);
    switch(number) {
        case 1:
            deploymentOutputFile = `deployment_${hre.network.name}_${process.env.ENV_NAME.toLowerCase()}_${new Date().toISOString()}.json`;
            // create a new empty output json file
            fs.openSync(deploymentOutputFile, 'w');
            // write default deployment data to json
            const DEFAULT_DATA = await getDefaultDeploymentOutput();
            await lib.writeToJSON(DEFAULT_DATA, deploymentOutputFile)
            print(`==> Deployment Output File is created: ${deploymentOutputFile}`)
            break;
        case 2:
            const response = await prompt({
                type: 'input',
                name: 'selection',
                message: 'Input existed deployment output file?'
            });
            if (fs.existsSync(response.selection)) {
                deploymentOutputFile = response.selection;
            } else {
                print(`Error: File not existed ${response.selection}`)
                process.exit(0)
            }
            break;
        case 3:
            process.exit(0)
            break;
        default:
            throw new Error(`Selected number invalid: ${number}`);
    }

    process.env.DEPLOYMENT_OUTPUT_FILE = deploymentOutputFile;
}

async function selectEnvironment() {
    // Select Environment File
    print("=========== ENV ==============")
    print('1. env.local')
    print('2. env.nightly')
    print('3. env.production')
    print("==============================")

    const response = await prompt({
        type: 'input',
        name: 'envFile',
        message: 'Select Environment File?'
    });

    require('dotenv').config({ path: response['envFile'] });
    print(`=> You are selected ENV: ${process.env.ENV_NAME}`)

    return response['envFile']
}

async function selectContractsToDeploy() {
    print("======= Contract Menu ========")
    print('1. ContractRegistry');
    print('2. Configuration');
    print('3. GeneNFTToken');
    print('4. LIFEToken');
    print('5. GFNExchangeLIFEBank');
    print('6. GFNExchangeWallet');
    print('7. GFNProfitWallet');
    print('8. GenomicDAOToken');
    print('9. GenomicDAOToken2LIFE');
    print('10. LIFE2GenomicDAOToken');
    print('11. TokenWallet');
    print('12. PCSPConfiguration');
    print('13. PCSPReward');
    print("==============================")

    const response = await prompt({
        type: 'input',
        name: 'selectedNumbers',
        message: 'Select contracts to deploy?'
    });

    const numbers = response.selectedNumbers.split(",");
    for (let i = 0; i < numbers.length; i++) {
        let number = parseInt(numbers[i].trim());
        switch(number) {
          case 1:
            await deployment.deployContractRegistry();
            break;
          case 2:
            await deployment.deployConfiguration();
            break;
          case 3:
            await deployment.deployGeneNFTToken();
            break;
          case 4:
            await deployment.deployLIFEToken();
            break;
          case 5:
            await deployment.deployGFNExchangeLIFEBank();
            break;
          case 6:
            await deployment.deployGFNExchangeWallet();
            break;
          case 7:
            await deployment.deployGFNProfitWallet();
            break;
          case 8:
            await deployment.deployGenomicDAOToken();
            break;
          case 9:
            await deployment.deployGenomicDAOToken2LIFE();
            break;
          case 10:
            await deployment.deployLIFE2GenomicDAOToken();
            break;
          case 11:
            await deployment.deployTokenWallet();
            break;
          case 12:
            await deployment.deployPCSPConfiguration();
            break;
          case 13:
            await deployment.deployPCSPReward();
            break;

          default:
            throw new Error(`Selected number invalid: ${number}`);
        }
    }

}

async function main() {
    // verify environment file
    await verifyEnvironment();

    // init Deployment Output File
    await initDeploymentOutputFile();

    // select Contracts you want to deploy
    await selectContractsToDeploy();

}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
