import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__transfer_internally__amount_less_than_balance_of_sender(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring internally
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner3) == 0

    # Actions
    gpo_wallet.transferInternally(
        genetic_owner2, genetic_owner3, 3e+18, {"from": gfn_owner1}
    )

    # Asserts after transferring internally
    assert life_token.balanceOf(gpo_wallet.address) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 21e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner3) == 3e+18


def test_success__transfer_internally__amount_equal_to_balance_of_sender(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring internally
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner3) == 0

    # Actions
    gpo_wallet.transferInternally(
        genetic_owner2, genetic_owner3, 24e+18, {"from": gfn_owner1}
    )

    # Asserts after transferring internally
    assert life_token.balanceOf(gpo_wallet.address) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner3) == 24e+18


def test_failure__transfer_internally__not_gfn_owner_make_transaction(
        deployment, initial_life_treasury, const
):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring internally
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner3) == 0

    # Actions
    with brownie.reverts("ParticipantWallet: caller is not the owner or registered contract"):
        gpo_wallet.transferInternally(
            genetic_owner2, genetic_owner3, 25e+18, {"from": genetic_owner3}
        )

    # Asserts after transferring internally
    assert life_token.balanceOf(gpo_wallet.address) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner3) == 0


def test_failure__transfer_internally__amount_greater_than_balance_of_sender(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring internally
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner3) == 0

    # Actions
    with brownie.reverts("ParticipantWallet: sender has not enough amount to send internally"):
        gpo_wallet.transferInternally(
            genetic_owner2, genetic_owner3, 25e+18, {"from": gfn_owner1}
        )

    # Asserts after transferring internally
    assert life_token.balanceOf(gpo_wallet.address) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner3) == 0
