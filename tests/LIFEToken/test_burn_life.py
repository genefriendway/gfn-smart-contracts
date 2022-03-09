import brownie
import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


@pytest.fixture(scope="function")
def setup(deployment, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    gfn_owner2 = deployment[const.GFN_OWNER2]
    gfn_operator = deployment[const.GFN_OPERATOR]
    gnft_token = deployment[const.GNFT_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]
    life_token = deployment[const.LIFE_TOKEN]

    genetic_owner1 = accounts[3]
    genetic_owner2 = accounts[4]

    # mint LIFE to Treasury
    gnft_token.mintBatchGNFT([genetic_owner1], [12345678], True, {"from": gfn_operator})

    # Actions
    # gfn_owner1 make a transaction to transfer 5000 LIFE to genetic_owner2
    calldata = life_token.transfer.encode_input(genetic_owner2.address,
                                                5000e+18)
    tx = life_treasury.submitTransaction(
        life_token.address, 0, calldata, {"from": gfn_owner1}
    )
    transaction_id = tx.events['SubmitTransaction']['transactionId']

    # gnf_owner2 confirm the transaction that gfn_owner1 made
    life_treasury.confirmTransaction(transaction_id, {"from": gfn_owner2})

    # Assert: check balances after transferring to GFN Wallet
    assert life_token.totalSupply() == 90000000e+18
    assert life_token.balanceOf(life_treasury.address) == 89995000e+18
    assert life_token.balanceOf(genetic_owner1.address) == 0
    assert life_token.balanceOf(genetic_owner2.address) == 5000e+18

    return {
        "genetic_owner1": genetic_owner1,
        "genetic_owner2": genetic_owner2,
    }


def test_success__burn_life_token__has_balance_and_enough(setup, deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_owner2 = setup['genetic_owner2']

    # Actions
    tx = life_token.burnLIFE(20e+18, {"from": genetic_owner2})

    # Assert: BurnGNFT Event
    assert ('BurnLIFE' in tx.events) is True
    assert tx.events['BurnLIFE']['account'] == genetic_owner2.address
    assert tx.events['BurnLIFE']['amount'] == 20e+18

    # Assert: Approval Event
    assert ('Transfer' in tx.events) is True
    assert tx.events['Transfer']['from'] == genetic_owner2
    assert tx.events['Transfer']['to'] == "0x0000000000000000000000000000000000000000"
    assert tx.events['Transfer']['value'] == 20e+18

    # Assert: check balances actions
    assert life_token.totalSupply() == 89999980e+18
    assert life_token.balanceOf(life_treasury.address) == 89995000e+18
    assert life_token.balanceOf(genetic_owner2.address) == 4980e+18


def test_failure__burn_life_token__has_balance_but_not_enough(setup, deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    genetic_owner2 = setup['genetic_owner2']

    # Assert: before actions
    assert life_token.totalSupply() == 90000000e+18
    assert life_token.balanceOf(life_treasury.address) == 89995000e+18
    assert life_token.balanceOf(genetic_owner2.address) == 5000e+18

    # Actions
    with brownie.reverts("ERC20: burn amount exceeds balance"):
        life_token.burnLIFE(5001e+18, {"from": genetic_owner2})

    # Assert: check balances actions
    assert life_token.totalSupply() == 90000000e+18
    assert life_token.balanceOf(life_treasury.address) == 89995000e+18
    assert life_token.balanceOf(genetic_owner2.address) == 5000e+18


def test_failure__burn_life_token__no_balance(setup, deployment, const):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    life_treasury = deployment[const.LIFE_TREASURY]

    # asserts before actions
    assert life_token.totalSupply() == 90000000e+18
    assert life_token.balanceOf(life_treasury.address) == 89995000e+18
    assert life_token.balanceOf(gfn_operator.address) == 0

    # Actions
    with brownie.reverts("ERC20: burn amount exceeds balance"):
        life_token.burnLIFE(5001e+18, {"from": gfn_operator})

    # Assert: check balances actions
    assert life_token.totalSupply() == 90000000e+18
    assert life_token.balanceOf(life_treasury.address) == 89995000e+18
    assert life_token.balanceOf(gfn_operator.address) == 0
