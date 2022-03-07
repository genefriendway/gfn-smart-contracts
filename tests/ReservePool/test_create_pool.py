import brownie
import pytest
from brownie import accounts


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__create_pool(deployment, const):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    reserve_pool = deployment[const.RESERVE_POOL]
    pool_id = 'Pool_ID_1'

    # Assert before
    assert reserve_pool.getStatusOfPool(pool_id) is False

    # Actions
    reserve_pool.createPool(pool_id, {"from": gfn_operator})

    # Asserts
    assert reserve_pool.getStatusOfPool(pool_id) is True


def test_failure__create_pool__not_gfn_owner_make_transaction(deployment, const):
    # Arranges
    reserve_pool = deployment[const.RESERVE_POOL]
    pool_id = 'Pool_ID_1'

    # Actions
    with brownie.reverts("AccessibleRegistry: caller must be operator"):
        reserve_pool.createPool(pool_id, {"from": accounts[5]})

    # Asserts
    assert reserve_pool.getStatusOfPool(pool_id) is False


def test_failure__create_pool__empty_pool_id(deployment, const):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    reserve_pool = deployment[const.RESERVE_POOL]
    pool_id = ''

    # Actions
    with brownie.reverts("ReservePool: Length of Pool Id is invalid"):
        reserve_pool.createPool(pool_id, {"from": gfn_operator})

    # Asserts
    assert reserve_pool.getStatusOfPool(pool_id) is False


def test_failure__create_pool__pool_id_over_max_length(deployment, const):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    reserve_pool = deployment[const.RESERVE_POOL]
    pool_id = 'KJHGFDTYUIOMNBGFGHJKJKJIUYFTDTRYUINBVFTUYGHIJKLOIUYTFYGHJLKJH' \
              'UYGFTGBJKJHUGYFKJHGFDTYUIOMNBGFGHJKJKJIUYFTDTRYUINBVFTUYGHIJK' \
              'LOIUYTFYGHJLKJHUYGFTGBJKJHUGYF'

    # Actions
    with brownie.reverts("ReservePool: Length of Pool Id is invalid"):
        reserve_pool.createPool(pool_id, {"from": gfn_operator})

    # Asserts
    assert reserve_pool.getStatusOfPool(pool_id) is False


def test_failure__create_pool__duplicated_pool_id(deployment, const):
    # Arranges
    gfn_operator = deployment[const.GFN_OPERATOR]
    reserve_pool = deployment[const.RESERVE_POOL]
    pool_id = 'POOL_ID_1'

    # Asserts
    assert reserve_pool.getStatusOfPool(pool_id) is False
    # Action
    reserve_pool.createPool(pool_id, {"from": gfn_operator})
    # Asserts
    assert reserve_pool.getStatusOfPool(pool_id) is True

    # Actions: re-create PoolID
    with brownie.reverts("ReservePool: Pool Id was created"):
        reserve_pool.createPool(pool_id, {"from": gfn_operator})

    # Asserts
    assert reserve_pool.getStatusOfPool(pool_id) is True
