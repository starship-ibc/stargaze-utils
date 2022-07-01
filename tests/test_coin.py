from stargazeutils import Coin


def test_given_equivalent_coins_should_be_equal():
    c1 = Coin("12", "ustars")
    c2 = Coin("12", "ustars")
    assert c1 == c2


def test_given_unequal_amounts_coins_should_be_unequal():
    c1 = Coin("12", "ustars")
    c2 = Coin("13", "ustars")
    assert c1 != c2


def test_given_uneqal_denoms_should_be_unequal():
    c1 = Coin("12", "ustars")
    c2 = Coin("12", "uatom")
    assert c1 != c2


def test_coin_string():
    c1 = Coin("1000000", "ustars")
    assert str(c1) == "1 stars"
    assert c1.__repr__() == str(c1)

    c1 = Coin("12", "uatom")
    assert str(c1) == "12 uatom"
    assert c1.__repr__() == str(c1)
