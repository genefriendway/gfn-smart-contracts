import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__transfer_to_user_address(deployment, initial_life_treasury, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    receiver = accounts[5]

    # Assert before transfer LIFE Token from GFN-Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6666e+18
    assert life_token.balanceOf(receiver) == 0

    # Actions: Transfer LIFE Token from GFN-Wallet to Receiver
    gfn_wallet.transfer(receiver, 333e+18, {"from": gfn_owner1})

    # Assert before transfer LIFE Token from GFN-Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6333e+18
    assert life_token.balanceOf(receiver) == 333e+18
