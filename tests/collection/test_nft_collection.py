import os

from stargazeutils.collection import NFTCollection

from ..assets import test_vals


def test_nft_collection_should_create_from_json_file():
    c = NFTCollection.from_json_file(test_vals.sg721_addr, test_vals.collection_file)
    assert c.sg721 == test_vals.sg721_addr
    assert c.tokens[1] == {"id": 1, "Color": "blue", "Type": "electric"}
    assert c.tokens[2] == {"id": 2, "Color": "blue", "Type": "water"}
    assert c.tokens[3] == {"id": 3, "Color": "red", "Type": "fire"}
    assert c.tokens[4] == {"id": 4, "Color": "yellow", "Type": "electric"}


def test_nft_collection_should_create_trait_dict():
    c = NFTCollection.from_json_file(test_vals.sg721_addr, test_vals.collection_file)
    assert c.traits == {
        "Color": {"blue": [1, 2], "red": [3], "yellow": [4]},
        "Type": {"electric": [1, 4], "water": [2], "fire": [3]},
    }


def test_nft_collection_filter_should_return_tokens():
    c = NFTCollection.from_json_file(test_vals.sg721_addr, test_vals.collection_file)
    filters = {"Color": ["blue"]}
    tokens = c.filter_tokens(filters)
    assert tokens == {1, 2}


def test_nft_collection_filter_should_combine_filters():
    c = NFTCollection.from_json_file(test_vals.sg721_addr, test_vals.collection_file)
    filters = {"Color": ["blue"], "Type": ["electric"]}
    tokens = c.filter_tokens(filters)
    assert tokens == {1}


def test_nft_collection_filter_should_allow_multiple_options():
    c = NFTCollection.from_json_file(test_vals.sg721_addr, test_vals.collection_file)
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
    c = NFTCollection.from_json_file(test_vals.sg721_addr, test_vals.collection_file)

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


def test_nft_collection_should_get_token_table():
    c = NFTCollection.from_json_file(test_vals.sg721_addr, test_vals.collection_file)
    table = c.get_tokens_info_table()
    assert table == [
        ["id", "Color", "Type"],
        [1, "blue", "electric"],
        [2, "blue", "water"],
        [3, "red", "fire"],
        [4, "yellow", "electric"],
    ]


def test_nft_collection_should_get_token_table_should_ignore_invalid_sort_key():
    c = NFTCollection.from_json_file(test_vals.sg721_addr, test_vals.collection_file)
    table = c.get_tokens_info_table(sort_key="baddata")
    assert table == [
        ["id", "Color", "Type"],
        [1, "blue", "electric"],
        [2, "blue", "water"],
        [3, "red", "fire"],
        [4, "yellow", "electric"],
    ]


def test_nft_collection_should_get_token_table_excluding_traits():
    c = NFTCollection.from_json_file(test_vals.sg721_addr, test_vals.collection_file)
    table = c.get_tokens_info_table(excluded_traits=["Type"])
    assert table == [
        ["id", "Color"],
        [1, "blue"],
        [2, "blue"],
        [3, "red"],
        [4, "yellow"],
    ]


def test_nft_collection_should_get_token_table_given_specific_tokens():
    c = NFTCollection.from_json_file(test_vals.sg721_addr, test_vals.collection_file)
    table = c.get_tokens_info_table(token_ids=[1, 2], excluded_traits=["Type"])
    assert table == [
        ["id", "Color"],
        [1, "blue"],
        [2, "blue"],
    ]


def test_nft_collection_should_get_sorted_token_table():
    c = NFTCollection.from_json_file(test_vals.sg721_addr, test_vals.collection_file)
    table = c.get_tokens_info_table(sort_key="Type")
    assert table == [
        ["id", "Color", "Type"],
        [1, "blue", "electric"],
        [4, "yellow", "electric"],
        [3, "red", "fire"],
        [2, "blue", "water"],
    ]


def test_nft_collection_should_get_rarity_tables():
    collection = NFTCollection.from_json_file(
        test_vals.sg721_addr, test_vals.collection_file
    )
    table = collection.get_trait_rarity_table()

    assert table == [
        ["Total Tokens", 4, ""],
        ["", "", ""],
        ["3 Color", "", ""],
        ["- red", 1, "25.00%"],
        ["- yellow", 1, "25.00%"],
        ["- blue", 2, "50.00%"],
        ["", "", ""],
        ["3 Type", "", ""],
        ["- water", 1, "25.00%"],
        ["- fire", 1, "25.00%"],
        ["- electric", 2, "50.00%"],
    ]


def test_nft_collection_should_get_traitless_rarity_tables():
    collection = NFTCollection.from_json_file(
        test_vals.sg721_addr, test_vals.traitless_collection_file
    )
    table = collection.get_trait_rarity_table()

    assert table == [["No traits"]]
