import os

from stargazeutils.collection import NFTCollection

from ..assets import test_vals


def test_nft_collection_should_create_from_json_file():
    c = NFTCollection.from_json_file(
        test_vals.sg721_addr, test_vals.test_collection_file
    )
    assert c.sg721 == test_vals.sg721_addr
    assert c.tokens[1] == {"id": 1, "Color": "blue", "Type": "electric"}
    assert c.tokens[2] == {"id": 2, "Color": "blue", "Type": "water"}
    assert c.tokens[3] == {"id": 3, "Color": "red", "Type": "fire"}
    assert c.tokens[4] == {"id": 4, "Color": "yellow", "Type": "electric"}


def test_nft_collection_should_create_trait_dict():
    c = NFTCollection.from_json_file(
        test_vals.sg721_addr, test_vals.test_collection_file
    )
    assert c.traits == {
        "Color": {"blue": [1, 2], "red": [3], "yellow": [4]},
        "Type": {"electric": [1, 4], "water": [2], "fire": [3]},
    }


def test_nft_collection_filter_should_return_tokens():
    c = NFTCollection.from_json_file(
        test_vals.sg721_addr, test_vals.test_collection_file
    )
    filters = {"Color": ["blue"]}
    tokens = c.filter_tokens(filters)
    assert tokens == {1, 2}


def test_nft_collection_filter_should_combine_filters():
    c = NFTCollection.from_json_file(
        test_vals.sg721_addr, test_vals.test_collection_file
    )
    filters = {"Color": ["blue"], "Type": ["electric"]}
    tokens = c.filter_tokens(filters)
    assert tokens == {1}


def test_nft_collection_filter_should_allow_multiple_options():
    c = NFTCollection.from_json_file(
        test_vals.sg721_addr, test_vals.test_collection_file
    )
    filters = {"Color": ["blue", "red"]}
    tokens = c.filter_tokens(filters)
    assert tokens == {1, 2, 3}


def test_sg721_client_should_fetch_trait_rarity():
    collection = NFTCollection(test_vals.sg721_addr, test_vals.token_traits.values())

    rarity = collection.fetch_trait_rarity()
    assert len(rarity) == len(test_vals.rarity)
    for trait, values in rarity.items():
        assert len(values) == len(test_vals.rarity[trait])
        for value, count in values.items():
            assert count == test_vals.rarity[trait][value]


def test_nft_collection_should_export_json():
    c = NFTCollection.from_json_file(
        test_vals.sg721_addr, test_vals.test_collection_file
    )

    filename = "test-collection.json"
    c.export_json(filename)

    try:
        assert os.path.exists(filename)
        c2 = NFTCollection.from_json_file(test_vals.sg721_addr, filename)
        assert len(c.tokens) == len(c2.tokens)
        for id, token in c.tokens.items():
            expected_token = c2.tokens[id]
            assert len(token) == len(expected_token)
            for k, v in token.items():
                assert v == expected_token[k]
    finally:
        os.remove(filename)


def test_nft_collection_should_export_csv():
    c = NFTCollection.from_json_file(
        test_vals.sg721_addr, test_vals.test_collection_file
    )
    filename = "test-collection.csv"
    assert not os.path.exists(filename)
    try:
        c.export_csv(filename)
        assert os.path.exists(filename)
    finally:
        os.remove(filename)
