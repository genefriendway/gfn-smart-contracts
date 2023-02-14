import pytest
import brownie
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__set_reserve_percent_for_community_campaign(advocate_deployment):
    # Arrange
    configuration_owner = advocate_deployment['advocate_reward_configuration_owner']
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']
    percent = 20

    # Action
    tx = configuration_contract.setReservePercentForCommunityCampaign(
        percent,
        {"from": configuration_owner}
    )
    # Assert: SetReservePercentForCommunityCampaign Event
    assert ('SetReservePercentForCommunityCampaign' in tx.events) is True
    assert tx.events['SetReservePercentForCommunityCampaign']['percent'] \
           == percent

    # Assert
    assert configuration_contract.getReservePercentForCommunityCampaign() \
           == percent


def test_failure__set_reserve_percent_for_community_campaign__invalid_owner_make_txn(
        advocate_deployment
):
    # Arrange
    configuration_contract = advocate_deployment['advocate_reward_configuration_contract']
    another_owner = accounts.add()
    percent = 20

    # Action
    with brownie.reverts("Ownable: caller is not the owner"):
        configuration_contract.setReservePercentForCommunityCampaign(
            percent,
            {"from": another_owner}
        )
