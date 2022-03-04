// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

interface  IContractRegistry {

    // Declare events
    event SetGFNOperator(address indexed oldGFNOperator, address indexed newGFNOperator);
    event RegisterContract(string name, address indexed _address);
    event RemoveContract(string name, address indexed _address);

    // Declare Functions
    function setGFNOperator(address contractAddress, address newGFNOperator) external;
    function registerContract(string memory name, address _address) external;
    function removeContract(string memory name, address _address) external;

    function getGFNOperator(address contractAddress) external view returns (address);
    function isRegisteredContract(address _address) external view returns (bool);
    function getContractAddress(string memory name) external view returns (address);
    function getContractName(address _address) external view returns (string memory name);

}