# Gene Friend Network - Smart Contracts

## Prerequisites
* Python version: Python 3.6.9

## Getting started
### Installing
* Install Brownie and related libraries: `pip install -r requirements.txt`
* Brownie has the following dependencies:
    - `python` 3.6+, `python3-dev`
    - `ganache-cli` - tested with version 6.12.2
    - Install Openzepplin:
      - `brownie pm install OpenZeppelin/openzeppelin-contracts@4.4.1`

### Compile contract
    - Compile Contracts: `brownie compile`

### Running the tests
  - Run Unit tests: `brownie test`
  - Test On Remix Env:
    1. Install **remixd** at https://www.npmjs.com/package/remixd
    2. Run: `remixd -s <absolute-path to project> --remix-ide https://remix.ethereum.org`

## Project structure
  - `contracts/`: Contract sources
  - `interfaces/`: Interface sources
  - `scripts/`: Scripts for deployment and interaction
  - `tests/`: Scripts for testing the project
  - `build/`: Project data such as compiler artifacts and unit test results
  - `reports/`: JSON report files for use in the GUI