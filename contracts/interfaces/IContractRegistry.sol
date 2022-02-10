// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

interface  IContractRegistry {

    // Declare events
    event RegisterContract(string indexed name, address indexed _address);
    event RemoveContract(string indexed name, address indexed _address);

    // Declare Functions
    function registerContract(string memory name, address _address) external;
    function removeContract(string memory name, address _address) external;

    function isRegisteredContract(address _address) external view returns (bool);
    function getContractAddress(string memory name) external view returns (address);
    function getContractName(address _address) external view returns (string memory name);

}