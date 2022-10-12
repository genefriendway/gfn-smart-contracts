import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_token_wallet_address(pcsp_deployment):
    # Arrange
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_pcsp_wallet_address = accounts.add()

    # Action
    tx = pcsp_configuration_contract.setTokenWalletAddress(
        new_pcsp_wallet_address,
        {"from": pcsp_configuration_owner}
    )
    # Assert: SetTokenWalletAddress Event
    assert ('SetTokenWalletAddress' in tx.events) is True
    assert tx.events['SetTokenWalletAddress']['tokenWalletAddress'] \
           == new_pcsp_wallet_address

    # Assert
    assert pcsp_configuration_contract.getTokenWalletAddress() \
           == new_pcsp_wallet_address


def test_failure__set_token_wallet_address__invalid_owner_make_txn(
        pcsp_deployment
):
    # Arrange
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    another_owner = accounts.add()
    new_pcsp_wallet_address = accounts.add()

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        pcsp_configuration_contract.setGeneNFTAddress(
            new_pcsp_wallet_address,
            {"from": another_owner}
        )
