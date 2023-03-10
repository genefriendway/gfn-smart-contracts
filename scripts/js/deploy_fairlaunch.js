const { ethers } = require("hardhat");
const hre = require("hardhat");
const { prompt } = require('enquirer');

const env = 'dev'

const timeSecond = 1
const timeMinute = timeSecond * 60
const timeHour = timeMinute * 60
const timeDay = timeHour * 24
const timeMonth = timeDay * 30

const timeDurationUnit = (env == 'dev') ? timeSecond : timeMonth

const configuration = {
  'dev': {
    listingDuration: timeMinute * 3,  // 3 mins
    finishListingFeePercent: 2,
    startVestingTime: (1676695676 + 120).toString(),
    taxReceiverAccount: "",
    gasPrice: "20000000000",
    vestingConfig: [
      {
        name: 'Community Development',
        address: '',
        percentageAllocation: 10,
        cliff: 0,
        duration: timeDurationUnit * 48,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'Developer Endowment',
        address: '',
        percentageAllocation: 10,
        cliff: timeDurationUnit * 3,
        duration: timeDurationUnit * 48,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'Strategic Partners',
        address: '',
        percentageAllocation: 5,
        cliff: timeDurationUnit * 3,
        duration: timeDurationUnit * 60,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'Liquidity',
        address: '', // Same token owner
        percentageAllocation: 5,
        cliff: 0,
        duration: 1, // Release immediately
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'Team',
        address: '',
        percentageAllocation: 10,
        cliff: timeDurationUnit * 18,
        duration: timeDurationUnit * 120,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'Advisor',
        address: '',
        percentageAllocation: 5,
        cliff: timeDurationUnit * 12,
        duration: timeDurationUnit * 60,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'R&D',
        address: '',
        percentageAllocation: 15,
        cliff: timeDurationUnit * 3,
        duration: timeDurationUnit * 60,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'Reserved for next stage evolution',
        address: '',
        percentageAllocation: 10,
        cliff: timeDurationUnit * 12,
        duration: timeDurationUnit * 60,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'GenomicDAO Launchpad Locked Tokens',
        address: '',
        percentageAllocation: 30,
        cliff: timeDurationUnit * 6,
        duration: timeDurationUnit * 24,
        sliceVesting: timeDurationUnit * 1
      }
    ]
  },
  'prod': {
    listingDuration: timeMinute * 3,  // 3 mins
    finishListingFeePercent: 2,
    startVestingTime: '1676851200', // 20/02/2023 7:00:00 AM 
    taxReceiverAccount: "",
    gasPrice: "10000000000",
    vestingConfig: [
      {
        name: 'Community Development',
        address: '',
        percentageAllocation: 10,
        cliff: 0,
        duration: timeDurationUnit * 48,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'Developer Endowment',
        address: '',
        percentageAllocation: 10,
        cliff: timeDurationUnit * 3,
        duration: timeDurationUnit * 48,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'Strategic Partners',
        address: '',
        percentageAllocation: 5,
        cliff: timeDurationUnit * 3,
        duration: timeDurationUnit * 60,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'Liquidity',
        address: '', // Same token owner
        percentageAllocation: 5,
        cliff: 0,
        duration: 1, // Release immediately
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'Team',
        address: '',
        percentageAllocation: 10,
        cliff: timeDurationUnit * 18,
        duration: timeDurationUnit * 120,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'Advisor',
        address: '',
        percentageAllocation: 5,
        cliff: timeDurationUnit * 12,
        duration: timeDurationUnit * 60,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'R&D',
        address: '',
        percentageAllocation: 15,
        cliff: timeDurationUnit * 3,
        duration: timeDurationUnit * 60,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'Reserved for next stage evolution',
        address: '',
        percentageAllocation: 10,
        cliff: timeDurationUnit * 12,
        duration: timeDurationUnit * 60,
        sliceVesting: timeDurationUnit * 1
      },
      {
        name: 'GenomicDAO Launchpad Locked Tokens',
        address: '',
        percentageAllocation: 30,
        cliff: timeDurationUnit * 6,
        duration: timeDurationUnit * 24,
        sliceVesting: timeDurationUnit * 1
      }
    ]
  },
}


async function selectStep() {
  // Configuration
  const [deployer] = await ethers.getSigners();
  const totalSupply = ethers.utils.parseUnits("1000000000");
  const config = configuration[env]

  let token
  let vesting

  // Menu
  console.log("----- Steps -----")
  console.log("1. Deploy token")
  console.log("2. Deploy lock vesting")
  console.log("3. Mint token")
  console.log("4. Setup token tax receiver")
  console.log("5. Setup vesting schedule")
  console.log("6. Release liquidity vesting")
  console.log("7. Exit")
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
        // Deploy token
        token = await deployToken(deployer, totalSupply, config.listingDuration, config.finishListingFeePercent)
        break;

      case 2:
        // Deploy lock vesting
        vesting = await deployVesting(token, deployer)
        break;

      case 3:
        // Mint token
        await mintTokenToVesting(token, vesting, totalSupply);
        break;

      case 4:
        // Setup token tax receiver
        await setupTax(token, config.taxReceiverAccount, config.gasPrice)
        break;

      case 5:
        // Setup vesting schedule
        await setupVesting(vesting, totalSupply, config.startVestingTime, config.vestingConfig);
        break;

      case 6:
        // Release liquidity vesting
        await releaseLiquidityVesting(vesting, deployer.address)
        break;

      case 7:
        // Exit
        return

      default:
        console.log(`Invalid selection: ${selectedValue}`)
        break

    }
  }
}

async function main() {

  await selectStep();

}

async function deployToken(deployer, totalSupply, listingDuration, finishListingFeePercent) {
  console.log("Start deployment ...");

  // Deploy token
  const fairLaunchToken = await hre.ethers.getContractFactory("GenomicDAOFairLaunchToken");

  const token = await fairLaunchToken.deploy(deployer.address, "Stroke-Prevention GenomicDAO", "PCSP", listingDuration, finishListingFeePercent, totalSupply);
  await token.deployed();

  console.log("Token deployed at: ", token.address)

  return token;
}

async function deployVesting(token, deployer) {
  console.log("Start deployment ...");

  const vestingSchedule = await hre.ethers.getContractFactory("TokenVesting");

  const vesting = await vestingSchedule.deploy(token.address, deployer.address)
  console.log("Vesting contract deployed at: ", vesting.address)

  return vesting
}

async function mintTokenToVesting(token, vesting, amount) {
  console.log("Start minting: ", amount.toString());

  // Mint 1b PCSP -> lock vesting
  await token.mint(vesting.address, amount)
  console.log(`Token ${token.address} minted to ${vesting.address}`);
}

async function setupVesting(vesting, totalSupply, startVestingTime, vestingConfig) {
  console.log("Start setting up vesting schedule")
  // Setup vesting schedule
  const revocable = true

  for (i in vestingConfig) {
    let item = vestingConfig[i]

    let amount = totalSupply.mul(item.percentageAllocation).div(100);

    console.log(`Create vesting: ${item.name}, amount: ${amount.toString()}`)

    // Create vesting schedule
    await vesting.createVestingSchedule(
      item.address,
      startVestingTime,
      item.cliff,
      item.duration,
      item.sliceVesting,
      revocable,
      amount
    )
  }
}

async function setupTax(token, taxReceiver, gasPrice) {
  console.log("Setting token tax")
  // Setup tax receiver
  await token.setTransferFee(taxReceiver, 2, 5, 0)

  // Setup gas price
  await token.setMaxGasPrice(gasPrice)
}

async function releaseLiquidityVesting(vesting, liquidityAccount) {
  console.log("Start releasing all liquidity vesting")

  const vestingScheduleId = await vesting.computeVestingScheduleIdForAddressAndIndex(liquidityAccount, 0);

  const releasableAmount = await vesting.computeReleasableAmount(vestingScheduleId);

  await vesting.release(vestingScheduleId, releasableAmount);

  console.log("Released: ", releasableAmount.toString())

}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });