from decimal import Decimal

import pytest

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
    c1 = Coin("12345000000", "ustars")
    assert str(c1) == "12,345 $STARS"
    assert c1.__repr__() == str(c1)

    c1 = Coin("12", "uatom")
    assert str(c1) == "12 uatom"
    assert c1.__repr__() == str(c1)


def test_coin_comparison():
    c1 = Coin("1", "ustars")
    c2 = Coin("2", "ustars")

    assert c1 < c2
    assert c1 <= c2
    assert c2 > c1
    assert c2 >= c1

    c3 = Coin("1", "ustars")
    assert c1 >= c3
    assert c1 <= c3


def test_coin_comparison_other_type():
    with pytest.raises(TypeError):
        assert Coin.from_stars(1) < 4

    with pytest.raises(TypeError):
        assert Coin.from_stars(1) <= 4


def test_coin_should_get_stars():
    stars = 42
    assert Coin.from_stars(stars).get_stars() == Decimal(stars)


def test_coin_should_not_get_stars_from_other_denom():
    c = Coin("123", "atom")
    assert c.get_stars() is None
