add_avax_fuji:
	brownie networks add GeneFriendNetwork avax-fuji host=https://api.avax-test.network/ext/bc/C/rpc chainid=43113 explorer=https://api-testnet.snowtrace.io/api

add_avax_mainnet:
	brownie networks add GeneFriendNetwork avax-mainnet host=https://api.avax.network/ext/bc/C/rpc chainid=43114 explorer=https://api.snowtrace.io/api

add_oasis_testnet:
	brownie networks add GeneFriendNetwork oasis-testnet host=https://testnet.emerald.oasis.dev chainid=42261 explorer=http://testnet.explorer.emerald.oasis.dev/api