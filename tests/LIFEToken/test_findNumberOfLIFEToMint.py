import brownie


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
    total_gnft_tokens = 1000000

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 100e+18


def test_success__find_LIFE_to_mint__total_1000001_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 1000001

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 10e+18


def test_success__find_LIFE_to_mint__total_10000001_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 10000001

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 1e+18


def test_success__find_LIFE_to_mint__total_100000001_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 100000001

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 1e+17


def test_success__find_LIFE_to_mint__total_1000000000_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 1000000000

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 1e+17


def test_success__find_LIFE_to_mint__total_1000000001_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 1000000001

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 1e+16


def test_success__find_LIFE_to_mint__total_12345678999_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 12345678999

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 0


def test_success__find_LIFE_to_mint__total_100000000001_GNFT(deployment, const):
    # Arranges
    life_token = deployment[const.LIFE_TOKEN]
    total_gnft_tokens = 100000000001

    # Actions
    number_of_life = life_token.findNumberOfLIFEToMint(total_gnft_tokens)

    # # Asserts
    assert number_of_life == 0
