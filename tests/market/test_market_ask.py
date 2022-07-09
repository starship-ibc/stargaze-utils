from datetime import datetime, timedelta

from stargazeutils.coin import Coin
from stargazeutils.common import EPOCH, MARKET_CONTRACT, timestamp_from_str
from stargazeutils.market.market_ask import InvalidAskReason, MarketAsk, SaleType

from ..assets import test_vals


def test_sale_type_from_string():
    assert SaleType.from_str("fixed_price") == SaleType.FIXED_PRICE
    assert SaleType.from_str("any") == SaleType.UNSUPPORTED


def test_market_ask_is_valid_when_not_strict():
    ask = MarketAsk.from_dict(test_vals.market_ask)
    ask.expiration = datetime.utcnow() + timedelta(1)
    assert ask.is_valid()


def test_market_ask_is_valid_when_strict():
    ask = MarketAsk.from_dict(test_vals.market_ask)
    ask.expiration = datetime.utcnow() + timedelta(1)
    ask.owner = test_vals.market_ask["seller"]

    expiration = str(int((ask.expiration - EPOCH).total_seconds() * 10000)) + "00000"
    ask.approvals = [{"spender": MARKET_CONTRACT, "expires": {"at_time": expiration}}]
    assert ask.is_valid()


def test_market_ask_is_invalid_when_not_active():
    ask = MarketAsk.from_dict(test_vals.market_ask)
    ask.expiration = datetime.utcnow() + timedelta(1)
    ask.is_active = False
    assert not ask.is_valid()
    assert ask.reason == InvalidAskReason.NOT_ACTIVE


def test_market_ask_is_invalid_when_expired():
    ask = MarketAsk.from_dict(test_vals.market_ask)
    ask.expiration = ask.expiration - timedelta(60)
    assert not ask.is_valid()
    assert ask.reason == InvalidAskReason.LISTING_EXPIRED


def test_market_ask_is_invalid_when_reserved():
    ask = MarketAsk.from_dict(test_vals.market_ask)
    ask.expiration = datetime.utcnow() + timedelta(1)
    ask.reserve_for = "buyer-1"
    assert not ask.is_valid()
    assert ask.reason == InvalidAskReason.LISTING_RESERVED


def test_market_ask_is_invalid_when_not_owned_by_seller():
    ask = MarketAsk.from_dict(test_vals.market_ask)
    ask.expiration = datetime.utcnow() + timedelta(1)
    ask.owner = "owner-1"
    assert not ask.is_valid()
    assert ask.reason == InvalidAskReason.NOT_OWNED_BY_SELLER


def test_market_ask_is_invalid_when_market_not_approved():
    ask = MarketAsk.from_dict(test_vals.market_ask)
    ask.expiration = datetime.utcnow() + timedelta(1)
    ask.approvals = []
    assert not ask.is_valid()
    assert ask.reason == InvalidAskReason.NOT_APPROVED


def test_market_ask_is_invalid_when_market_approval_expired():
    ask = MarketAsk.from_dict(test_vals.market_ask)
    ask.expiration = datetime.utcnow() + timedelta(1)
    ask.approvals = [
        {"spender": MARKET_CONTRACT, "expires": {"at_time": "1642999240605000000"}}
    ]
    assert not ask.is_valid()
    assert ask.reason == InvalidAskReason.APPROVAL_EXPIRED


def test_market_ask_should_parse_json():
    ask = MarketAsk.from_dict(test_vals.market_ask)
    assert ask.sale_type == SaleType.FIXED_PRICE
    assert ask.collection == test_vals.market_ask["collection"]
    assert ask.expiration == timestamp_from_str(test_vals.future_timestamp_str)
    assert ask.funds_recipient == test_vals.market_ask["funds_recipient"]
    assert ask.is_active == test_vals.market_ask["is_active"]
    assert ask.price == Coin.from_stars(15000)
    assert ask.reserve_for is None
    assert ask.token_id == test_vals.market_ask["token_id"]
