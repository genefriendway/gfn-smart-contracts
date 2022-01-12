## Description
GFN will have multiple smart contracts. To interact with each other, one will need to acknowledge the other's address.

ContractRegistry will be the place where GFN's smart contracts are registered and looking for others' addresses.

## API
- `function registerContract(string memory name, address _address)`
  - register a new contract's address along with its name into the registry
  - only gfnOwner will be allowed to use this API
- `function removeContract(string memory name, address _address)`
  - remove a contract record from the registry
  - only gfnOwner will be allowed to use this API
- `function getContractAddress(string memory name)`
  - retrieve a smart contract's address by specifying its registered name
  - any entity can use this API
- `function getContractName(address _address)`
  - retrieve a smart contract's name by specifying its registered address
  - any entity can use this API