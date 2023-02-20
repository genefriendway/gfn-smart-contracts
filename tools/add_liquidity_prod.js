require('dotenv').config()

const Web3 = require('web3')
const Contract = require('web3-eth-contract');
const HDWalletProvider = require('truffle-hdwallet-provider')

// Configuration
const pkeys = ['']
const routerAddress = '0x10ED43C718714eb63d5aA57B78B54704E256024E'  // pancake router
const pcspTokenAddress = ''
const usdtTokenAddress = '0x55d398326f99059fF775485246999027B3197955'
const url = 'https://bsc-dataseed.binance.org'

const provider = new HDWalletProvider(
    pkeys,
    url,
    0,
    pkeys.length
)

Contract.setProvider(provider);

const web3 = new Web3(provider)
const { utils } = web3

const ROUTER = {
    abi: require('../abis/PancakeSwap.json'),
    address: routerAddress
}

const USDT = {
    abi: require('../abis/USDTToken.json'),
    address: usdtTokenAddress
}

const PCSP = {
    abi: require('../abis/PCSPToken.json'),
    address: pcspTokenAddress
}

function with0x(pkey) {
    return pkey.substring(0, 2) == '0x' ? pkey : '0x' + pkey
}

function getAccount(pkey) {
    const account = web3.eth.accounts.privateKeyToAccount(with0x(pkey))
    return {
        address: account.address,
        privateKey: account.privateKey
    }
}

async function getCurrentTimestamp() {
    const blockNumber = await web3.eth.getBlockNumber()
    const block = await web3.eth.getBlock(blockNumber)

    return block.timestamp
}

async function main() {

    // Setup contract
    const usdtToken = new Contract(USDT.abi, USDT.address)
    const pcspToken = new Contract(PCSP.abi, PCSP.address)
    const routerPancake = new Contract(ROUTER.abi, ROUTER.address)

    const usdtTokenOptions = usdtToken.options
    const pcspTokenOptions = pcspToken.options
    const routerPancakeOptions = routerPancake.options

    const account = getAccount(pkeys[0])

    const amountIn = utils.toWei('1', 'ether')
    const approveAmount = utils.toWei('3', 'ether')

    // Add liquidity
    const pcspLiquidAmount = utils.toWei('5000', 'ether')
    const usdtLiquidAmount = utils.toWei('10', 'ether')
    await addLiquidityPair(
        routerPancake,
        account.address,
        pcspToken,
        usdtToken,
        pcspLiquidAmount,
        usdtLiquidAmount
    )
}

async function addLiquidityPair(routerContract, fromAccount, pcspTokenContract, usdtTokenContract, pcspAmount, usdtAmount) {
    console.log("Start adding PCSP/USDT liquidity pool")
    console.log("PCSP amount: ", pcspAmount.toString())
    console.log("USDT amount: ", usdtAmount.toString())

    const currentTimestamp = await getCurrentTimestamp()
    const deadline = currentTimestamp + 60 * 10;    // 10mins from current time

    const routerAddress = routerContract.options.address
    const pcspAddress = pcspTokenContract.options.address
    const usdtAddress = usdtTokenContract.options.address

    // Approve PCSP
    const approvePCSP = await pcspTokenContract.methods.approve(
        routerAddress,
        pcspAmount
    ).send({ from: fromAccount })
    console.log("Approve PCSP: ", approvePCSP.transactionHash)


    // Approve USDT
    const approveUSDT = await usdtTokenContract.methods.approve(
        routerAddress,
        usdtAmount
    ).send({ from: fromAccount })
    console.log("Approve USDT: ", approveUSDT.transactionHash)

    // Create liquidity pair
    const liquidityPair = await routerContract.methods.addLiquidity(
        pcspAddress,
        usdtAddress,
        pcspAmount,
        usdtAmount,
        0,
        0,
        fromAccount,
        deadline
    ).send({ from: fromAccount })

    console.log('Liquidity Pair: ', liquidityPair.transactionHash)

}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });