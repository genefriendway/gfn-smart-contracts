import pytest
import brownie

from brownie import (
    accounts,
    GenomicDAOToken,
    TokenVesting,
)


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__initialize_token_vesting():
    # Arranges
    deployer = accounts[0]
    dao_token_owner = accounts[1]
    token_vesting_owner = accounts[2]

    # Deploy GenomicDAOToken contract
    dao_token_contract = GenomicDAOToken.deploy(
        dao_token_owner,
        "Token Name",
        "TOKEN",
        1000000000 * 10 ** 18,
        {"from": deployer}
    )

    # Deploy TokenVesting contract
    token_vesting = TokenVesting.deploy(
        dao_token_contract,
        token_vesting_owner,
        {"from": deployer}
    )
    assert dao_token_contract == token_vesting.getToken()
    assert token_vesting_owner == token_vesting.owner()


def test_failure__token_is_null():
    # Arranges
    deployer = accounts[0]
    dao_token_contract = '0x0000000000000000000000000000000000000000'

    # Deploy TokenVesting contract
    with brownie.reverts(""):
        TokenVesting.deploy(
            dao_token_contract, deployer, {"from": deployer}
        )
