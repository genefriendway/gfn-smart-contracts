const { ethers } = require("hardhat")
const { prompt } = require('enquirer')

const config = {
  proxy: {
    bsc: process.env.BSC_MULTICHAIN_PROXY_ADDRESS,
    arbitrum: process.env.ARB_MULTICHAIN_PROXY_ADDRESS
  },
  bsc_token_address: process.env.BSC_TOKEN_ADDRESS,
  arbitrum_token_address: process.env.ARB_TOKEN_ADDRESS,
  bsc_bridge_address: process.env.BSC_BRIDGE_ADDRESS,
  arb_bridge_address: process.env.ARB_BRIDGE_ADDRESS,
  arb_chain_id: process.env.ARB_CHAIN_ID,
  bsc_chain_id: process.env.BSC_CHAIN_ID,
  token_receiver: process.env.TOKEN_RECEIVER_ADDRESS
}

const totalSupply = ethers.utils.parseUnits(process.env.PCSP_TOTAL_SUPPLY)


async function main() {
  // Configuration
  const [deployer] = await ethers.getSigners();

  // Menu
  console.log("------ Steps ------")
  console.log("1. Deploy Token")
  console.log("2. Deploy Bridge")
  console.log("3. Set token & client peers")
  console.log("4. Permission to mint")
  console.log("5. Exit")
  console.log("-------------------")

  let response
  let selectedValue
  let token
  let bridge

  while (1) {
    response = await prompt({
      type: 'input',
      name: 'selection',
      message: 'Select step to execute'
    })

    selectedValue = parseInt(response.selection)

    switch (selectedValue) {
      case 1:
        // Deploy token
        token = await deployToken(
          deployer
        )
        break;

      case 2:
        // Deploy bridge contract
        console.log("Start deploying bridge")

        const anyswapTokenAnycallClient = await ethers.getContractFactory("AnyswapTokenAnycallClient");
        bridge = await anyswapTokenAnycallClient.deploy(
          deployer.address,
          config.proxy.arbitrum
        )
        await bridge.deployed()

        console.log("Bridge contract deployed at: ", bridge.address)

        break;

      case 3:
        // Set token peers and client peers source BSC -> Arb
        const source_bridge = await ethers.getContractAt("AnyswapTokenAnycallClient", config.arb_bridge_address);

        console.log("Start setting peers")
        let txnResult = await source_bridge.setClientPeers(
          [config.bsc_chain_id], [config.bsc_bridge_address]
        )

        console.log("Client peers are set: ", txnResult?.hash)

        txnResult = await source_bridge.setTokenPeers(
          config.arbitrum_token_address, [config.bsc_chain_id], [config.bsc_token_address]
        )

        console.log("Token peers are set: ", txnResult?.hash)

        break;

      case 4:
        // Give bridge contract permission to mint and burn
        const dest_token = await ethers.getContractAt("CrossChainToken", config.arbitrum_token_address)

        console.log("Start giving bridge contract the minting permission")
        const txn = await dest_token?.transferOwnership(config.arb_bridge_address)

        console.log("Minter is set: ", txn?.hash)

        break;

      case 5:
        return

      default:
        console.log(`Invalid selection; ${selectedValue}`)
        return
    }
  }
}

async function deployToken(deployer) {
  console.log("Start deployment ...")

  const crossChainToken = await ethers.getContractFactory("GenomicDAOToken");

  const token = await crossChainToken.deploy(
    deployer.address,
    process.env.FAIR_LAUNCH_TOKEN_NAME,
    process.env.FAIR_LAUNCH_TOKEN_SYMBOL,
    totalSupply
  )
  await token.deployed()

  console.log("Token deployed at: ", token.address)

  return token
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
