import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_token_wallet_address(advocate_deployment):
    # Arrange
    advocate_reward_configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    advocate_reward_configuration_contract = advocate_deployment['advocate_reward_configuration_contract']
    new_advocate_reward_wallet_address = accounts.add()

    # Action
    tx = advocate_reward_configuration_contract.setTokenWalletAddress(
        new_advocate_reward_wallet_address,
        {"from": advocate_reward_configuration_owner}
    )
    # Assert: SetTokenWalletAddress Event
    assert ('SetTokenWalletAddress' in tx.events) is True
    assert tx.events['SetTokenWalletAddress']['tokenWalletAddress'] \
           == new_advocate_reward_wallet_address

    # Assert
    assert advocate_reward_configuration_contract.getTokenWalletAddress() \
           == new_advocate_reward_wallet_address


def test_failure__set_token_wallet_address__invalid_owner_make_txn(
        advocate_deployment
):
    # Arrange
    advocate_reward_configuration_contract = advocate_deployment['advocate_reward_configuration_contract']
    another_owner = accounts.add()
    new_advocate_reward_wallet_address = accounts.add()

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        advocate_reward_configuration_contract.setTokenWalletAddress(
            new_advocate_reward_wallet_address,
            {"from": another_owner}
        )
