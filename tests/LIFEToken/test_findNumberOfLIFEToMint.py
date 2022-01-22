import pytest


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_success__find_LIFE_to_mint__total_01_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 90000000e+18


def test_success__find_LIFE_to_mint__total_02_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 2

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10000000e+18


def test_success__find_LIFE_to_mint__total_4_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 4

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10000000e+18


def test_success__find_LIFE_to_mint__total_10_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 2

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10000000e+18


def test_success__find_LIFE_to_mint__total_11_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 11

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 1000000e+18


def test_success__find_LIFE_to_mint__total_55_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 55

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 1000000e+18


def test_success__find_LIFE_to_mint__total_100_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 100

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 1000000e+18


def test_success__find_LIFE_to_mint__total_101_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 101

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 100000e+18


def test_success__find_LIFE_to_mint__total_111_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 111

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 100000e+18


def test_success__find_LIFE_to_mint__total_500_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 500

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 100000e+18


def test_success__find_LIFE_to_mint__total_1000_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 1000

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 100000e+18


def test_success__find_LIFE_to_mint__total_1001_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 1001

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10000e+18


def test_success__find_LIFE_to_mint__total_2000_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 2000

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10000e+18


def test_success__find_LIFE_to_mint__total_10000_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10000

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10000e+18


def test_success__find_LIFE_to_mint__total_10001_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10001

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 1000e+18


def test_success__find_LIFE_to_mint__total_100000_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 100000

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 1000e+18


def test_success__find_LIFE_to_mint__total_100001_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 100001

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 100e+18


def test_success__find_LIFE_to_mint__total_1000000_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**6

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 100e+18


def test_success__find_LIFE_to_mint__total_1000001_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**6 + 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10e+18


def test_success__find_LIFE_to_mint__total_10000001_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**7 + 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**18


def test_success__find_LIFE_to_mint__total_100000001_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**8 + 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**17


def test_success__find_LIFE_to_mint__total_1000000000_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**9

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**17


def test_success__find_LIFE_to_mint__total_1000000001_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**9 + 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**16


def test_success__find_LIFE_to_mint__total_1e10_plus_1_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**10 + 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**15


def test_success__find_LIFE_to_mint__total_1e11_plus_1_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**11 + 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**14


def test_success__find_LIFE_to_mint__total_1e12_plus_1_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**12 + 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**13


def test_success__find_LIFE_to_mint__total_1e13_plus_1_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**13 + 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**12


def test_success__find_LIFE_to_mint__total_1e14_plus_1_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**14 + 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**11


def test_success__find_LIFE_to_mint__total_1e15_plus_1_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**15 + 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**10


def test_success__find_LIFE_to_mint__total_1e16_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**16

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**10


def test_success__find_LIFE_to_mint__total_1e16_plus_1_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**16 + 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**9


def test_success__find_LIFE_to_mint__total_1e17_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**17

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10**9


def test_success__find_LIFE_to_mint__total_1e17_plus_1_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10**17 + 1

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 0
