from unittest import mock

from stargazeutils.cache.sg721_info import SG721Info
from stargazeutils.collection import Sg721Client
from stargazeutils.collection.collection_info import CollectionInfo
from stargazeutils.collection.minter_config import MinterConfig
from stargazeutils.collection.whitelist import Whitelist
from tests.mock_response import MockResponse

from ..assets import test_vals


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_tokens_owned_by(sg_client):
    client = Sg721Client(test_vals.sg721_addr, test_vals.minter_addr, sg_client)

    sg_client.query_contract.side_effect = [
        {"data": {"tokens": [1, 2, 3]}},
        {"data": {"tokens": []}},
    ]
    tokens = client.query_tokens_owned_by(test_vals.owner)

    assert tokens == [1, 2, 3]


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_query_minter_given_none(sg_client):
    sg_client.fetch_sg721_minter.return_value = test_vals.minter_addr
    client = Sg721Client(test_vals.sg721_addr, sg_client=sg_client)
    assert client.minter == test_vals.minter_addr


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_query_minter_config_once(sg_client):
    client = Sg721Client(test_vals.sg721_addr, test_vals.minter_addr, sg_client)

    expected_minter_config = MinterConfig.from_data(test_vals.minter_config_data)
    sg_client.query_contract.return_value = {"data": test_vals.minter_config_data}

    minter_config = client.query_minter_config()
    assert minter_config == expected_minter_config

    minter_config = client.query_minter_config()
    assert minter_config == expected_minter_config
    sg_client.query_contract.assert_called_once_with(
        test_vals.minter_addr, {"config": {}}
    )


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_query_collection_info_once(sg_client):
    client = Sg721Client(test_vals.sg721_addr, test_vals.minter_addr, sg_client)

    expected_collection_info = CollectionInfo.from_data(test_vals.collection_info_data)
    sg_client.query_contract.return_value = {"data": test_vals.collection_info_data}

    collection_info = client.query_collection_info()
    assert collection_info == expected_collection_info

    collection_info = client.query_collection_info()
    assert collection_info == expected_collection_info
    sg_client.query_contract.assert_called_once_with(
        test_vals.sg721_addr, {"collection_info": {}}
    )


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_query_whitelist_once(sg_client):
    client = Sg721Client(test_vals.sg721_addr, test_vals.minter_addr, sg_client)
    client._minter_config = MinterConfig.from_data(test_vals.minter_config_data)

    expected_whitelist = Whitelist.from_data(test_vals.whitelist_data)
    sg_client.query_contract.return_value = {"data": test_vals.whitelist_data}

    whitelist = client.query_whitelist()
    assert whitelist == expected_whitelist

    whitelist = client.query_whitelist()
    assert whitelist == expected_whitelist
    sg_client.query_contract.assert_called_once_with(
        test_vals.whitelist_addr, {"config": {}}
    )


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_given_no_whitelist_when_query_whitelist_return_none(sg_client):
    client = Sg721Client(test_vals.sg721_addr, test_vals.minter_addr, sg_client)
    client._minter_config = MinterConfig.from_data(test_vals.minter_config_data)
    client._minter_config.whitelist = None

    whitelist = client.query_whitelist()
    assert whitelist is None


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_minted_tokens(sg_client):
    client = Sg721Client(test_vals.sg721_addr, test_vals.minter_addr, sg_client)
    sg_client.query_contract.side_effect = [
        {"data": {"tokens": [1, 2, 3]}},
        {"data": {"tokens": [4, 5, 6]}},
        {"data": {"tokens": []}},
    ]

    tokens = client.fetch_minted_tokens(limit=3)
    assert tokens == [1, 2, 3, 4, 5, 6]


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_token_owner(sg_client):
    client = Sg721Client(test_vals.sg721_addr, test_vals.minter_addr, sg_client)

    sg_client.query_contract.return_value = {"data": {"owner": test_vals.owner}}

    owner = client.query_owner_of_token(1)
    assert owner == test_vals.owner

    sg_client.query_contract.assert_called_once_with(
        test_vals.sg721_addr, {"owner_of": {"token_id": "1"}}
    )


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_num_minted(sg_client):
    client = Sg721Client(test_vals.sg721_addr, test_vals.minter_addr, sg_client)

    sg_client.query_contract.return_value = {"data": {"count": 3}}

    assert client.query_num_minted_tokens() == 3
    sg_client.query_contract.assert_called_once_with(
        test_vals.sg721_addr, {"num_tokens": {}}
    )


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_query_contract_info(sg_client):
    client = Sg721Client(test_vals.sg721_addr, test_vals.minter_addr, sg_client)

    sg_client.query_contract.return_value = {"data": test_vals.sg721_contract_info_data}

    contract_info = client.query_contract_info()
    assert contract_info == test_vals.sg721_contract_info_data

    sg_client.query_contract.assert_called_once_with(
        test_vals.sg721_addr, {"contract_info": {}}
    )

    # def query_nft_info(self, token_id: str):
    #     return self.query_sg721({'all_nft_info': {'token_id': token_id}})


# @mock.patch("stargazeutils.StargazeClient")
# def test_sg721_client_should_create_minted_tokens_list(sg_client):
#     client = Sg721Client(test_vals.test_sg721_addr, \
#           test_vals.test_minter_addr, sg_client)
#     client._minter_config = MinterConfig.from_data(test_vals.test_minter_config_data)
#     client._minter_config.num_tokens = 5

#     minted_tokens = client.create_minted_tokens_list()
#     assert minted_tokens == [1, 2, 3, 4, 5]


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_holders(sg_client):
    client = Sg721Client(test_vals.sg721_addr, test_vals.minter_addr, sg_client)

    sg_client.query_contract.side_effect = [
        {"data": {"tokens": [1, 2, 3]}},
        {"data": {"owner": "owner1", "approvals": []}},
        {"data": {"owner": "owner2", "approvals": []}},
        {"data": {"owner": "owner1", "approvals": []}},
    ]

    holders = client.fetch_holders()
    assert holders == {"owner1", "owner2"}

    sg_client.query_contract.assert_called_with(
        test_vals.sg721_addr, {"owner_of": {"token_id": 3}}
    )


@mock.patch("stargazeutils.StargazeClient")
@mock.patch("stargazeutils.ipfs.IpfsClient")
def test_sg721_client_should_fetch_nft_collection(sg_client, ipfs_client):
    client = Sg721Client(
        test_vals.sg721_addr, test_vals.minter_addr, sg_client, ipfs_client
    )
    client._minter_config = MinterConfig.from_data(test_vals.minter_config_data)
    client._minter_config.num_tokens = len(test_vals.token_metadata)

    ipfs_client.get.side_effect = [MockResponse(m) for m in test_vals.token_metadata]
    collection = client.fetch_nft_collection()

    assert len(collection.tokens) == len(test_vals.token_traits)
    for id, token in collection.tokens.items():
        expected_token = test_vals.token_traits[id]
        assert len(token) == len(expected_token)
        for k, v in token.items():
            assert v == expected_token[k]


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_fetch_nft_collection_from_json(sg_client):
    client = Sg721Client(test_vals.sg721_addr, test_vals.minter_addr, sg_client)
    client._minter_config = MinterConfig.from_data(test_vals.minter_config_data)
    client._minter_config.num_tokens = len(test_vals.token_metadata)

    c = client.fetch_nft_collection(test_vals.collection_file)
    assert c.sg721 == test_vals.sg721_addr
    assert c.tokens[1] == {"id": 1, "Color": "blue", "Type": "electric"}
    assert c.tokens[2] == {"id": 2, "Color": "blue", "Type": "water"}
    assert c.tokens[3] == {"id": 3, "Color": "red", "Type": "fire"}
    assert c.tokens[4] == {"id": 4, "Color": "yellow", "Type": "electric"}


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_create_from_collection_name(sg_client):
    sg_client.get_sg721_info.return_value = SG721Info(
        test_vals.sg721_addr, test_vals.collection_name
    )
    client = Sg721Client.from_collection_name(test_vals.collection_name, sg_client)

    assert client.sg721 == test_vals.sg721_addr


@mock.patch("stargazeutils.StargazeClient")
def test_sg721_client_should_return_none_when_collection_name_not_found(sg_client):
    sg_client.get_sg721_info.return_value = None
    client = Sg721Client.from_collection_name(test_vals.collection_name, sg_client)

    assert client is None


@mock.patch("stargazeutils.StargazeClient")
@mock.patch("stargazeutils.ipfs.IpfsClient")
def test_sg721_client_should_fetch_traitless_nft_collection(sg_client, ipfs_client):
    client = Sg721Client(
        test_vals.sg721_addr, test_vals.minter_addr, sg_client, ipfs_client
    )
    client._minter_config = MinterConfig.from_data(test_vals.minter_config_data)
    client._minter_config.num_tokens = len(test_vals.traitless_token_metadata)

    ipfs_client.get.side_effect = [
        MockResponse(m) for m in test_vals.traitless_token_metadata
    ]
    collection = client.fetch_nft_collection()

    assert len(collection.tokens) == len(test_vals.traitless_token_metadata)
    for id, token in collection.tokens.items():
        expected_token = test_vals.traitless_token_traits[id]
        assert len(token) == len(expected_token)
        for k, v in token.items():
            assert v == expected_token[k]
