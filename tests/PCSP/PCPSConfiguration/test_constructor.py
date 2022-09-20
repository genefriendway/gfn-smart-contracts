#!/usr/bin/python3
import pytest
import brownie
from brownie import accounts, PCSPConfiguration


def test_success__deploy_smart_contract():
    deployer = accounts[0]
    pcsp_configuration_owner = accounts[1]

    # Actions
    pcsp_configuration_contract = PCSPConfiguration.deploy(
        pcsp_configuration_owner,
        {"from": deployer}
    )

    # Assert Customer Reward Percents
    assert pcsp_configuration_contract.getCustomerRewardPercent(1) == 1000
    assert pcsp_configuration_contract.getCustomerRewardPercent(3) == 200
    assert pcsp_configuration_contract.getCustomerRewardPercent(16) == 15
    assert pcsp_configuration_contract.getCustomerRewardPercent(80) == 2

    assert pcsp_configuration_contract.checkActiveRiskOfGettingStroke(1) is True
    assert pcsp_configuration_contract.checkActiveRiskOfGettingStroke(3) is True
    assert pcsp_configuration_contract.checkActiveRiskOfGettingStroke(16) is True
    assert pcsp_configuration_contract.checkActiveRiskOfGettingStroke(80) is True

    assert pcsp_configuration_contract.checkActiveRiskOfGettingStroke(0) is False
    assert pcsp_configuration_contract.checkActiveRiskOfGettingStroke(2) is False
    assert pcsp_configuration_contract.checkActiveRiskOfGettingStroke(5) is False
    assert pcsp_configuration_contract.checkActiveRiskOfGettingStroke(66) is False
    assert pcsp_configuration_contract.checkActiveRiskOfGettingStroke(81) is False


def test_failure__deploy_smart_contract__null_owner():
    deployer = accounts[0]
    pcsp_configuration_owner = "0x0000000000000000000000000000000000000000"

    # Actions
    with brownie.reverts("Ownable: new owner is the zero address"):
        PCSPConfiguration.deploy(
            pcsp_configuration_owner,
            {"from": deployer}
        )


def test_failure__deploy_smart_contract__owner_is_not_adddress_type():
    deployer = accounts[0]
    pcsp_configuration_owner = "Hello_Address"

    # Actions
    with pytest.raises(ValueError):
        PCSPConfiguration.deploy(
            pcsp_configuration_owner,
            {"from": deployer}
        )
