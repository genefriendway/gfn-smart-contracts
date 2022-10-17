import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_budget_address_to_reward(pcsp_deployment):
    # Arrange
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    budget_address_to_reward = accounts.add()

    # Action
    tx = pcsp_configuration_contract.setBudgetAddressToReward(
        budget_address_to_reward,
        {"from": pcsp_configuration_owner}
    )
    # Assert: SetBudgetAddressToReward Event
    assert ('SetBudgetAddressToReward' in tx.events) is True
    assert tx.events['SetBudgetAddressToReward']['budgetAddress'] \
           == budget_address_to_reward

    # Assert
    assert pcsp_configuration_contract.getBudgetAddressToReward() \
           == budget_address_to_reward


def test_failure__set_budget_address_to_reward__invalid_owner_make_txn(
        pcsp_deployment
):
    # Arrange
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    another_owner = accounts.add()
    budget_address_to_reward = accounts.add()

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        pcsp_configuration_contract.setBudgetAddressToReward(
            budget_address_to_reward,
            {"from": another_owner}
        )


def test_failure__set_budget_address_to_reward__budget_address_null(
        pcsp_deployment
):
    # Arrange
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    budget_address_to_reward = "0x0000000000000000000000000000000000000000"

    # Action
    with brownie.reverts("PCSPCustomerRewardConfiguration: address must not be null"):
        pcsp_configuration_contract.setBudgetAddressToReward(
            budget_address_to_reward,
            {"from": pcsp_configuration_owner}
        )


def test_failure__set_budget_address_to_reward__budget_address_same_current_value(
        pcsp_deployment
):
    # Arrange
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    budget_address_to_reward = accounts.add()

    # Action
    pcsp_configuration_contract.setBudgetAddressToReward(
        budget_address_to_reward,
        {"from": pcsp_configuration_owner}
    )

    # Assert
    assert pcsp_configuration_contract.getBudgetAddressToReward() \
           == budget_address_to_reward

    with brownie.reverts("PCSPCustomerRewardConfiguration: address must "
                         "differ from current value"):
        pcsp_configuration_contract.setBudgetAddressToReward(
            budget_address_to_reward,
            {"from": pcsp_configuration_owner}
        )