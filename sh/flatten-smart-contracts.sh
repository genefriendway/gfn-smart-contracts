echo "Flattening ContractRegistry"
npx hardhat flatten contracts/ContractRegistry.sol > flatten/flatten.ContractRegistry.sol
echo "Removing duplicated SPDX-License-Identifier: MIT"
sed -i 's/\/\/ SPDX-License-Identifier: MIT//g' flatten/flatten.ContractRegistry.sol
sed -i '5 i \/\/ SPDX-License-Identifier: MIT' flatten/flatten.ContractRegistry.sol
echo "------------------------------------------------"

echo "Flattening Configuration"
npx hardhat flatten contracts/Configuration.sol > flatten/flatten.Configuration.sol
echo "Removing duplicated SPDX-License-Identifier: MIT"
sed -i 's/\/\/ SPDX-License-Identifier: MIT//g' flatten/flatten.Configuration.sol
sed -i '5 i \/\/ SPDX-License-Identifier: MIT' flatten/flatten.Configuration.sol
echo "------------------------------------------------"

echo "Flattening GNFTToken"
npx hardhat flatten contracts/GNFTToken.sol > flatten/flatten.GNFTToken.sol
echo "Removing duplicated SPDX-License-Identifier: MIT"
sed -i 's/\/\/ SPDX-License-Identifier: MIT//g' flatten/flatten.GNFTToken.sol
sed -i '5 i \/\/ SPDX-License-Identifier: MIT' flatten/flatten.GNFTToken.sol
echo "------------------------------------------------"

echo "Flattening LIFEToken"
npx hardhat flatten contracts/LIFEToken.sol > flatten/flatten.LIFEToken.sol
echo "Removing duplicated SPDX-License-Identifier: MIT"
sed -i 's/\/\/ SPDX-License-Identifier: MIT//g' flatten/flatten.LIFEToken.sol
sed -i '5 i \/\/ SPDX-License-Identifier: MIT' flatten/flatten.LIFEToken.sol
echo "------------------------------------------------"

echo "Flattening GeneFriendNetworkWallet"
npx hardhat flatten contracts/GeneFriendNetworkWallet.sol > flatten/flatten.GeneFriendNetworkWallet.sol
echo "Removing duplicated SPDX-License-Identifier: MIT"
sed -i 's/\/\/ SPDX-License-Identifier: MIT//g' flatten/flatten.GeneFriendNetworkWallet.sol
sed -i '5 i \/\/ SPDX-License-Identifier: MIT' flatten/flatten.GeneFriendNetworkWallet.sol
echo "------------------------------------------------"

echo "Flattening GenomicDAOToken"
npx hardhat flatten contracts/dao/GenomicDAOToken.sol > flatten/flatten.GenomicDAOToken.sol
echo "Removing duplicated SPDX-License-Identifier: MIT"
sed -i 's/\/\/ SPDX-License-Identifier: MIT//g' flatten/flatten.GenomicDAOToken.sol
sed -i '5 i \/\/ SPDX-License-Identifier: MIT' flatten/flatten.GenomicDAOToken.sol
echo "------------------------------------------------"