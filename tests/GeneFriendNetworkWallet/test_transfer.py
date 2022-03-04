import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__transfer_to_user_address__amount_less_than_balance_of_sender(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    receiver = accounts[5]

    # Assert before transfer LIFE Token from GFN-Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6666e+18
    assert life_token.balanceOf(receiver) == 0

    # Actions: Transfer LIFE Token from GFN-Wallet to Receiver
    gfn_wallet.transfer(receiver, 333e+18, {"from": gfn_operator})

    # Assert before transfer LIFE Token from GFN-Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6333e+18
    assert life_token.balanceOf(receiver) == 333e+18


def test_success__transfer_to_another_gfn_wallet__amount_less_than_balance_of_sender(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    gfn_sale_wallet = deployment[const.GFN_SALE_WALLET]

    # Assert before transfer LIFE Token from GFN-Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6666e+18
    assert life_token.balanceOf(gfn_sale_wallet) == 0

    # Actions: Transfer LIFE Token from GFN-Wallet to Receiver
    gfn_wallet.transfer(gfn_sale_wallet, 22e+18, {"from": gfn_operator})

    # Assert before transfer LIFE Token from GFN-Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6644e+18
    assert life_token.balanceOf(gfn_sale_wallet.address) == 22e+18


def test_success__transfer_to_another_gfn_wallet__amount_equal_to_balance_of_sender(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    gfn_sale_wallet = deployment[const.GFN_SALE_WALLET]

    # Assert before transfer LIFE Token from GFN-Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6666e+18
    assert life_token.balanceOf(gfn_sale_wallet) == 0

    # Actions: Transfer LIFE Token from GFN-Wallet to Receiver
    gfn_wallet.transfer(gfn_sale_wallet, 6666e+18, {"from": gfn_operator})

    # Assert after transfer LIFE Token from GFN-Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 0
    assert life_token.balanceOf(gfn_sale_wallet.address) == 6666e+18


def test_success__transfer_to_another_gfn_wallet__not_gfn_owner_make_transaction(
        deployment, initial_life_treasury, const
):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    gfn_sale_wallet = deployment[const.GFN_SALE_WALLET]

    # Assert before transfer LIFE Token from GFN-Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6666e+18
    assert life_token.balanceOf(gfn_sale_wallet) == 0

    # Actions
    with brownie.reverts("AccessibleRegistry: caller must be GFN Operator"):
        gfn_wallet.transfer(gfn_sale_wallet, 6666e+18, {"from": accounts[3]})

    # Assert after transfer LIFE Token from GFN-Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6666e+18
    assert life_token.balanceOf(gfn_sale_wallet) == 0


def test_success__transfer_to_another_gfn_wallet__amount_greater_than_balance_of_wallet(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gfn_wallet = deployment[const.GENE_FRIEND_NETWORK_WALLET]
    gfn_sale_wallet = deployment[const.GFN_SALE_WALLET]

    # Assert before transfer LIFE Token from GFN-Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6666e+18
    assert life_token.balanceOf(gfn_sale_wallet) == 0

    # Actions
    with brownie.reverts("GeneFriendNetWorkWallet: Wallet has not enough amount to transfer"):
        gfn_wallet.transfer(gfn_sale_wallet, 6667e+18, {"from": gfn_operator})

    # Assert after transfer LIFE Token from GFN-Wallet
    assert life_token.balanceOf(gfn_wallet.address) == 6666e+18
    assert life_token.balanceOf(gfn_sale_wallet) == 0
