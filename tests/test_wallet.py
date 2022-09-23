import json
from datetime import datetime, timedelta
from unittest import mock

from stargazeutils.coin import Coin
from stargazeutils.market import MarketAsk
from stargazeutils.wallet import Wallet

FUTURE = datetime.utcnow() + timedelta(5)


@mock.patch("subprocess.check_output")
def test_wallet_should_get_balances(mock_cli):
    wallet = Wallet("stars1")

    expected_balances = [
        {"amount": "123000000", "denom": "ustars"},
        {"amount": "321000000", "denom": "uatom"},
    ]

    mock_cli.return_value = json.dumps({"balances": expected_balances})
    coins = wallet.get_coins()

    assert len(coins) == len(expected_balances)
    assert coins[0] == Coin(
        expected_balances[0]["amount"], expected_balances[0]["denom"]
    )
    assert coins[1] == Coin(
        expected_balances[1]["amount"], expected_balances[1]["denom"]
    )


@mock.patch("subprocess.check_output")
def test_wallet_should_bid_on_ask_auto_sign(mock_cli: mock.MagicMock):
    wallet = Wallet("stars1")
    ask = MarketAsk("c1", 1, "stars2", Coin.from_stars(100), FUTURE)

    expected_hash = "ABCD"
    mock_cli.return_value = json.dumps({"txhash": expected_hash})
    hash = wallet.set_bid_from_ask(ask, True)

    assert hash == expected_hash
    args = mock_cli.call_args_list[0].args[0]
    assert ["--from", wallet.address] == args[8:10]
    assert "--yes" in args


@mock.patch("subprocess.check_output")
def test_wallet_should_bid_on_ask_no_auto_sign(mock_cli: mock.MagicMock):
    wallet = Wallet("stars1")
    ask = MarketAsk("c1", 1, "stars2", Coin.from_stars(100), FUTURE)

    expected_hash = "ABCD"
    mock_cli.return_value = json.dumps({"txhash": expected_hash})
    hash = wallet.set_bid_from_ask(ask)

    assert hash == expected_hash
    args = mock_cli.call_args_list[0].args[0]
    assert ["--from", wallet.address] == args[8:10]
    assert "--yes" not in args


@mock.patch("subprocess.check_output")
def test_wallet_should_transfer_auto_sign(mock_cli: mock.MagicMock):
    wallet = Wallet("stars1")

    expected_hash = "ABCD"
    mock_cli.return_value = json.dumps({"txhash": expected_hash})
    hash = wallet.transfer_nft("c1", 1, "stars2", True)

    assert hash == expected_hash
    args = mock_cli.call_args_list[0].args[0]
    assert ["--from", wallet.address] == args[6:8]
    assert "--yes" in args


@mock.patch("subprocess.check_output")
def test_wallet_should_transfer_no_auto_sign(mock_cli):
    wallet = Wallet("stars1")

    expected_hash = "ABCD"
    mock_cli.return_value = json.dumps({"txhash": expected_hash})
    hash = wallet.transfer_nft("c1", 1, "stars2")

    assert hash == expected_hash
    args = mock_cli.call_args_list[0].args[0]
    assert ["--from", wallet.address] == args[6:8]
    assert "--yes" not in args


@mock.patch("subprocess.check_output")
def test_wallet_should_send_funds_no_auto_sign(mock_cli: mock.MagicMock):
    wallet = Wallet("stars1")

    expected_hash = "ABCD"
    mock_cli.return_value = json.dumps({"txhash": expected_hash})
    hash = wallet.send_funds(Coin.from_stars(12), "stars2")

    assert hash == expected_hash
    args = mock_cli.call_args_list[0].args[0]
    assert [
        "starsd",
        "tx",
        "bank",
        "send",
        wallet.address,
        "stars2",
        "12000000ustars",
        "--node",
        wallet.sg_client.node,
        "--chain-id",
        wallet.sg_client.chain_id,
        "--output",
        "json",
    ] == args


@mock.patch("subprocess.check_output")
def test_wallet_should_send_funds_auto_sign(mock_cli: mock.MagicMock):
    wallet = Wallet("stars1")

    expected_hash = "ABCD"
    mock_cli.return_value = json.dumps({"txhash": expected_hash})
    hash = wallet.send_funds(Coin.from_stars(12), "stars2", True)

    assert hash == expected_hash
    args = mock_cli.call_args_list[0].args[0]
    assert [
        "starsd",
        "tx",
        "bank",
        "send",
        wallet.address,
        "stars2",
        "12000000ustars",
        "--node",
        wallet.sg_client.node,
        "--chain-id",
        wallet.sg_client.chain_id,
        "--yes",
        "--output",
        "json",
    ] == args
