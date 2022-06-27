from stargazeutils.nft_collection import NFTCollection

test_sg721 = "addr1"
test_collection_file = "tests/assets/eg_collection.json"

def test_nft_collection_should_create_from_json_file():
    c = NFTCollection.from_json_file(test_sg721, test_collection_file)
    assert c.sg721 == test_sg721
    assert c.tokens[1] ==  {"id": 1, "Color": "blue", "Type": "electric"}
    assert c.tokens[2] ==  {"id": 2, "Color": "blue", "Type": "water"}
    assert c.tokens[3] ==  {"id": 3, "Color": "red", "Type": "fire"}
    assert c.tokens[4] ==  {"id": 4, "Color": "yellow", "Type": "electric"}

def test_nft_collection_should_create_trait_dict():
    c = NFTCollection.from_json_file(test_sg721, test_collection_file)
    assert c.traits == {
        "Color": {
            "blue": [1, 2],
            "red": [3],
            "yellow": [4]
        },
        "Type": {
            "electric": [1,4],
            "water": [2],
            "fire": [3]
        }
    }

def test_nft_collection_filter_should_return_tokens():
    c = NFTCollection.from_json_file(test_sg721, test_collection_file)
    filters = {"Color": ["blue"]}
    tokens = c.filter_tokens(filters)
    assert tokens == {1, 2}

def test_nft_collection_filter_should_combine_filters():
    c = NFTCollection.from_json_file(test_sg721, test_collection_file)
    filters = {"Color": ["blue"], "Type": ["electric"]}
    tokens = c.filter_tokens(filters)
    assert tokens == {1}

def test_nft_collection_filter_should_allow_multiple_options():
    c = NFTCollection.from_json_file(test_sg721, test_collection_file)
    filters = {"Color": ["blue", "red"]}
    tokens = c.filter_tokens(filters)
    assert tokens == {1, 2, 3}
