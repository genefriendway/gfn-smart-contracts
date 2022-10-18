#!/usr/bin/python3
import pytest
import brownie
from brownie import accounts, AdvocateReward


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


@pytest.fixture
def data_test(advocate_deployment):
    token_wallet = advocate_deployment['token_wallet_contract']
    token_wallet_owner = advocate_deployment['token_wallet_owner']
    advocate_reward_contract = advocate_deployment['advocate_reward_contract']
    config = advocate_deployment['advocate_reward_configuration_contract']
    config_owner = advocate_deployment['advocate_reward_configuration_owner']

    customer_reward_address = accounts.add()
    platform_fee_address = accounts.add()
    community_campaign_address = accounts.add()
    quarter_referral_reward_address = accounts.add()
    advocate_reward_address = accounts.add()

    # configure Token Wallet Address
    config.setTokenWalletAddress(token_wallet, {"from": config_owner})

    # Configure Reserved Addresses
    config.setReserveAddressForCustomerReward(
        customer_reward_address, {"from": config_owner}
    )
    config.setReserveAddressForPlatformFee(
        platform_fee_address, {"from": config_owner}
    )
    config.setReserveAddressForCommunityCampaign(
        community_campaign_address, {"from": config_owner}
    )
    config.setReserveAddressForQuarterReferralReward(
        quarter_referral_reward_address, {"from": config_owner}
    )
    config.setReserveAddressForAdvocateReward(
        advocate_reward_address, {"from": config_owner}
    )

    assert config.getTokenWalletAddress() == token_wallet
    assert config.getReserveAddressForCustomerReward() == customer_reward_address
    assert config.getReserveAddressForPlatformFee() == platform_fee_address
    assert config.getReserveAddressForCommunityCampaign() == community_campaign_address
    assert config.getReserveAddressForQuarterReferralReward() == quarter_referral_reward_address
    assert config.getReserveAddressForAdvocateReward() == advocate_reward_address

    # add Operator to Token Wallet
    token_wallet.addOperator(
        advocate_reward_contract, {"from": token_wallet_owner}
    )

    assert token_wallet.checkActiveOperator(advocate_reward_contract) is True

    return {
        "customer_reward_address": customer_reward_address,
        "platform_fee_address": platform_fee_address,
        "community_campaign_address": community_campaign_address,
        "quarter_referral_reward_address": quarter_referral_reward_address,
        "advocate_reward_address": advocate_reward_address,
    }


def test_success__reward_advocates_quarterly__owner_make_txn(
        advocate_deployment, data_test
):
    # Arranges
    token_wallet = advocate_deployment['token_wallet_contract']
    token_wallet_owner = advocate_deployment['token_wallet_owner']
    advocate_reward_owner = advocate_deployment['advocate_reward_owner']
    advocate_reward_contract = advocate_deployment['advocate_reward_contract']

    quarter_referral_reward_address = data_test['quarter_referral_reward_address']

    token_wallet.deposit(
        quarter_referral_reward_address,
        800 * 10 ** 18,
        "Deposit",
        {"from": token_wallet_owner}
    )

    advocate1 = accounts.add()
    advocate2 = accounts.add()
    
    reward_amount1 = 500 * 10 ** 18
    reward_amount2 = 150 * 10 ** 18

    # Assert Before Actions
    assert token_wallet.getTotalBalance() == 800 * 10 ** 18
    assert token_wallet.getBalance(quarter_referral_reward_address) == 800 * 10 ** 18
    assert token_wallet.getBalance(advocate1) == 0
    assert token_wallet.getBalance(advocate2) == 0

    # Actions
    txn = advocate_reward_contract.rewardAdvocatesQuarterly(
        [advocate1, advocate2], 
        [reward_amount1, reward_amount2], 
        {"from": advocate_reward_owner}
    )

    # Assert: RewardAdvocateQuarterly Event
    assert ('RewardAdvocateQuarterly' in txn.events) is True
    assert txn.events['RewardAdvocateQuarterly'][0]['advocateAddress'] == advocate1
    assert txn.events['RewardAdvocateQuarterly'][0]['rewardAmount'] == reward_amount1

    assert txn.events['RewardAdvocateQuarterly'][1]['advocateAddress'] == advocate2
    assert txn.events['RewardAdvocateQuarterly'][1]['rewardAmount'] == reward_amount2

    assert token_wallet.getTotalBalance() == 800 * 10 ** 18
    assert token_wallet.getBalance(quarter_referral_reward_address) == 150 * 10 ** 18
    assert token_wallet.getBalance(advocate1) == reward_amount1
    assert token_wallet.getBalance(advocate2) == reward_amount2