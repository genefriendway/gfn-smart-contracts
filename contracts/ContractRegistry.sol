// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/IContractRegistry.sol";


contract ContractRegistry is Ownable, IContractRegistry {

    mapping(string => address) private _nameToAddress;
    mapping(address => string) private _addressToName;

    modifier registeredName(string memory name) {
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

    modifier registeredAddress(address _address) {
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

    modifier notRegisteredName(string memory name) {
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

    modifier notRegisteredAddress(address _address) {
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

    constructor(address owner) {
        transferOwnership(owner);
    }

    function registerContract(
        string memory name, 
        address _address
    ) 
        external
        override onlyOwner notRegisteredName(name) notRegisteredAddress(_address)
    {
        _nameToAddress[name] = _address;
        _addressToName[_address] = name;

        emit RegisterContract(name, _address);
    }

    function removeContract(
        string memory name,
        address _address
    )
        external override onlyOwner registeredName(name) registeredAddress(_address)
    {
        delete _nameToAddress[name];
        delete _addressToName[_address];
        emit RemoveContract(name, _address);
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