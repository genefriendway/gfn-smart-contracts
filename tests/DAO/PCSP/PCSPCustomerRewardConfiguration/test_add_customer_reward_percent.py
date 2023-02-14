import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__add_customer_reward_percent__owner_make_txn(pcsp_deployment):
    # Arrange
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_risk_value = 50
    new_reward_percent = 300

    # Assert before actions
    with brownie.reverts("PCSPCustomerRewardConfiguration: risk of getting "
                         "stroke is inactive"):
        pcsp_configuration_contract.getCustomerRewardPercent(new_risk_value)

    is_active_risk = pcsp_configuration_contract.checkActiveRiskOfGettingStroke(
        new_risk_value
    )
    assert is_active_risk is False

    # Action
    tx = pcsp_configuration_contract.addCustomerRewardPercent(
        new_risk_value,
        new_reward_percent,
        {"from": pcsp_configuration_owner}
    )
    # Assert: AddCustomerRewardPercent Event
    assert ('AddCustomerRewardPercent' in tx.events) is True
    assert tx.events['AddCustomerRewardPercent']['riskOfGettingStroke'] == new_risk_value
    assert tx.events['AddCustomerRewardPercent']['rewardPercent'] == new_reward_percent

    # Assert:
    return_reward_percent = pcsp_configuration_contract.getCustomerRewardPercent(new_risk_value)
    is_active_risk = pcsp_configuration_contract.checkActiveRiskOfGettingStroke(new_risk_value)
    assert return_reward_percent == new_reward_percent
    assert is_active_risk is True


def test_failure__add_customer_reward_percent__invalid_owner_make_txn(pcsp_deployment):
    # Arrange
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_risk_value = 50
    new_reward_percent = 300
    another_owner = accounts.add()

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        pcsp_configuration_contract.addCustomerRewardPercent(
            new_risk_value,
            new_reward_percent,
            {"from": another_owner}
        )


def test_failure__add_customer_reward_percent__risk_is_negative(pcsp_deployment):
    # Arrange
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_risk_value = -10
    new_reward_percent = 300

    # Action
    with pytest.raises(OverflowError):
        pcsp_configuration_contract.addCustomerRewardPercent(
            new_risk_value,
            new_reward_percent,
            {"from": pcsp_configuration_owner}
        )


def test_failure__add_customer_reward_percent__risk_is_zero(pcsp_deployment):
    # Arrange
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_risk_value = 0
    new_reward_percent = 300

    # Action
    with brownie.reverts("PCSPCustomerRewardConfiguration: risk of getting stroke must be greater than zero"):
        pcsp_configuration_contract.addCustomerRewardPercent(
            new_risk_value,
            new_reward_percent,
            {"from": pcsp_configuration_owner}
        )


def test_failure__add_customer_reward_percent__risk_over_100(pcsp_deployment):
    # Arrange
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_risk_value = 101
    new_reward_percent = 300

    # Action
    with brownie.reverts("PCSPCustomerRewardConfiguration: risk of getting stroke must be equal to or less than 100"):
        pcsp_configuration_contract.addCustomerRewardPercent(
            new_risk_value,
            new_reward_percent,
            {"from": pcsp_configuration_owner}
        )


def test_failure__add_customer_reward_percent__reward_percent_is_negative(pcsp_deployment):
    # Arrange
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_risk_value = 50
    new_reward_percent = -400

    # Action
    with pytest.raises(OverflowError):
        pcsp_configuration_contract.addCustomerRewardPercent(
            new_risk_value,
            new_reward_percent,
            {"from": pcsp_configuration_owner}
        )


def test_failure__add_customer_reward_percent__reward_percent_is_zero(pcsp_deployment):
    # Arrange
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    new_risk_value = 50
    new_reward_percent = 0

    # Action
    with brownie.reverts("PCSPCustomerRewardConfiguration: reward percent must be greater than zero"):
        pcsp_configuration_contract.addCustomerRewardPercent(
            new_risk_value,
            new_reward_percent,
            {"from": pcsp_configuration_owner}
        )
