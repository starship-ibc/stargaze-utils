import os
from datetime import datetime

from stargazeutils.coin import Coin
from stargazeutils.market.market_sale import MarketSale
from tests.assets import test_vals


def test_market_sale_should_parse_transaction():
    sale = MarketSale.from_tx(test_vals.sale_tx)
    assert sale.buyer == test_vals.sale_buyer
    assert sale.height == test_vals.sale_height
    assert sale.price == Coin.from_ustars(test_vals.sale_price)
    assert sale.seller == test_vals.sale_seller
    assert sale.timestamp == test_vals.sale_timestamp
    assert sale.token_id == test_vals.sale_token_id
    assert sale.tx_hash == test_vals.sale_tx_hash


def test_market_sale_should_export_csv():
    sales = [
        MarketSale(
            "tx-1",
            datetime.utcnow(),
            "123",
            "1",
            Coin.from_stars(100),
            "seller-1",
            "buyer-1",
        ),
        MarketSale(
            "tx-2",
            datetime.utcnow(),
            "123",
            "2",
            Coin.from_stars(200),
            "seller-1",
            "buyer-1",
        ),
    ]
    filename = "test-sales.csv"
    assert not os.path.exists(filename)
    try:
        MarketSale.export_sales_csv(sales, filename)
        assert os.path.exists(filename)
    finally:
        os.remove(filename)
    assert not os.path.exists(filename)
