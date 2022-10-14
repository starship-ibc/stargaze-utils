from datetime import datetime, timedelta

from stargazeutils.coin import Coin
from stargazeutils.collection.nft_collection import NFTCollection
from stargazeutils.market import AskCollection
from stargazeutils.market.market_ask import MarketAsk
from tests.assets import test_vals

FUTURE = datetime.utcnow() + timedelta(1)

asks = [
    MarketAsk(
        test_vals.sg721_addr,
        1,
        "seller-1",
        Coin.from_stars(444),
        FUTURE,
    ),
    MarketAsk(
        test_vals.sg721_addr,
        2,
        "seller-1",
        Coin.from_stars(555),
        FUTURE,
    ),
    MarketAsk(
        test_vals.sg721_addr,
        4,
        "seller-1",
        Coin.from_stars(444),
        datetime.utcnow() - timedelta(1),
    ),
]
token_info = NFTCollection(
    test_vals.sg721_addr,
    [
        {"id": 1, "type": "Grass", "rank": 2},
        {"id": 2, "type": "Grass", "rank": 2},
        {"id": 4, "type": "Fire", "rank": 1},
    ],
)


def test_ask_collection_should_create_asks_by_trait():
    ac = AskCollection(asks, token_info)
    traits = ac.create_asks_by_trait()
    assert len(traits) == 1

    type_trait = traits["type"]
    assert len(type_trait) == 2

    grass_type = type_trait["Grass"]
    assert len(grass_type) == 2
    assert grass_type[0]["ask"] == asks[0]
    assert grass_type[0]["token_info"] == token_info.tokens[asks[0].token_id]
    assert grass_type[1]["ask"] == asks[1]
    assert grass_type[1]["token_info"] == token_info.tokens[asks[1].token_id]

    fire_type = type_trait["Fire"]
    assert len(fire_type) == 1
    assert fire_type[0]["ask"] == asks[2]
    assert fire_type[0]["token_info"] == token_info.tokens[asks[2].token_id]


def test_ask_collection_create_asks_by_trait_returns_all_when_no_traits():
    asks = [
        MarketAsk("star1", 1, "seller", Coin.from_stars(10), FUTURE),
        MarketAsk("star1", 2, "seller", Coin.from_stars(20), FUTURE),
    ]
    token_info = NFTCollection("star1", [{"id": 1}, {"id": 2}])

    ac = AskCollection(asks, token_info)
    trait_asks = ac.create_asks_by_trait()

    import pprint

    pprint.pprint(trait_asks)
    assert trait_asks == {
        "all": {
            "all": [
                {"ask": asks[0], "token_info": token_info.tokens[1]},
                {"ask": asks[1], "token_info": token_info.tokens[2]},
            ]
        }
    }


def test_ask_collection_should_get_csv_table():
    ac = AskCollection(asks, token_info)
    table = ac.get_csv_table(["type"])
    assert table == [
        ["id", "price", "seller", "valid", "reason", "type"],
        ["1", "444", "seller-1", "True", "VALID", "Grass"],
        ["2", "555", "seller-1", "True", "VALID", "Grass"],
        ["4", "444", "seller-1", "False", "LISTING_EXPIRED", "Fire"],
    ]


def test_ask_collection_should_get_trait_pricing_table():
    ac = AskCollection(asks, token_info)
    table = ac.get_avg_trait_pricing_table()

    assert table == [
        ["Trait", "Value", "Num Listings", "Min Price", "Avg Price", "Max Price"],
        ["type", "Grass", 2, "444", "499.5", "555"],
        ["type", "Fire", 1, "444", "444", "444"],
    ]
