#!/usr/bin/python3
import pytest
import brownie
from brownie import accounts, AdvocateRewardConfiguration


def test_success__deploy_smart_contract():
    deployer = accounts[0]
    configuration_owner = accounts[1]

    # Actions
    configuration = AdvocateRewardConfiguration.deploy(
        configuration_owner,
        {"from": deployer}
    )

    level = 1
    assert configuration.getAdvocateMinReferral(level) == 1
    assert configuration.getAdvocateMaxReferral(level) == 99
    assert configuration.getAdvocateRewardPercent(level) == 20
    assert configuration.getAdvocateLevelStatus(level) is True

    level = 2
    assert configuration.getAdvocateMinReferral(level) == 100
    assert configuration.getAdvocateMaxReferral(level) == 199
    assert configuration.getAdvocateRewardPercent(level) == 30
    assert configuration.getAdvocateLevelStatus(level) is True

    level = 3
    assert configuration.getAdvocateMinReferral(level) == 200
    assert configuration.getAdvocateMaxReferral(level) == 299
    assert configuration.getAdvocateRewardPercent(level) == 40
    assert configuration.getAdvocateLevelStatus(level) is True

    level = 4
    assert configuration.getAdvocateMinReferral(level) == 300
    assert configuration.getAdvocateMaxReferral(level) == 99999999
    assert configuration.getAdvocateRewardPercent(level) == 50
    assert configuration.getAdvocateLevelStatus(level) is True
    
    assert configuration.getReservePercentForCustomerReward() == 20
    assert configuration.getReservePercentForPlatformFee() == 15
    assert configuration.getReservePercentForCommunityCampaign() == 10
    assert configuration.getReservePercentForQuarterReferralReward() == 5
    assert configuration.getReservePercentForAdvocateReward() == 50


def test_failure__deploy_smart_contract__null_owner():
    deployer = accounts[0]
    configuration_owner = "0x0000000000000000000000000000000000000000"

    # Actions
    with brownie.reverts("Ownable: new owner is the zero address"):
        AdvocateRewardConfiguration.deploy(
            configuration_owner,
            {"from": deployer}
        )


def test_failure__deploy_smart_contract__owner_is_not_adddress_type():
    deployer = accounts[0]
    configuration_owner = "Hello_Address"

    # Actions
    with pytest.raises(ValueError):
        AdvocateRewardConfiguration.deploy(
            configuration_owner,
            {"from": deployer}
        )
