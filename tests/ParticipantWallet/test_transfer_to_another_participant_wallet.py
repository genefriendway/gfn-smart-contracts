import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__transfer_to_another_participant_wallet__amount_less_than_balance_of_sender(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    du_wallet = deployment[const.DATA_UTILIZER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring to another participant wallet
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(du_wallet) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert du_wallet.getBalanceOfParticipant(genetic_owner3) == 0

    # Action: transfer LIFE to another participant wallet
    gpo_wallet.transferToAnotherParticipantWallet(
        genetic_owner2, du_wallet, genetic_owner3, 5e+18, {"from": gfn_operator}
    )

    # Asserts after transferring
    assert life_token.balanceOf(gpo_wallet.address) == 19e+18
    assert life_token.balanceOf(du_wallet.address) == 5e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 19e+18
    assert du_wallet.getBalanceOfParticipant(genetic_owner3) == 5e+18


def test_success__transfer_to_another_participant_wallet__amount_equal_to_balance_of_sender(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    du_wallet = deployment[const.DATA_UTILIZER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(du_wallet) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert du_wallet.getBalanceOfParticipant(genetic_owner3) == 0

    # Action: transfer LIFE to another participant wallet
    gpo_wallet.transferToAnotherParticipantWallet(
        genetic_owner2, du_wallet, genetic_owner3, 24e+18, {"from": gfn_operator}
    )

    # Asserts after transferring
    assert life_token.balanceOf(gpo_wallet.address) == 0
    assert life_token.balanceOf(du_wallet.address) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 0
    assert du_wallet.getBalanceOfParticipant(genetic_owner3) == 24e+18


def test_failure__transfer_to_another_participant_wallet__not_gfn_owner_make_transaction(
        deployment, initial_life_treasury, const
):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    du_wallet = deployment[const.DATA_UTILIZER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(du_wallet) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert du_wallet.getBalanceOfParticipant(genetic_owner3) == 0

    # Action: transfer LIFE to another participant wallet
    with brownie.reverts("ParticipantWallet: caller is not the owner or registered contract"):
        gpo_wallet.transferToAnotherParticipantWallet(
            genetic_owner2, du_wallet, genetic_owner3, 24e+18, {"from": genetic_owner3}
        )

    # Asserts after transferring
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(du_wallet) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert du_wallet.getBalanceOfParticipant(genetic_owner3) == 0


def test_failure__transfer_to_another_participant_wallet__amount_greater_than_balance_of_sender(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    du_wallet = deployment[const.DATA_UTILIZER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring internally
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(du_wallet) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert du_wallet.getBalanceOfParticipant(genetic_owner3) == 0

    # Action: transfer LIFE to another participant wallet
    with brownie.reverts("ParticipantWallet: sender has not enough amount to "
                         "send to another participant wallet"):
        gpo_wallet.transferToAnotherParticipantWallet(
            genetic_owner2, du_wallet, genetic_owner3, 25e+18, {"from": gfn_operator}
        )

    # Asserts after transferring
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(du_wallet) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert du_wallet.getBalanceOfParticipant(genetic_owner3) == 0
