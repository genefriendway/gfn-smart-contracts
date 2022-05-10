import pytest


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    """make each function being isolated by common fixtures"""
    pass


def test_success__initialize_genomic_dao_token_2_life(
        genomic_dao_token_2_life_deployment
):
    # Arranges
    dao_token = genomic_dao_token_2_life_deployment['dao_token']
    genomic_dao_token_2_life = \
        genomic_dao_token_2_life_deployment['genomic_dao_token_2_life']

    # Assert
    assert dao_token.balanceOf(genomic_dao_token_2_life.address) == 100
