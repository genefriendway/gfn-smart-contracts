require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-web3");
const { prompt } = require('enquirer');
const print = console.log


require('dotenv').config({ path: '.env.local' });


const config = {
    defaultNetwork: "hardhat",
    networks: {
        hardhat: {
            accounts: { count: 200 }
        },
        eth_rinkeby: {
            url: `https://rinkeby.infura.io/v3/${process.env.INFURA_API_KEY}`,
            accounts: [`${process.env.GFN_DEPLOYER_PRIVATE_KEY}`],
            gas: 8100000,
            gasPrice: 8000000000
        },
        avax_testnet: {
            url: 'https://api.avax-test.network/ext/bc/C/rpc',
            chainId: 43113,
            accounts: [`${process.env.GFN_DEPLOYER_PRIVATE_KEY}`],
        },
        avax_mainnet: {
            url: 'https://api.avax.network/ext/bc/C/rpc',
            chainId: 43114,
            accounts: [`${process.env.GFN_DEPLOYER_PRIVATE_KEY}`],
        },
        oasis_testnet: {
            url: 'https://testnet.emerald.oasis.dev',
            chainId: 42261,
            accounts: [`${process.env.GFN_DEPLOYER_PRIVATE_KEY}`],
        },
        oasis_mainnet: {
            url: 'https://emerald.oasis.dev',
            chainId: 42262,
            accounts: [`${process.env.GFN_DEPLOYER_PRIVATE_KEY}`],
        },
        bsc_testnet: {
            url: 'https://data-seed-prebsc-1-s1.binance.org:8545',
            chainId: 97,
            accounts: [`${process.env.GFN_DEPLOYER_PRIVATE_KEY}`],
        },
        bsc_mainnet: {
            url: 'https://bsc-dataseed.binance.org',
            chainId: 56,
            accounts: [`${process.env.GFN_DEPLOYER_PRIVATE_KEY}`],
        },

    },
    accounts: {
        count: 200
    },
//    etherscan: {
//        apiKey: `${process.env.ETHERSCAN_KEY}`
//    },
    solidity: {
        compilers: [
            {
                version: "0.8.11",
                settings: {
                    optimizer: {
                        enabled: true,
                        runs: 200
                    }
                }
            }
        ],
    },
    paths: {
        sources: "./contracts",
        tests: "./test",
        cache: "./cache",
        artifacts: "./artifacts",
        deploy: 'deploy',
        deployments: 'deployments',
    },
};

module.exports = config;
