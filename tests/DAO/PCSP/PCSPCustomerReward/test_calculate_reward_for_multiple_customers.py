#!/usr/bin/python3
import pytest
import brownie
from brownie import accounts, PCSPCustomerReward


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


@pytest.fixture
def data_test(deployment, pcsp_deployment, const):
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    token_wallet_contract = pcsp_deployment['token_wallet_contract']
    token_wallet_owner = pcsp_deployment['token_wallet_owner']
    gfn_operator = deployment[const.GFN_OPERATOR]
    gene_nft_token = deployment[const.GNFT_TOKEN]
    genetic_profile_id1 = 12345678
    genetic_profile_id2 = 12333456
    genetic_profile_id3 = 234567654
    genetic_profile_owner1 = accounts.add()
    genetic_profile_owner2 = accounts.add()
    genetic_profile_owner3 = accounts.add()

    # mint GeneNFT
    gene_nft_token.mintBatchGNFT(
        [genetic_profile_owner1, genetic_profile_owner2, genetic_profile_owner3],
        [genetic_profile_id1, genetic_profile_id2, genetic_profile_id3],
        True,
        {"from": gfn_operator}
    )

    # set GeneNFTAddress to PCSPCustomerRewardConfiguration
    pcsp_configuration_contract.setGeneNFTAddress(
        gene_nft_token, {"from": pcsp_configuration_owner}
    )
    # Config Token PCSP Wallet
    pcsp_configuration_contract.setTokenWalletAddress(
        token_wallet_contract, {"from": pcsp_configuration_owner}
    )
    # set DAO Token Operator
    token_wallet_contract.addOperator(
        pcsp_reward_contract, {"from": token_wallet_owner}
    )

    assert pcsp_configuration_contract.getGeneNFTAddress() == gene_nft_token
    assert pcsp_configuration_contract.getTokenWalletAddress() == token_wallet_contract
    assert token_wallet_contract.checkActiveOperator(pcsp_reward_contract) is True

    return {
        'genenft_token_id1': genetic_profile_id1,
        'genenft_token_id2': genetic_profile_id2,
        'genenft_token_id3': genetic_profile_id3,
        'genetic_profile_owner1': genetic_profile_owner1,
        'genetic_profile_owner2': genetic_profile_owner2,
        'genetic_profile_owner3': genetic_profile_owner3,
    }


def test_success__calculate_reward_for_multiple_customers__owner_make_txn(
        pcsp_deployment, data_test
):
    # Arranges
    token_wallet_contract = pcsp_deployment['token_wallet_contract']
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    genenft_token_id1 = data_test['genenft_token_id1']
    genetic_profile_owner1 = data_test['genetic_profile_owner1']
    risk_of_getting_stroke = 1
    revenue_in_pcsp = 50e+18

    # Assert before actions
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0

    # Actions
    txn = pcsp_reward_contract.calculateRewardForMultipleCustomers(
        [genenft_token_id1],
        [risk_of_getting_stroke],
        [revenue_in_pcsp],
        {"from": pcsp_reward_owner}
    )

    # Assert: SetPCSPConfiguration Event
    assert ('RecordRiskOfGettingStroke' in txn.events) is True
    assert txn.events['RecordRiskOfGettingStroke']['geneNFTTokenID'] == genenft_token_id1
    assert txn.events['RecordRiskOfGettingStroke']['riskOfGettingStroke'] == risk_of_getting_stroke

    # Assert: SetPCSPConfiguration Event
    assert ('RewardForRiskOfGettingStroke' in txn.events) is True
    assert txn.events['RewardForRiskOfGettingStroke']['geneNFTTokenID'] == genenft_token_id1
    assert txn.events['RewardForRiskOfGettingStroke']['geneNFTOwner'] == genetic_profile_owner1
    assert txn.events['RewardForRiskOfGettingStroke']['riskOfGettingStroke'] == risk_of_getting_stroke
    assert txn.events['RewardForRiskOfGettingStroke']['revenue'] == revenue_in_pcsp
    assert txn.events['RewardForRiskOfGettingStroke']['rewardAmount'] == 500e+18

    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 500e+18
    assert pcsp_reward_contract.getRiskOfGettingStroke(genenft_token_id1) == 1
    assert pcsp_reward_contract.checkGeneNFTRewardStatus(genenft_token_id1) is True


def test_success__calculate_reward_for_multiple_customers__two_customers(
        pcsp_deployment, data_test
):
    # Arranges
    token_wallet_contract = pcsp_deployment['token_wallet_contract']
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    genenft_token_id1 = data_test['genenft_token_id1']
    genenft_token_id2 = data_test['genenft_token_id2']
    genetic_profile_owner1 = data_test['genetic_profile_owner1']
    genetic_profile_owner2 = data_test['genetic_profile_owner2']
    risk_of_getting_stroke1 = 1
    risk_of_getting_stroke2 = 3
    revenue_in_pcsp_1 = 50e+18
    revenue_in_pcsp_2 = 240e+18

    # Assert before actions
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0

    # Actions
    txn = pcsp_reward_contract.calculateRewardForMultipleCustomers(
        [genenft_token_id1, genenft_token_id2],
        [risk_of_getting_stroke1, risk_of_getting_stroke2],
        [revenue_in_pcsp_1, revenue_in_pcsp_2],
        {"from": pcsp_reward_owner}
    )

    # Assert Event
    assert ('RecordRiskOfGettingStroke' in txn.events) is True
    assert txn.events['RecordRiskOfGettingStroke'][0]['geneNFTTokenID'] == genenft_token_id1
    assert txn.events['RecordRiskOfGettingStroke'][0]['riskOfGettingStroke'] == risk_of_getting_stroke1
    assert txn.events['RecordRiskOfGettingStroke'][1]['geneNFTTokenID'] == genenft_token_id2
    assert txn.events['RecordRiskOfGettingStroke'][1]['riskOfGettingStroke'] == risk_of_getting_stroke2

    # Assert event
    assert ('RewardForRiskOfGettingStroke' in txn.events) is True
    assert txn.events['RewardForRiskOfGettingStroke'][0]['geneNFTTokenID'] == genenft_token_id1
    assert txn.events['RewardForRiskOfGettingStroke'][0]['geneNFTOwner'] == genetic_profile_owner1
    assert txn.events['RewardForRiskOfGettingStroke'][0]['riskOfGettingStroke'] == risk_of_getting_stroke1
    assert txn.events['RewardForRiskOfGettingStroke'][0]['revenue'] == revenue_in_pcsp_1
    assert txn.events['RewardForRiskOfGettingStroke'][0]['rewardAmount'] == 500e+18

    assert txn.events['RewardForRiskOfGettingStroke'][1]['geneNFTTokenID'] == genenft_token_id2
    assert txn.events['RewardForRiskOfGettingStroke'][1]['geneNFTOwner'] == genetic_profile_owner2
    assert txn.events['RewardForRiskOfGettingStroke'][1]['riskOfGettingStroke'] == risk_of_getting_stroke2
    assert txn.events['RewardForRiskOfGettingStroke'][1]['revenue'] == revenue_in_pcsp_2
    assert txn.events['RewardForRiskOfGettingStroke'][1]['rewardAmount'] == 480e+18

    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 500e+18
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 480e+18

    assert pcsp_reward_contract.getRiskOfGettingStroke(genenft_token_id1) == 1
    assert pcsp_reward_contract.checkGeneNFTRewardStatus(genenft_token_id1) is True
    assert pcsp_reward_contract.getRiskOfGettingStroke(genenft_token_id2) == 3
    assert pcsp_reward_contract.checkGeneNFTRewardStatus(genenft_token_id2) is True


def test_failure__calculate_reward_for_multiple_customers__not_owner_make_txn(
        pcsp_deployment, data_test
):
    # Arranges
    token_wallet_contract = pcsp_deployment['token_wallet_contract']
    pcsp_reward_owner_fake = accounts.add()
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    genenft_token_id1 = data_test['genenft_token_id1']
    genetic_profile_owner1 = data_test['genetic_profile_owner1']
    risk_of_getting_stroke = 1
    revenue_in_pcsp = 50e+18

    # Assert before actions
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0

    # Actions
    with brownie.reverts("Ownable: caller is not the owner"):
        pcsp_reward_contract.calculateRewardForMultipleCustomers(
            [genenft_token_id1],
            [risk_of_getting_stroke],
            [revenue_in_pcsp],
            {"from": pcsp_reward_owner_fake}
        )

    # Assert after actions
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0

    assert pcsp_reward_contract.getRiskOfGettingStroke(genenft_token_id1) == 0
    assert pcsp_reward_contract.checkGeneNFTRewardStatus(genenft_token_id1) is False


def test_failure__calculate_reward_for_multiple_customers__invalid_risk_value(
        pcsp_deployment, data_test
):
    # Arranges
    token_wallet_contract = pcsp_deployment['token_wallet_contract']
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    genenft_token_id1 = data_test['genenft_token_id1']
    genenft_token_id2 = data_test['genenft_token_id2']
    genetic_profile_owner1 = data_test['genetic_profile_owner1']
    genetic_profile_owner2 = data_test['genetic_profile_owner2']
    risk_of_getting_stroke1_invalid = 1000
    risk_of_getting_stroke2 = 3
    revenue_in_pcsp_1 = 50e+18
    revenue_in_pcsp_2 = 240e+18

    # Assert before actions
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0

    # Actions
    with brownie.reverts("PCSPCustomerReward: risk of getting stroke value is invalid"):
        pcsp_reward_contract.calculateRewardForMultipleCustomers(
            [genenft_token_id1, genenft_token_id2],
            [risk_of_getting_stroke1_invalid, risk_of_getting_stroke2],
            [revenue_in_pcsp_1, revenue_in_pcsp_2],
            {"from": pcsp_reward_owner}
        )

    # Assert after actions
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0


def test_failure__calculate_reward_for_multiple_customers__invalid_nft_id(
        pcsp_deployment, data_test
):
    # Arranges
    token_wallet_contract = pcsp_deployment['token_wallet_contract']
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    genenft_token_id1_invalid = 88888888888
    genenft_token_id2 = data_test['genenft_token_id2']
    genetic_profile_owner1 = data_test['genetic_profile_owner1']
    genetic_profile_owner2 = data_test['genetic_profile_owner2']
    risk_of_getting_stroke1 = 1
    risk_of_getting_stroke2 = 3
    revenue_in_pcsp_1 = 50e+18
    revenue_in_pcsp_2 = 240e+18

    # Assert before actions
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0

    # Actions
    with brownie.reverts("ERC721: owner query for nonexistent token"):
        pcsp_reward_contract.calculateRewardForMultipleCustomers(
            [genenft_token_id1_invalid, genenft_token_id2],
            [risk_of_getting_stroke1, risk_of_getting_stroke2],
            [revenue_in_pcsp_1, revenue_in_pcsp_2],
            {"from": pcsp_reward_owner}
        )

    # Assert after actions
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0

    assert pcsp_reward_contract.getRiskOfGettingStroke(genenft_token_id1_invalid) == 0
    assert pcsp_reward_contract.checkGeneNFTRewardStatus(genenft_token_id1_invalid) is False
    assert pcsp_reward_contract.getRiskOfGettingStroke(genenft_token_id2) == 0
    assert pcsp_reward_contract.checkGeneNFTRewardStatus(genenft_token_id2) is False


def test_failure__calculate_reward_for_multiple_customers__duplicated_reward(
        pcsp_deployment, data_test
):
    # Arranges
    token_wallet_contract = pcsp_deployment['token_wallet_contract']
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    genenft_token_id1 = data_test['genenft_token_id1']
    genenft_token_id2 = data_test['genenft_token_id2']
    genetic_profile_owner1 = data_test['genetic_profile_owner1']
    genetic_profile_owner2 = data_test['genetic_profile_owner2']
    risk_of_getting_stroke1 = 1
    risk_of_getting_stroke2 = 3
    revenue_in_pcsp_1 = 50e+18
    revenue_in_pcsp_2 = 240e+18

    # Assert before action1
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0

    # Action 1
    pcsp_reward_contract.calculateRewardForMultipleCustomers(
        [genenft_token_id1, genenft_token_id2],
        [risk_of_getting_stroke1, risk_of_getting_stroke2],
        [revenue_in_pcsp_1, revenue_in_pcsp_2],
        {"from": pcsp_reward_owner}
    )

    # Assert after action1
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 500e+18
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 480e+18

    # Action 2: Duplicated Calculate Reward
    with brownie.reverts("PCSPCustomerReward: the GeneNFT has rewarded for "
                         "risk of getting stroke"):
        pcsp_reward_contract.calculateRewardForMultipleCustomers(
            [genenft_token_id1],
            [risk_of_getting_stroke1],
            [revenue_in_pcsp_1],
            {"from": pcsp_reward_owner}
        )

    # Assert after action2
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 500e+18


def test_failure__calculate_reward_for_multiple_customers__invalid_length_list_of_ids(
        pcsp_deployment, data_test
):
    # Arranges
    token_wallet_contract = pcsp_deployment['token_wallet_contract']
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    genenft_token_id1 = data_test['genenft_token_id1']
    genetic_profile_owner1 = data_test['genetic_profile_owner1']
    genetic_profile_owner2 = data_test['genetic_profile_owner2']
    risk_of_getting_stroke1 = 1
    risk_of_getting_stroke2 = 3
    revenue_in_pcsp_1 = 50e+18
    revenue_in_pcsp_2 = 240e+18

    # Assert before actions
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0

    # Actions
    with brownie.reverts("PCSPCustomerReward: list of GeneNFTTokenIds "
                         "and risksOfGettingStroke must have same length"):
        pcsp_reward_contract.calculateRewardForMultipleCustomers(
            [genenft_token_id1],
            [risk_of_getting_stroke1, risk_of_getting_stroke2],
            [revenue_in_pcsp_1, revenue_in_pcsp_2],
            {"from": pcsp_reward_owner}
        )

    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0


def test_failure__calculate_reward_for_multiple_customers__invalid_length_list_of_risks(
        pcsp_deployment, data_test
):
    # Arranges
    token_wallet_contract = pcsp_deployment['token_wallet_contract']
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    genenft_token_id1 = data_test['genenft_token_id1']
    genenft_token_id2 = data_test['genenft_token_id2']
    genetic_profile_owner1 = data_test['genetic_profile_owner1']
    genetic_profile_owner2 = data_test['genetic_profile_owner2']
    risk_of_getting_stroke1 = 1
    revenue_in_pcsp_1 = 50e+18
    revenue_in_pcsp_2 = 240e+18

    # Assert before actions
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0

    # Actions
    with brownie.reverts("PCSPCustomerReward: list of GeneNFTTokenIds "
                         "and risksOfGettingStroke must have same length"):
        pcsp_reward_contract.calculateRewardForMultipleCustomers(
            [genenft_token_id1, genenft_token_id2],
            [risk_of_getting_stroke1],
            [revenue_in_pcsp_1, revenue_in_pcsp_2],
            {"from": pcsp_reward_owner}
        )

    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0


def test_failure__calculate_reward_for_multiple_customers__invalid_length_list_of_revenues(
        pcsp_deployment, data_test
):
    # Arranges
    token_wallet_contract = pcsp_deployment['token_wallet_contract']
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    genenft_token_id1 = data_test['genenft_token_id1']
    genenft_token_id2 = data_test['genenft_token_id2']
    genetic_profile_owner1 = data_test['genetic_profile_owner1']
    genetic_profile_owner2 = data_test['genetic_profile_owner2']
    risk_of_getting_stroke1 = 1
    risk_of_getting_stroke2 = 3
    revenue_in_pcsp_1 = 50e+18

    # Assert before actions
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0

    # Actions
    with brownie.reverts("PCSPCustomerReward: list of risksOfGettingStroke "
                         "and revenues must have same length"):
        pcsp_reward_contract.calculateRewardForMultipleCustomers(
            [genenft_token_id1, genenft_token_id2],
            [risk_of_getting_stroke1, risk_of_getting_stroke2],
            [revenue_in_pcsp_1],
            {"from": pcsp_reward_owner}
        )

    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0


def test_failure__calculate_reward_for_multiple_customers__length_list_of_revenues_over(
        pcsp_deployment, data_test
):
    # Arranges
    token_wallet_contract = pcsp_deployment['token_wallet_contract']
    pcsp_reward_owner = pcsp_deployment['pcsp_reward_owner']
    pcsp_reward_contract = pcsp_deployment['pcsp_reward_contract']
    genenft_token_id1 = data_test['genenft_token_id1']
    genenft_token_id2 = data_test['genenft_token_id2']
    genetic_profile_owner1 = data_test['genetic_profile_owner1']
    genetic_profile_owner2 = data_test['genetic_profile_owner2']
    risk_of_getting_stroke1 = 1
    risk_of_getting_stroke2 = 3
    revenue_in_pcsp_1 = 50e+18
    revenue_in_pcsp_2 = 240e+18

    # Assert before actions
    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0

    # Actions
    with brownie.reverts("PCSPCustomerReward: list of risksOfGettingStroke "
                         "and revenues must have same length"):
        pcsp_reward_contract.calculateRewardForMultipleCustomers(
            [genenft_token_id1, genenft_token_id2],
            [risk_of_getting_stroke1, risk_of_getting_stroke2],
            [revenue_in_pcsp_1, revenue_in_pcsp_2, revenue_in_pcsp_2],
            {"from": pcsp_reward_owner}
        )

    assert token_wallet_contract.getBalance(genetic_profile_owner1) == 0
    assert token_wallet_contract.getBalance(genetic_profile_owner2) == 0