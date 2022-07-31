import os
import shutil
from unittest import mock
from unittest.mock import MagicMock

from stargazeutils.cache.sg721_cache import SG721Cache
from stargazeutils.cache.sg721_info import SG721Info
from stargazeutils.stargaze import QueryMethod, StargazeClient

cache_file = "tests/assets/sg721_cache.csv"
cache_backup = "tests/assets/sg721_backup.csv"


def mock_starsd(*args, **kwargs):
    if args[0][3] == "list-contract-by-code":
        if args[0][5] == "1":
            return """
            {"contracts":["addr1", "addr2"],
            "pagination":{"next_key":"a","total":"0"}}
            """
        if args[0][5] == "2":
            return """
                {"contracts":["addr3", "addr4"],
                "pagination":{"next_key":"a","total":"0"}}
                """
        return '{"contracts":[],"pagination":{"next_key":null,"total":"0"}}'
    if args[0][5] == "addr3" in args[0]:
        if args[0][6] == '{"contract_info": {}}':
            return '{"data":{"name":"Collection 3", "symbol": "SYM3"} }'
        if args[0][6] == '{"minter": {}}':
            return '{"data": {"minter": "minter-1"} }'
    if args[0][5] == "addr4":
        if args[0][6] == '{"contract_info": {}}':
            return '{"data":{"name":"Collection 4", "symbol": "SYM4"} }'
        if args[0][6] == '{"minter": {}}':
            return '{"data": {"minter": "minter-1"} }'
    return None


@mock.patch("subprocess.check_output")
def test_stargazeclient_can_query_contract_via_binary(mock: MagicMock):
    mock.return_value = "{}"

    cache = SG721Cache(cache_file)
    client = StargazeClient(query_method=QueryMethod.BINARY, sg721_cache=cache)
    r = client.query_contract("contract", {"query": {}})

    expected_args = [
        "starsd",
        "query",
        "wasm",
        "contract-state",
        "smart",
        "contract",
        '{"query": {}}',
        "--node",
        client.node,
        "--chain-id",
        client.chain_id,
    ]
    assert r == {}
    mock.assert_called_once_with(expected_args)


def test_stargazeclient_can_query_contract_via_rest(requests_mock):
    cache = SG721Cache(cache_file)
    client = StargazeClient(query_method=QueryMethod.REST, sg721_cache=cache)

    contract = "testcontract"
    config_query = "eyJxdWVyeSI6IHt9fQ=="
    expected_url = (
        f"{client.rest_url}/cosmwasm/wasm/v1/contract/{contract}/smart/{config_query}"
    )
    requests_mock.get(expected_url, text='{"data": {}}')

    r = client.query_contract(contract, {"query": {}})
    assert r == {"data": {}}


@mock.patch("subprocess.check_output")
def test_stargazeclient_should_fetch_contracts(mock: MagicMock):
    mock.side_effect = [
        '{"contracts":["addr1", "addr2"],"pagination":{"next_key":"a","total":"0"}}',
        '{"contracts":[],"pagination":{"next_key":null,"total":"0"}}',
    ]

    cache = SG721Cache(cache_file)
    client = StargazeClient(query_method=QueryMethod.BINARY, sg721_cache=cache)
    code_id = 1
    r = client.fetch_contracts(code_id)

    expected_args = [
        "starsd",
        "query",
        "wasm",
        "list-contract-by-code",
        "--page",
        "2",
        str(code_id),
        "--node",
        client.node,
        "--chain-id",
        client.chain_id,
    ]

    assert r == ["addr1", "addr2"]
    mock.assert_called_with(expected_args)


@mock.patch("subprocess.check_output")
def test_stargazeclient_should_fetch_paginated_contracts(mock: MagicMock):
    mock.side_effect = [
        '{"contracts":["addr1", "addr2"],"pagination":{"next_key":"a","total":"0"}}',
        '{"contracts":["addr3"],"pagination":{"next_key":"b","total":"0"}}',
        '{"contracts":[],"pagination":{"next_key":null,"total":"0"}}',
    ]

    cache = SG721Cache(cache_file)
    client = StargazeClient(query_method=QueryMethod.BINARY, sg721_cache=cache)
    code_id = 1
    r = client.fetch_contracts(code_id)

    expected_args = [
        "starsd",
        "query",
        "wasm",
        "list-contract-by-code",
        "--page",
        "3",
        str(code_id),
        "--node",
        client.node,
        "--chain-id",
        client.chain_id,
    ]

    assert r == ["addr1", "addr2", "addr3"]
    mock.assert_called_with(expected_args)


@mock.patch("subprocess.check_output")
def test_stargazeclient_should_fetch_sg721_info(mock: MagicMock):
    addr = "test-addr2"
    name = "NFT Collection"
    symbol = "NFT"
    mock.return_value = '{"data":{"name":"' + name + '","symbol":"' + symbol + '"} }'

    cache = SG721Cache(cache_file)
    client = StargazeClient(query_method=QueryMethod.BINARY, sg721_cache=cache)
    info = client.fetch_sg721_contract_info(addr)

    expected_args = [
        "starsd",
        "query",
        "wasm",
        "contract-state",
        "smart",
        addr,
        '{"contract_info": {}}',
        "--node",
        client.node,
        "--chain-id",
        client.chain_id,
    ]

    mock.assert_called_once_with(expected_args)
    assert info.sg721 == addr
    assert info.name == name
    assert info.symbol == symbol


@mock.patch("subprocess.check_output")
def test_stargazeclient_should_use_cached_sg721_info(mock: MagicMock):
    addr = "test-addr"
    name = "NFT Collection"
    symbol = "NFT"
    mock.return_value = '{"data":{"name":"' + name + '","symbol":"' + symbol + '"} }'

    cache = SG721Cache(cache_file)
    client = StargazeClient(query_method=QueryMethod.BINARY, sg721_cache=cache)
    client.fetch_sg721_contract_info(addr)
    mock.assert_called_once()
    info = client.fetch_sg721_contract_info(addr)

    assert info.sg721 == addr
    assert info.name == name
    assert info.symbol == symbol


@mock.patch("subprocess.check_output")
def test_stargazeclient_should_fetch_minter(mock):
    addr = "test-addr2"
    minter = "minter-addr2"
    mock.return_value = '{"data":{"minter":"' + minter + '"} }'

    cache = SG721Cache(cache_file)
    client = StargazeClient(query_method=QueryMethod.BINARY, sg721_cache=cache)
    info = client.fetch_sg721_minter(addr)

    expected_args = [
        "starsd",
        "query",
        "wasm",
        "contract-state",
        "smart",
        addr,
        '{"minter": {}}',
        "--node",
        client.node,
        "--chain-id",
        client.chain_id,
    ]

    mock.assert_called_once_with(expected_args)
    assert info.sg721 == addr
    assert info.minter == minter


@mock.patch("subprocess.check_output")
def test_stargazeclient_should_use_cached_minter(mock):
    addr = "test-addr"
    minter = "minter-addr"
    mock.return_value = '{"data":{"minter":"' + minter + '"} }'

    cache = SG721Cache(cache_file)
    client = StargazeClient(query_method=QueryMethod.BINARY, sg721_cache=cache)
    client.fetch_sg721_minter(addr)
    mock.assert_called_once()
    info = client.fetch_sg721_minter(addr)

    assert info.sg721 == addr
    assert info.minter == minter


def test_stargazeclient_should_query_txs_via_rest(requests_mock):
    cache = SG721Cache(cache_file)
    client = StargazeClient(query_method=QueryMethod.REST, sg721_cache=cache)

    params = {"param_name": "param_value"}
    expected_url = f"{client.rest_url}/txs"
    requests_mock.get(expected_url, text='{"data": {}}')

    r = client.query_txs(params)
    assert r == {"data": {}}


@mock.patch("subprocess.check_output")
def test_stargazeclient_should_update_cache(mock):
    mock.side_effect = mock_starsd

    shutil.copyfile(cache_file, cache_backup)
    try:
        cache = SG721Cache(cache_file)
        client = StargazeClient(query_method=QueryMethod.BINARY, sg721_cache=cache)
        contracts = client.update_sg721_cache()
    finally:
        shutil.copyfile(cache_backup, cache_file)
        os.remove(cache_backup)

    assert len(contracts) == 4
    assert contracts[0]["contract"] == "addr1"
    assert not contracts[0]["is_new"]
    assert contracts[1]["contract"] == "addr2"
    assert not contracts[1]["is_new"]
    assert contracts[2]["contract"] == "addr3"
    assert contracts[2]["is_new"]
    assert contracts[3]["contract"] == "addr4"
    assert contracts[3]["is_new"]


@mock.patch("subprocess.check_output")
def test_stargazeclient_should_print_sg721_info(mock, capsys):
    mock.side_effect = mock_starsd

    shutil.copyfile(cache_file, cache_backup)
    try:
        cache = SG721Cache(cache_file)
        client = StargazeClient(query_method=QueryMethod.BINARY, sg721_cache=cache)
        client.print_sg721_info(only_new=False)
    finally:
        shutil.copyfile(cache_backup, cache_file)
        os.remove(cache_backup)

    captured = capsys.readouterr()
    assert "- name1" in captured.out
    assert "- name2" in captured.out
    assert "- Collection 3" in captured.out
    assert "- Collection 4" in captured.out


@mock.patch("subprocess.check_output")
def test_stargazeclient_should_print_sg721_info_given_no_new(mock, capsys):
    mock.side_effect = mock_starsd

    shutil.copyfile(cache_file, cache_backup)
    try:
        cache = SG721Cache(cache_file)
        client = StargazeClient(query_method=QueryMethod.BINARY, sg721_cache=cache)
        client.update_sg721_cache()
        client.print_sg721_info(only_new=True)
    finally:
        shutil.copyfile(cache_backup, cache_file)
        os.remove(cache_backup)

    captured = capsys.readouterr()
    assert "- name1" not in captured.out
    assert "- name2" not in captured.out
    assert "- Collection 3" not in captured.out
    assert "- Collection 4" not in captured.out


@mock.patch("subprocess.check_output")
def test_stargazeclient_should_print_only_new_sg721_info(mock, capsys):
    mock.side_effect = mock_starsd

    shutil.copyfile(cache_file, cache_backup)
    try:
        cache = SG721Cache(cache_file)
        client = StargazeClient(query_method=QueryMethod.BINARY, sg721_cache=cache)
        client.print_sg721_info(only_new=True)
    finally:
        shutil.copyfile(cache_backup, cache_file)
        os.remove(cache_backup)

    captured = capsys.readouterr()
    assert "- name1" not in captured.out
    assert "- name2" not in captured.out
    assert "- Collection 3" in captured.out
    assert "- Collection 4" in captured.out


@mock.patch("stargazeutils.cache.sg721_cache.SG721Cache")
def test_stargaze_client_should_get_sg721_info_from_collection_name(mock_cache):
    client = StargazeClient(query_method=QueryMethod.BINARY, sg721_cache=mock_cache)
    expected_info = SG721Info("sg721", "name", "sym", "mint")
    mock_cache.get_sg721_info_from_name.return_value = expected_info
    info = client.get_sg721_info(expected_info.name)

    assert info == expected_info
