import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__transfer_internally(deployment, initial_life_treasury, const):
    # Arranges
    gfn_owner1 = deployment[const.GFN_OWNER1]
    life_treasury = deployment[const.LIFE_TREASURY]
    life_token = deployment[const.LIFE_TOKEN]
    gpo_wallet = deployment[const.GENETIC_PROFILE_OWNER_WALLET]
    genetic_owner2 = accounts[4]
    genetic_owner3 = accounts[5]

    # Asserts before transferring internally
    assert life_token.balanceOf(gpo_wallet) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner3) == 0

    gpo_wallet.transferInternally(
        genetic_owner2, genetic_owner3, 3e+18, {"from": gfn_owner1}
    )

    # Asserts after transferring internally
    assert life_token.balanceOf(gpo_wallet.address) == 24e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner2) == 21e+18
    assert gpo_wallet.getBalanceOfParticipant(genetic_owner3) == 3e+18
