import json

from stargazeutils.coin import Coin
from stargazeutils.market import MarketBid


def test_bid_is_serializable():
    bid = MarketBid("stars1-c", 1, "seller", "buyer", Coin.from_stars(10), "c1", "a")

    d1 = bid.to_serializable()
    str = json.dumps(d1)

    d2 = json.loads(str)
    assert d1 == d2
    assert d1["collection"] == bid.collection
    assert d1["collection_name"] == bid.collection_name
    assert d1["seller"] == bid.seller
    assert d1["buyer"] == bid.buyer
    assert d1["price"] == bid.price.to_serializable()
    assert d1["tx_hash"] == bid.tx_hash


def test_bid_is_compariable():
    b1 = MarketBid("stars1-c", 1, "seller", "buyer", Coin.from_stars(10), "c1", "a")
    b2 = MarketBid("stars1-c", 1, "seller", "buyer", Coin.from_stars(10), "c1", "a")
    assert b1 == b2

    b2.collection = "invalid"
    assert b1 != b2

    b2.collection = b1.collection
    assert b1 == b2

    b2.some_field = "invalid"
    assert b1 != b2

    b1.other_field = "still_invalid"
    assert b1 != b2

    assert b1 != str(b1)
