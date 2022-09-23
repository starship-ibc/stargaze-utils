import logging

from ..coin import Coin

LOG = logging.getLogger(__name__)


class MarketBid:
    def __init__(
        self,
        collection: str,
        token_id: int,
        seller: str,
        buyer: str,
        price: Coin,
        collection_name: str = None,
        tx_hash: str = None,
    ):
        self.collection = collection
        self.collection_name = collection_name or collection
        self.token_id = token_id
        self.buyer = buyer
        self.seller = seller
        self.price = price
        self.tx_hash = tx_hash

    def __repr__(self):
        return (
            f"<MarketBid for {self.collection_name} token "
            f"{self.token_id} @ {self.price}>"
        )

    def __eq__(self, o: object) -> bool:
        if type(o) is not type(self):
            return False
        if len(self.__dict__) != len(o.__dict__):
            return False
        for k, v in self.__dict__.items():
            if k not in o.__dict__:
                return False
            if v != o.__dict__[k]:
                print(f"{v} != {o.__dict__[k]}")
                return False
        return True

    def to_serializable(self):
        return {
            "collection": self.collection,
            "collection_name": self.collection_name,
            "token_id": self.token_id,
            "seller": self.seller,
            "buyer": self.buyer,
            "price": self.price.to_serializable(),
            "tx_hash": self.tx_hash,
        }
