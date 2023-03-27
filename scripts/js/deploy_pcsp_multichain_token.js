
const { ethers } = require("hardhat");
const hre = require("hardhat");

const ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'


// configuration
const initMintTokenAmount = ethers.utils.parseUnits("2000000")


async function main() {
    // Hardhat always runs the compile task when running scripts with its command
    // line interface.
    //
    // If this script is run directly using `node` you may want to call compile
    // manually to make sure everything is compiled
    // await hre.run('compile');

    // We get the contract to deploy

    const [deployer] = await ethers.getSigners();

    // Menu
    console.log("------ Steps ------")
    console.log("1. Deploy Token")
    console.log("2. Mint Token")
    console.log("3. Exit")
    console.log("-------------------")

    let response
    let selectedValue

    while (1) {
        response = await prompt({
            type: 'input',
            name: 'selection',
            message: 'Select step to execute'
        })

        selectedValue = parseInt(response.selection)

        switch (selectedValue) {
            case 1:
                // Deploy Token
                console.log("Start deployment ...")

                const bridgeToken = await hre.ethers.getContractFactory("AnyswapV6ERC20");
                const token = await bridgeToken.deploy(
                    "Stroke-Prevention GenomicDAO",
                    "PCSP",
                    18,
                    ZERO_ADDRESS,
                    deployer.address
                )

                await token.deployed();

                console.log("Token deployed at:", token.address);
                break;

            case 2:
                // Mint token
                console.log("Start minting token")

                const receiverAddress = process.env.ARB_MINT_ADDRESS

                const txn = await token.mint(
                    receiverAddress, initMintTokenAmount
                )

                console.log("Token minted to:", receiverAddress)
                console.log("Mint transaction", txn.hash)

                break;

            case 3:
                return;

            default:
                console.log(`Invalid selection; ${selectedValue}`)
                return
        }
    }
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
