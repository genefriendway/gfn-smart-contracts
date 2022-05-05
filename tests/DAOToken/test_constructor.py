import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__initialize_dao_token(dao_deployment):
    # Arranges
    dao_token = dao_deployment['dao_token']
