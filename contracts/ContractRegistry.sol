// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/IContractRegistry.sol";


contract ContractRegistry is Ownable, IContractRegistry {

    // mapping from Contract name to contract address
    mapping(string => address) private _nameToAddress;
    // mapping from Contract address to Contract Name
    mapping(address => string) private _addressToName;
    // mapping from Contract address to GFN Operator
    mapping(address => address) private _gfnOperators;


    modifier validNewGFNOperator(address newGFNOperator) {
        require(
            newGFNOperator != address(0),
            "ContractRegistry: new GFN operator must be not empty"
        );
        _;
    }

    modifier registeredContractName(string memory name) {
        require(
            bytes(name).length > 0,
            "ContractRegistry: contract name must not be empty"
        );
        require(
            _nameToAddress[name] != address(0),
            "ContractRegistry: contract name is not registered"
        );
        _;
    }

    modifier registeredContractAddress(address _address) {
        require(
            _address != address(0),
            "ContractRegistry: contract address is invalid"
        );
        require(
            bytes(_addressToName[_address]).length != 0,
            "ContractRegistry: contract address is not registered"
        );
        _;
    }

    modifier notRegisteredContractName(string memory name) {
        require(
            bytes(name).length > 0,
            "ContractRegistry: contract name must not be empty"
        );
        require(
            _nameToAddress[name] == address(0),
            "ContractRegistry: contract name is registered"
        );
        _;
    }

    modifier notRegisteredContractAddress(address _address) {
        require(
            _address != address(0),
            "ContractRegistry: contract address is invalid"
        );
        require(
            bytes(_addressToName[_address]).length == 0,
            "ContractRegistry: contract address is registered"
        );
        _;
    }

    constructor(address gfnOwner) {
        transferOwnership(gfnOwner);
    }

    function setGFNOperator(
        address contractAddress,
        address newGFNOperator
    )
        external
        override
        onlyOwner
        registeredContractAddress(contractAddress)
        validNewGFNOperator(newGFNOperator)
    {
        address oldGFNOperator = _gfnOperators[contractAddress];
        _gfnOperators[contractAddress] = newGFNOperator;
        emit SetGFNOperator(oldGFNOperator, _gfnOperators[contractAddress]);
    }

    function registerContract(
        string memory name,
        address _address
    )
        external
        override
        onlyOwner
        notRegisteredContractName(name)
        notRegisteredContractAddress(_address)
    {
        _nameToAddress[name] = _address;
        _addressToName[_address] = name;

        emit RegisterContract(name, _address);
    }

    function removeContract(
        string memory name,
        address _address
    )
        external
        override
        onlyOwner
        registeredContractName(name)
        registeredContractAddress(_address)
    {
        _nameToAddress[name] = address(0);
        _addressToName[_address] = "";
        emit RemoveContract(name, _address);
    }

    function getGFNOperator(
        address contractAddress
    )
        external override view returns (address)
    {
        return _gfnOperators[contractAddress];
    }

    function isRegisteredContract(
        address _address
    )
        external override view returns(bool)
    {
        if(bytes(_addressToName[_address]).length > 0) {
            return true;
        } else {
            return false;
        }
    }

    function getContractAddress(
        string memory name
    ) 
        external override view returns(address) 
    {
        return _nameToAddress[name];
    }

    function getContractName(
        address _address
    )
        external override view returns(string memory name)
    {
        return _addressToName[_address];
    }

}