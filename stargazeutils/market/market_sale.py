import logging
from datetime import datetime

from ..coin import Coin

LOG = logging.getLogger(__name__)


class MarketSale:
    """Represents a sale of an NFT on Stargaze."""

    def __init__(
        self,
        tx_hash: str,
        timestamp: datetime,
        height,
        token_id,
        price: Coin,
        seller: str,
        buyer: str,
    ):
        """Initializes a MarketSale

        :param tx_hash: The transaction has for the sale
        :param timestamp: When the sale was fulfilled
        :param height: The blockchain height of the sale
        :param token_id: The token id that was sold
        :param price: The price of the sale
        :param seller: The seller's stars address
        :param buyer: The buyer's stars address
        """
        self.tx_hash = tx_hash
        self.token_id = token_id
        self.timestamp: datetime = timestamp
        self.height = height
        self.price = price
        self.seller = seller
        self.buyer = buyer

    @staticmethod
    def export_sales_csv(sales, csv_name: str):
        """Exports a list of sales as an CSV

        :param sales: The list of sales to export
        :param csv_name: The name of the csv file
        """
        LOG.info(f"Exporting {len(sales)} sales to {csv_name}")
        sales.sort(key=lambda s: s.timestamp)
        with open(csv_name, "w") as f:
            f.write(MarketSale.get_csv_header() + "\n")
            for sale in sales:
                f.write(sale.get_csv_line())
                f.write("\n")

    @staticmethod
    def get_csv_header() -> str:
        """Gets the CSV header"""
        return '"timestamp","height", "token_id","tx_hash","price","seller","buyer"'

    def get_csv_line(self) -> str:
        """Gets a line for a CSV file"""
        return (
            f'"{self.timestamp}","{self.height}","{self.token_id}","{self.tx_hash}",'
            f'"{self.price}","{self.seller}","{self.buyer}"'
        )

    def __repr__(self):
        return f"<token_id={self.token_id} price={self.price}>"

    def __str__(self):
        return f"Spunk #{self.token_id:4} @ {self.price:6} $STARS [{self.tx_hash}]"

    @classmethod
    def from_tx(cls, tx: dict):
        """Initializes a MarketSale from transaction data. This
        expects the transaction to have a wasm-finalize-sale event.

        :param tx: The tx data dictionary
        :return the MarketSale
        :rtype MarketSale
        """
        events = tx["logs"][0]["events"]
        timestamp = datetime.strptime(tx["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        attrs = []
        for event in events:
            if event["type"] == "wasm-finalize-sale":
                attrs = event["attributes"]
                sale = {x["key"]: x["value"] for x in attrs}
                return cls(
                    tx["txhash"],
                    timestamp,
                    tx["height"],
                    sale["token_id"],
                    Coin.from_ustars(sale["price"]),
                    sale["seller"],
                    sale["buyer"],
                )
