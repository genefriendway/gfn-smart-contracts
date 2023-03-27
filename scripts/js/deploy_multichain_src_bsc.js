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


async function main() {
  // Configuration
  const [deployer] = await ethers.getSigners();

  // Menu
  console.log("------ Steps ------")
  console.log("1. Deploy Bridge")
  console.log("2. Set token & client peers")
  console.log("3. Transfer token to bridge")
  console.log("4. Bridge out")
  console.log("5. Exit")
  console.log("-------------------")

  let response
  let selectedValue
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
        // Deploy bridge contract
        console.log("Start deploying bridge")

        const anyswapTokenAnycallClient = await ethers.getContractFactory("AnyswapTokenAnycallClient");
        bridge = await anyswapTokenAnycallClient.deploy(
          deployer.address,
          config.proxy.bsc
        )
        await bridge.deployed()

        console.log("Bridge contract deployed at: ", bridge.address)

        break;

      case 2:
        // Set token peers and client peers source BSC -> Goerli

        const source_bridge = await ethers.getContractAt("AnyswapTokenAnycallClient", config.bsc_bridge_address);

        console.log("Start setting peers")
        let txnResult = await source_bridge.setClientPeers(
          [config.arb_chain_id], [config.arb_bridge_address]
        )

        console.log("Client peers are set: ", txnResult?.hash)

        txnResult = await source_bridge.setTokenPeers(
          config.bsc_token_address, [config.arb_chain_id], [config.arbitrum_token_address]
        )

        console.log("Token peers are set: ", txnResult?.hash)

        break;

      case 3:
        break;

      case 4:
        // Bridge out all token on bridge BSC -> Arb
        console.log("Start bridging out")

        const token = await ethers.getContractAt("GenomicDAOFairLaunchToken", process.env.BSC_TOKEN_ADDRESS)

        const bsc_bridge = await ethers.getContractAt("AnyswapTokenAnycallClient", config.bsc_bridge_address);

        const bridegAmount = await token.balanceOf(config.bsc_bridge_address)

        const flags = 2

        const fee = { value: ethers.utils.parseEther("0.02") }

        let bridgeTxn = await bsc_bridge.swapout(
          config.bsc_token_address,
          bridegAmount,
          config.token_receiver,
          config.arb_chain_id,
          flags,
          fee
        )

        console.log(`Bridge out ${bridegAmount.toString()}: ${bridgeTxn.hash}`)

        break;

      default:
        console.log(`Invalid selection; ${selectedValue}`)
        return
    }
  }
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
