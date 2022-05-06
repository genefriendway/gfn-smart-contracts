import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__initialize_dao_token(dao_deployment):
    # Arranges
    dao_token = dao_deployment['dao_token']
    owner = dao_deployment['owner']

    # Assert
    assert dao_token.name() == "Post-Covid-Stroke Prevention"
    assert dao_token.symbol() == "PCSP"
    assert dao_token.totalSupply() == 1000
    assert dao_token.balanceOf(owner) == 1000
