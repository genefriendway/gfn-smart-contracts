#!/usr/bin/python3

import pytest

from brownie import accounts, PCSPConfiguration, PCSPReward


@pytest.fixture(scope="module")
def pcsp_reward_setup(pcsp_deployment):
    pcsp_configuration_owner = pcsp_deployment['pcsp_configuration_owner']
    pcsp_configuration_contract = pcsp_deployment['pcsp_configuration_contract']
