import pytest


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__initialize_life_2_genomic_dao_token(
        life_2_genomic_dao_token_deployment
):
    # Arranges
    life_token = life_2_genomic_dao_token_deployment['life_token']
    life_2_genomic_dao_token = \
        life_2_genomic_dao_token_deployment['life_2_genomic_dao_token']

    # Assert
    assert life_token.balanceOf(life_2_genomic_dao_token.address) == 100
