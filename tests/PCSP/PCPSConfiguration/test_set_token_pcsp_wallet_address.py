import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_pcsp_wallet_address(pcsp_deployment):
    # Arrange
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_pcsp_wallet_address = accounts.add()

    # Action
    tx = pcsp_configuration_contract.setTokenPCSPWalletAddress(
        new_pcsp_wallet_address,
        {"from": pcsp_configuration_owner}
    )
    # Assert: SetTokenPCSPWalletAddress Event
    assert ('SetTokenPCSPWalletAddress' in tx.events) is True
    assert tx.events['SetTokenPCSPWalletAddress']['tokenPCSPWalletAddress'] == new_pcsp_wallet_address

    # Assert
    assert pcsp_configuration_contract.getTokenPCSPWalletAddress() == new_pcsp_wallet_address


def test_failure__set_pcsp_wallet_address__invalid_owner_make_txn(pcsp_deployment):
    # Arrange
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    another_owner = accounts.add()
    new_pcsp_wallet_address = accounts.add()

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        pcsp_configuration_contract.setTokenPCSPWalletAddress(
            new_pcsp_wallet_address,
            {"from": another_owner}
        )
