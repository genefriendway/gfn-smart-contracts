// SPDX-License-Identifier: MIT

pragma solidity ^0.8.11;

interface IUniswapV2Factory {
    function createPair(address tokenA, address tokenB)
    external
    returns (address pair);
}

interface IUniswapV2Router01 {
    function factory() external pure returns (address);
}

interface IUniswapV2Router02 is IUniswapV2Router01 {}

library LDex {
    bytes4 private constant FACTORY_SELECTOR =
    bytes4(keccak256(bytes("factory()")));

    // address internal constant _wbnb =
    //     address(0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c);
    address internal constant _wbnb =
    address(0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd); // testnet

    // address internal constant _busd =
    //     address(0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56);
    address internal constant _busd =
    address(0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56); // testnet

    function _isPair(address pair_) internal returns (bool) {
        (bool success, bytes memory data) = pair_.call(
            (abi.encodeWithSelector(FACTORY_SELECTOR))
        );
        return success && data.length > 0;
    }

    function _createPair(address router_, address pairedToken_)
    internal
    returns (address)
    {
        return
        IUniswapV2Factory(IUniswapV2Router02(router_).factory()).createPair(
            address(this),
            pairedToken_
        );
    }
}
