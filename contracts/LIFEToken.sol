// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/IContractRegistry.sol";
import "../interfaces/ILIFEToken.sol";
import "../interfaces/IGNFTToken.sol";


contract LIFEToken is ERC20, Ownable, ILIFEToken {

    IContractRegistry public registry;

    struct GNFTRange {
        uint256 lower;
        uint256 upper;
        uint256 numerOfLIFEToMint;
    }
    // Mapping from index to GNFTRange
    mapping(uint256 => GNFTRange) private _tableOfMintingLIFE;


    modifier onlyGNFTToken() {
        require(
            _msgSender() == _getGNFTTokenAddress(),
            "LIFEToken: caller is not GNFTToken contract"
        );
        _;
    }

    constructor(
        address gfnOwner,
        IContractRegistry _registry,
        string memory name,
        string memory symbol
    ) 
        ERC20(name, symbol) 
    {
        registry = _registry;
        _initializeTableOfMintingLIFE();
        transferOwnership(gfnOwner);
    }

    function findNumberOfLIFEToMint(
        uint256 totalGNFTTokens
    )
        public view returns (uint256)
    {
        uint256 minIndex = 1;
        uint256 maxIndex = 11;
        for(uint256 index = minIndex; index <= maxIndex; index++) {
            GNFTRange storage range = _tableOfMintingLIFE[index];
            if (totalGNFTTokens >= range.lower
                && totalGNFTTokens <= range.upper) {
                return range.numerOfLIFEToMint;
            }
        }
        return 0;
    }

    function mintLIFE(
        uint256 geneticProfileId
    ) external override onlyGNFTToken {
        address lifeTreasuryAddress = _getLIFETreasuryAddress();
        require(
            lifeTreasuryAddress != address(0),
            "LIFEToken: Please register LIFETreasury in ContractRegistry"
        );

        // find number of LIFE to mint
        uint256 totalGNFTTokens = _getGNFTTokenInstance().getTotalGeneticProfiles();
        uint256 numberOfLIFEToMint = findNumberOfLIFEToMint(totalGNFTTokens);

        if (numberOfLIFEToMint > 0) {
            // Mint new LIFE tokens to LIFETreasury contract
            _mint(lifeTreasuryAddress, numberOfLIFEToMint);

            emit MintLIFE(lifeTreasuryAddress, geneticProfileId);
        }
    }

    function burnLIFE(uint256 amount) external override {
        address accountToBurn = _msgSender();
        require(
            balanceOf(accountToBurn) >= amount,
            "LIFEToken: burn amount exceeds balance"
        );
        _burn(accountToBurn, amount);
        emit BurnLIFE(accountToBurn, amount);
    }


    function _getLIFETreasuryAddress() internal view returns (address) {
        return registry.getContractAddress('LIFETreasury');
    }

    function _getGNFTTokenAddress() internal view returns (address) {
        return registry.getContractAddress('GNFTToken');
    }

    function _getGNFTTokenInstance() internal view returns (IGNFTToken) {
        return  IGNFTToken(_getGNFTTokenAddress());
    }

    function _initializeTableOfMintingLIFE() private {
//        _tableOfMintingLIFE[index] = GNFTRange(lower, upper, number of LIFE);
        _tableOfMintingLIFE[1] = GNFTRange(1, 1, 90000000e18);
        _tableOfMintingLIFE[2] = GNFTRange(2, 10, 10000000e18);
        _tableOfMintingLIFE[3] = GNFTRange(11, 100, 1000000e18);
        _tableOfMintingLIFE[4] = GNFTRange(101, 1000, 100000e18);
        _tableOfMintingLIFE[5] = GNFTRange(1001, 10000, 10000e18);
        _tableOfMintingLIFE[6] = GNFTRange(10001, 100000, 1000e18);
        _tableOfMintingLIFE[7] = GNFTRange(100001, 1000000, 100e18);
        _tableOfMintingLIFE[8] = GNFTRange(1000001, 10000000, 10e18);
        _tableOfMintingLIFE[9] = GNFTRange(10000001, 100000000, 1e18);
        _tableOfMintingLIFE[10] = GNFTRange(100000001, 1000000000, 1e17);
        _tableOfMintingLIFE[11] = GNFTRange(1000000001, 10000000000, 1e16);
    }
}
