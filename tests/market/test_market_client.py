from datetime import datetime
from unittest import mock

from stargazeutils.coin import Coin
from stargazeutils.common import DEFAULT_MARKET_CONTRACT
from stargazeutils.market import MarketClient
from stargazeutils.market.market_ask import MarketAsk
from tests.assets import test_sales, test_vals


@mock.patch("stargazeutils.StargazeClient")
def test_market_client_should_fetch_bids_by_bidder(sg_client):
    # return self.sg_client.query_contract(self.contract, query)
    expected_query = {"bids_by_bidder": {"bidder": test_vals.sg721_addr}}
    sg_client.query_contract.return_value = {"bids: []"}
    client = MarketClient(DEFAULT_MARKET_CONTRACT, sg_client)
    client.fetch_bids_by_bidder(test_vals.sg721_addr)

    sg_client.query_contract.assert_called_once_with(DEFAULT_MARKET_CONTRACT, expected_query)


@mock.patch("stargazeutils.StargazeClient")
def test_market_client_should_fetch_ask_for_token(sg_client):
    expected_query = {
        "ask": {"collection": test_vals.sg721_addr, "token_id": test_vals.sale_token_id}
    }
    sg_client.query_contract.return_value = test_vals.market_ask
    client = MarketClient(DEFAULT_MARKET_CONTRACT, sg_client)
    ask = client.fetch_ask_for_token(test_vals.sg721_addr, test_vals.sale_token_id)

    sg_client.query_contract.assert_called_once_with(DEFAULT_MARKET_CONTRACT, expected_query)
    assert ask == MarketAsk.from_dict(test_vals.market_ask)


@mock.patch("stargazeutils.StargazeClient")
@mock.patch("stargazeutils.collection.NFTCollection")
def test_market_client_should_fetch_asks_for_collection(sg_client, mock_nft_collection):
    expected_query = {
        "asks": {"collection": test_vals.sg721_addr, "start_after": 1, "limit": 100}
    }
    sg_client.query_contract.side_effect = [
        {"data": {"asks": [test_vals.market_ask]}},
        {"data": {"asks": []}},
    ]
    client = MarketClient(DEFAULT_MARKET_CONTRACT, sg_client)
    mock_nft_collection.sg721 = test_vals.sg721_addr
    asks = client.fetch_asks_for_collection(mock_nft_collection)

    sg_client.query_contract.assert_called_with(DEFAULT_MARKET_CONTRACT, expected_query)
    assert asks.asks[0] == MarketAsk.from_dict(test_vals.market_ask)


@mock.patch("stargazeutils.StargazeClient")
@mock.patch("stargazeutils.collection.NFTCollection")
def test_market_client_when_fetch_asks_for_collection_should_strict_verify(
    sg_client, mock_nft_collection
):
    expected_query = {
        "asks": {"collection": test_vals.sg721_addr, "start_after": 1, "limit": 100}
    }
    expected_ask = MarketAsk.from_dict(test_vals.market_ask)
    approvals = [
        {
            "spender": DEFAULT_MARKET_CONTRACT,
            "expires": {"at_time": test_vals.future_timestamp_str},
        }
    ]
    expected_ask.approvals = approvals
    expected_ask.owner = expected_ask.seller
    sg_client.query_contract.side_effect = [
        {"data": {"asks": [test_vals.market_ask]}},
        {"data": {"owner": expected_ask.owner, "approvals": approvals}},
        {"data": {"asks": []}},
    ]
    client = MarketClient(DEFAULT_MARKET_CONTRACT, sg_client)
    mock_nft_collection.sg721 = test_vals.sg721_addr
    asks = client.fetch_asks_for_collection(mock_nft_collection, strict_verify=True)

    sg_client.query_contract.assert_called_with(DEFAULT_MARKET_CONTRACT, expected_query)
    assert asks.asks[0] == expected_ask


@mock.patch("stargazeutils.StargazeClient")
@mock.patch("stargazeutils.collection.NFTCollection")
def test_market_client_fetch_asks_strict_verify_custom_marketplace(
    sg_client, mock_nft_collection
):
    market_contract = "new-contract"
    expected_query = {
        "asks": {"collection": test_vals.sg721_addr, "start_after": 1, "limit": 100}
    }
    expected_ask = MarketAsk.from_dict(test_vals.market_ask)
    approvals = [
        {
            "spender": market_contract,
            "expires": {"at_time": test_vals.future_timestamp_str},
        }
    ]
    expected_ask.approvals = approvals
    expected_ask.owner = expected_ask.seller
    sg_client.query_contract.side_effect = [
        {"data": {"asks": [test_vals.market_ask]}},
        {"data": {"owner": expected_ask.owner, "approvals": approvals}},
        {"data": {"asks": []}},
    ]
    client = MarketClient(market_contract, sg_client)
    mock_nft_collection.sg721 = test_vals.sg721_addr
    asks = client.fetch_asks_for_collection(mock_nft_collection, strict_verify=True)

    sg_client.query_contract.assert_called_with(market_contract, expected_query)
    assert asks.asks[0] == expected_ask

@mock.patch("stargazeutils.StargazeClient")
@mock.patch("stargazeutils.collection.NFTCollection")
def test_market_client_should_fetch_filtered_asks(sg_client, mock_nft_collection):
    expected_query = {"ask": {"collection": test_vals.sg721_addr, "token_id": 1}}
    sg_client.query_contract.side_effect = [test_vals.market_ask, []]
    client = MarketClient(DEFAULT_MARKET_CONTRACT, sg_client)
    mock_nft_collection.filter_tokens.return_value = {1}
    mock_nft_collection.sg721 = test_vals.sg721_addr
    asks = client.fetch_filtered_asks(mock_nft_collection, {})

    sg_client.query_contract.assert_called_once_with(DEFAULT_MARKET_CONTRACT, expected_query)
    assert len(asks.asks) == 1

    expected_ask = MarketAsk.from_dict(test_vals.market_ask)
    assert asks.asks[0] == expected_ask


@mock.patch("stargazeutils.StargazeClient")
def test_market_client_should_fetch_sales(sg_client, requests_mock):
    sg_client.rest_url = "https://stargaze"
    client = MarketClient(DEFAULT_MARKET_CONTRACT, sg_client)

    requests_mock.get(sg_client.rest_url + "/txs", json=test_sales.sales)

    sales = client.fetch_collection_sales(test_vals.sg721_addr)
    assert len(sales) == 1

    expected_sale = test_sales.sales["txs"][0]
    sale = sales[0]
    assert sale.token_id == "6681"
    assert sale.price == Coin.from_stars(1300)
    assert sale.tx_hash == expected_sale["txhash"]
    assert sale.seller == "seller-1"
    assert sale.buyer == "buyer-1"
    assert sale.timestamp == datetime.strptime(
        expected_sale["timestamp"], "%Y-%m-%dT%H:%M:%SZ"
    )
    assert sale.height == expected_sale["height"]
