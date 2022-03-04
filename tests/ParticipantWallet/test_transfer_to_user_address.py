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
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring to GFN Wallet
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(genetic_owner3) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18

    # Action: transfer LIFE to GFN wallet
    gpo_wallet.transferExternally(
        genetic_owner2, genetic_owner3, 5e+18, {"from": gfn_operator}
    )

    # Asserts after transferring
    assert life_token.balanceOf(gpo_wallet.address) == 19e+18
    assert life_token.balanceOf(genetic_owner3.address) == 5e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 19e+18


def test_success__transfer_to_user_address__amount_equal_to_balance_of_sender(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring to GFN Wallet
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(genetic_owner3) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18

    # Action: transfer LIFE to GFN wallet
    gpo_wallet.transferExternally(
        genetic_owner2, genetic_owner3, 24e+18, {"from": gfn_operator}
    )

    # Asserts after transferring
    assert life_token.balanceOf(gpo_wallet.address) == 0
    assert life_token.balanceOf(genetic_owner3.address) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 0


def test_success__transfer_to_user_address__user_withdrawal_to_your_own_wallet(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    genetic_owner2 = accounts[4]

    # Asserts before transferring to GFN Wallet
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(genetic_owner2) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18

    # Action: transfer LIFE to GFN wallet
    gpo_wallet.transferExternally(
        genetic_owner2, genetic_owner2, 22e+18, {"from": gfn_operator}
    )

    # Asserts after transferring
    assert life_token.balanceOf(gpo_wallet.address) == 2e+18
    assert life_token.balanceOf(genetic_owner2.address) == 22e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 2e+18


def test_failure__transfer_to_user_address__not_gfn_owner_make_transaction(
        deployment, initial_life_treasury, const
):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring to GFN Wallet
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(genetic_owner3) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18

    # Action: transfer LIFE to another participant wallet
    with brownie.reverts("ParticipantWallet: caller is not the owner or registered contract"):
        gpo_wallet.transferExternally(
            genetic_owner2, genetic_owner3, 24e+18, {"from": genetic_owner2}
        )

    # Asserts after transferring
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(genetic_owner3) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18


def test_failure__transfer_to_user_address__amount_greater_than_balance_of_sender(
        deployment, initial_life_treasury, const
):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring to GFN Wallet
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(genetic_owner3) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18

    # Action: transfer LIFE to another participant wallet
    with brownie.reverts("ParticipantWallet: sender has not enough amount "
                         "to send to GFN wallet"):
        gpo_wallet.transferExternally(
            genetic_owner2, genetic_owner3, 30e+18, {"from": gfn_operator}
        )

    # Asserts after transferring
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert life_token.balanceOf(genetic_owner3) == 0
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
