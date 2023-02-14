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


def test_success__reward_advocates_monthly__owner_make_txn(
        advocate_deployment, data_test
):
    # Arranges
    token_wallet = advocate_deployment['token_wallet_contract']
    advocate_reward_owner = advocate_deployment['advocate_reward_owner']
    advocate_reward_contract = advocate_deployment['advocate_reward_contract']
    config = advocate_deployment['advocate_reward_configuration_contract']

    customer_reward_address = data_test['customer_reward_address']
    platform_fee_address = data_test['platform_fee_address']
    community_campaign_address = data_test['community_campaign_address']
    quarter_referral_reward_address = data_test['quarter_referral_reward_address']
    advocate_reward_address = data_test['advocate_reward_address']

    advocate1 = accounts.add()
    advocate2 = accounts.add()
    advocate3 = accounts.add()
    
    revenue1 = 80 * 10 ** 18
    revenue2 = 15 * 10 ** 18
    revenue3 = 230 * 10 ** 18

    referral1 = 101
    referral2 = 2
    referral3 = 205

    # Assert Before Actions
    assert token_wallet.getBalance(customer_reward_address) == 0
    assert token_wallet.getBalance(platform_fee_address) == 0
    assert token_wallet.getBalance(community_campaign_address) == 0
    assert token_wallet.getBalance(quarter_referral_reward_address) == 0
    assert token_wallet.getBalance(advocate_reward_address) == 0
    assert token_wallet.getBalance(advocate1) == 0
    assert token_wallet.getBalance(advocate2) == 0
    assert token_wallet.getBalance(advocate3) == 0

    # Actions
    txn = advocate_reward_contract.rewardAdvocatesMonthly(
        [advocate1, advocate2, advocate3], 
        [revenue1, revenue2, revenue3], 
        [referral1, referral2, referral3], 
        {"from": advocate_reward_owner}
    )

    # Assert: DistributeRevenue Event
    assert ('DistributeRevenue' in txn.events) is True
    assert txn.events['DistributeRevenue'][0]['totalRevenue'] == revenue1
    assert txn.events['DistributeRevenue'][0]['reserveRevenueForCustomerReward'] == 16 * 10 ** 18  # 20 %
    assert txn.events['DistributeRevenue'][0]['reserveRevenueForPlatformFee'] == 12 * 10 ** 18  # 15 %
    assert txn.events['DistributeRevenue'][0]['reserveRevenueForCommunityCampaign'] == 8 * 10 ** 18  # 10 %
    assert txn.events['DistributeRevenue'][0]['reserveRevenueForQuarterReferralReward'] == 4 * 10 ** 18  # 5 %
    assert txn.events['DistributeRevenue'][0]['rewardAmountForAdvocate'] == 24 * 10 ** 18  # 30 %
    assert txn.events['DistributeRevenue'][0]['remainingReservedRevenueForAdvocateReward'] == 16 * 10 ** 18  # 30 %

    assert txn.events['DistributeRevenue'][1]['totalRevenue'] == revenue2
    assert txn.events['DistributeRevenue'][1]['reserveRevenueForCustomerReward'] == 3 * 10 ** 18  # 20 %
    assert txn.events['DistributeRevenue'][1]['reserveRevenueForPlatformFee'] == 2.25 * 10 ** 18  # 15 %
    assert txn.events['DistributeRevenue'][1]['reserveRevenueForCommunityCampaign'] == 1.5 * 10 ** 18  # 10 %
    assert txn.events['DistributeRevenue'][1]['reserveRevenueForQuarterReferralReward'] == 0.75 * 10 ** 18  # 5 %
    assert txn.events['DistributeRevenue'][1]['rewardAmountForAdvocate'] == 3 * 10 ** 18  # 20 %
    assert txn.events['DistributeRevenue'][1]['remainingReservedRevenueForAdvocateReward'] == 4.5 * 10 ** 18  # 30 %

    assert txn.events['DistributeRevenue'][2]['totalRevenue'] == revenue3
    assert txn.events['DistributeRevenue'][2]['reserveRevenueForCustomerReward'] == 46 * 10 ** 18  # 20 %
    assert txn.events['DistributeRevenue'][2]['reserveRevenueForPlatformFee'] == 34.5 * 10 ** 18  # 15 %
    assert txn.events['DistributeRevenue'][2]['reserveRevenueForCommunityCampaign'] == 23 * 10 ** 18  # 10 %
    assert txn.events['DistributeRevenue'][2]['reserveRevenueForQuarterReferralReward'] == 11.5* 10 ** 18  # 5 %
    assert txn.events['DistributeRevenue'][2]['rewardAmountForAdvocate'] == 92 * 10 ** 18  # 40 %
    assert txn.events['DistributeRevenue'][2]['remainingReservedRevenueForAdvocateReward'] == 23 * 10 ** 18  # 10 %

    # Assert: RewardAdvocateMonthly Event
    assert ('RewardAdvocateMonthly' in txn.events) is True
    assert txn.events['RewardAdvocateMonthly'][0]['advocateAddress'] == advocate1
    assert txn.events['RewardAdvocateMonthly'][0]['revenue'] == revenue1
    assert txn.events['RewardAdvocateMonthly'][0]['numberOfReferrals'] == referral1
    assert txn.events['RewardAdvocateMonthly'][0]['rewardAmount'] == 24 * 10 ** 18 # 30 %

    assert txn.events['RewardAdvocateMonthly'][1]['advocateAddress'] == advocate2
    assert txn.events['RewardAdvocateMonthly'][1]['revenue'] == revenue2
    assert txn.events['RewardAdvocateMonthly'][1]['numberOfReferrals'] == referral2
    assert txn.events['RewardAdvocateMonthly'][1]['rewardAmount'] == 3 * 10 ** 18  # 20 %

    assert txn.events['RewardAdvocateMonthly'][2]['advocateAddress'] == advocate3
    assert txn.events['RewardAdvocateMonthly'][2]['revenue'] == revenue3
    assert txn.events['RewardAdvocateMonthly'][2]['numberOfReferrals'] == referral3
    assert txn.events['RewardAdvocateMonthly'][2]['rewardAmount'] == 92 * 10 ** 18  # 40 %

    # Assert token wallet
    assert token_wallet.getTotalBalance() == 325 * 10 ** 18

    assert token_wallet.getBalance(customer_reward_address) == 65 * 10 ** 18
    assert token_wallet.getBalance(platform_fee_address) == 48.75 * 10 ** 18
    assert token_wallet.getBalance(community_campaign_address) == 32.5 * 10 ** 18
    assert token_wallet.getBalance(quarter_referral_reward_address) == 16.25 * 10 ** 18
    assert token_wallet.getBalance(advocate_reward_address) == 43.5 * 10 ** 18
    assert token_wallet.getBalance(advocate1) == 24 * 10 ** 18
    assert token_wallet.getBalance(advocate2) == 3 * 10 ** 18
    assert token_wallet.getBalance(advocate3) == 92 * 10 ** 18


