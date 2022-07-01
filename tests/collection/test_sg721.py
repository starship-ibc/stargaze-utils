from tests.mock_response import MockResponse
from unittest import mock

from stargazeutils.collection import Sg721Client
from stargazeutils.collection.collection_info import CollectionInfo
from stargazeutils.collection.minter_config import MinterConfig
from stargazeutils.collection.whitelist import Whitelist
from ..assets import test_rarity, test_token_metadata, test_token_traits, test_sg721_addr, test_minter_addr, test_whitelist_addr, test_owner, test_sg721_contract_info_data, test_minter_config_data, test_collection_info_data, test_whitelist_data


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_tokens_owned_by(sg_client):
    client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)

    sg_client.query_contract.return_value = {"data": {"tokens": [1, 2, 3]}}
    tokens = client.fetch_tokens_owned_by(test_owner)

    sg_client.query_contract.assert_called_with(test_sg721_addr, {"tokens": {"owner": test_owner}})
    assert tokens == [1, 2, 3]

@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_query_minter_given_none(sg_client):
    sg_client.fetch_sg721_minter.return_value = test_minter_addr
    client = Sg721Client(test_sg721_addr, sg_client=sg_client)
    assert client.minter == test_minter_addr


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_query_minter_config_once(sg_client):
    client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)

    expected_minter_config = MinterConfig.from_data(test_minter_config_data)
    sg_client.query_contract.return_value = {"data": test_minter_config_data}

    minter_config = client.query_minter_config()
    assert minter_config == expected_minter_config

    minter_config = client.query_minter_config()
    assert minter_config == expected_minter_config
    sg_client.query_contract.assert_called_once_with(test_minter_addr, {"config": {}})


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_query_collection_info_once(sg_client):
    client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)

    expected_collection_info = CollectionInfo.from_data(test_collection_info_data)
    sg_client.query_contract.return_value = {"data": test_collection_info_data}

    collection_info = client.query_collection_info()
    assert collection_info == expected_collection_info

    collection_info = client.query_collection_info()
    assert collection_info == expected_collection_info
    sg_client.query_contract.assert_called_once_with(test_sg721_addr, {"collection_info": {}})


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_query_whitelist_once(sg_client):
    client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)
    client._minter_config = MinterConfig.from_data(test_minter_config_data)

    expected_whitelist = Whitelist.from_data(test_whitelist_data)
    sg_client.query_contract.return_value = {"data": test_whitelist_data}

    whitelist = client.query_whitelist()
    assert whitelist == expected_whitelist

    whitelist = client.query_whitelist()
    assert whitelist == expected_whitelist
    sg_client.query_contract.assert_called_once_with(test_whitelist_addr, {"config": {}})

@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_given_no_whitelist_when_query_whitelist_return_none(sg_client):
    client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)
    client._minter_config = MinterConfig.from_data(test_minter_config_data)
    client._minter_config.whitelist = None

    whitelist = client.query_whitelist()
    assert whitelist is None

@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_minted_tokens(sg_client):
    client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)
    sg_client.query_contract.side_effect = [
        {"data": {"tokens": [1, 2, 3]}},
        {"data": {"tokens": [4, 5, 6]}},
        {"data": {"tokens": []}},
    ]

    tokens = client.fetch_minted_tokens(limit=3)
    assert tokens == [1, 2, 3, 4, 5, 6]

@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_token_owner(sg_client):
    client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)

    sg_client.query_contract.return_value = {"data": {"owner": test_owner}}

    owner = client.fetch_owner_of_token(1)
    assert owner == test_owner

    sg_client.query_contract.assert_called_once_with(test_sg721_addr, {"owner_of": {"token_id": "1"}})

@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_num_minted(sg_client):
    client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)

    sg_client.query_contract.return_value = {"data": {"count": 3}}

    assert client.fetch_num_minted_tokens() == 3
    sg_client.query_contract.assert_called_once_with(test_sg721_addr, {"num_tokens": {}})

@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_query_contract_info(sg_client):
    client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)

    sg_client.query_contract.return_value = {"data": test_sg721_contract_info_data}

    contract_info = client.query_contract_info()
    assert contract_info == test_sg721_contract_info_data

    sg_client.query_contract.assert_called_once_with(test_sg721_addr, {"contract_info": {}})

    # def query_nft_info(self, token_id: str):
    #     return self.query_sg721({'all_nft_info': {'token_id': token_id}})

# @mock.patch("stargazeutils.StargazeClient")
# def test_sg721_client_should_create_minted_tokens_list(sg_client):
#     client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)
#     client._minter_config = MinterConfig.from_data(test_minter_config_data)
#     client._minter_config.num_tokens = 5

#     minted_tokens = client.create_minted_tokens_list()
#     assert minted_tokens == [1, 2, 3, 4, 5]

@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_holders(sg_client):
    client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)

    sg_client.query_contract.side_effect = [
        {"data": {"tokens": [1, 2, 3]}},
        {"data": {"owner": "owner1", "approvals": []}},
        {"data": {"owner": "owner2", "approvals": []}},
        {"data": {"owner": "owner1", "approvals": []}}
    ]

    holders = client.fetch_holders()
    assert holders == {"owner1", "owner2"}

    sg_client.query_contract.assert_called_with(test_sg721_addr, {"owner_of": {"token_id": 3}})



@mock.patch("stargazeutils.ipfs.get")
@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_traits(sg_client, ipfs_get_mock):
    client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)
    client._minter_config = MinterConfig.from_data(test_minter_config_data)
    client._minter_config.num_tokens = len(test_token_metadata)

    ipfs_get_mock.side_effect = [MockResponse(m) for m in test_token_metadata]
    traits = client.fetch_traits()

    assert len(traits) == len(test_token_traits)
    for token in traits:
        expected_token = test_token_traits[token['id']]
        assert len(token) == len(expected_token)
        for k,v in token.items():
            assert v == expected_token[k]

@mock.patch("stargazeutils.ipfs.get")
@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_traits(sg_client, ipfs_get_mock):
    client = Sg721Client(test_sg721_addr, test_minter_addr, sg_client)
    client._minter_config = MinterConfig.from_data(test_minter_config_data)
    client._minter_config.num_tokens = len(test_token_metadata)
    ipfs_get_mock.side_effect = [MockResponse(m) for m in test_token_metadata]

    rarity = client.fetch_trait_rarity()
    assert len(rarity) == len(test_rarity)
    for trait,values in rarity.items():
        assert len(values) == len(test_rarity[trait])
        for value,count in values.items():
            assert count == test_rarity[trait][value]
