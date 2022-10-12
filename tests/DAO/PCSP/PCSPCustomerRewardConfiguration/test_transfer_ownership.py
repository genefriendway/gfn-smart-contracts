import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__transfer_ownership__right_owner_make_txn(pcsp_deployment):
    # Arrange
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_owner = accounts.add()

    # Assert before Actions
    assert pcsp_configuration_contract.owner() == pcsp_configuration_owner

    # Action
    pcsp_configuration_contract.transferOwnership(
        new_owner,
        {"from": pcsp_configuration_owner}
    )

    # Assert
    assert pcsp_configuration_contract.owner() == new_owner


def test_failure__transfer_ownership__invalid_owner_make_txn(pcsp_deployment):
    # Arrange
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    another_owner1 = accounts.add()
    another_owner2 = accounts.add()

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        pcsp_configuration_contract.transferOwnership(
            another_owner2,
            {"from": another_owner1}
        )

    assert pcsp_configuration_contract.owner() == pcsp_configuration_owner