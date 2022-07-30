import logging
from datetime import datetime
from enum import Enum

from ..coin import Coin
from ..common import DEFAULT_MARKET_CONTRACT, timestamp_from_str

LOG = logging.getLogger(__name__)


class SaleType(Enum):
    UNSUPPORTED = 1
    FIXED_PRICE = 2

    @classmethod
    def from_str(cls, s):
        if s == "fixed_price":
            return cls.FIXED_PRICE
        return cls.UNSUPPORTED


class InvalidAskReason(Enum):
    VALID = 0
    NOT_ACTIVE = 1
    LISTING_EXPIRED = 2
    LISTING_RESERVED = 3
    NOT_OWNED_BY_SELLER = 4
    NOT_APPROVED = 5
    APPROVAL_EXPIRED = 6


class MarketAsk:
    def __init__(
        self,
        collection: str,
        token_id: int,
        seller: str,
        price: Coin,
        expiration: datetime,
        sale_type: SaleType = SaleType.FIXED_PRICE,
        funds_recipient: str = None,
        reserve_for: str = None,
        is_active: bool = True,
    ):
        self.collection = collection
        self.token_id = token_id
        self.seller = seller
        self.price = price
        self.expiration = expiration
        self.sale_type = sale_type
        self.funds_recipient = funds_recipient or self.seller
        self.reserve_for = reserve_for
        self.is_active = is_active
        self.owner = None
        self.approvals = None
        self.reason = InvalidAskReason.VALID

    def is_valid(self, market_contract=DEFAULT_MARKET_CONTRACT):
        if not self.is_active:
            self.reason = InvalidAskReason.NOT_ACTIVE

        elif self.expiration < datetime.utcnow():
            self.reason = InvalidAskReason.LISTING_EXPIRED

        elif self.reserve_for is not None:
            self.reason = InvalidAskReason.LISTING_RESERVED

        elif self.owner is not None and self.owner != self.seller:
            self.reason = InvalidAskReason.NOT_OWNED_BY_SELLER

        elif self.approvals is not None:
            approval_list = {
                a["spender"]: timestamp_from_str(a["expires"]["at_time"])
                for a in self.approvals
            }
            if market_contract not in approval_list:
                self.reason = InvalidAskReason.NOT_APPROVED

            elif approval_list[market_contract] <= datetime.utcnow():
                self.reason = InvalidAskReason.APPROVAL_EXPIRED

        if self.reason is not InvalidAskReason.VALID:
            LOG.warning(f"#{self.token_id} {self.reason.name}")
            return False

        return True

    @property
    def marketplace_url(self):
        return (
            f"https://app.stargaze.zone/marketplace/{self.collection}/{self.token_id}"
        )

    def __repr__(self):
        return (
            f"<MarketAsk for {self.collection} token {self.token_id} of {self.price}>"
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

    @classmethod
    def from_dict(cls, data: dict):
        sale_type = SaleType.from_str(data["sale_type"])
        price = Coin.from_ustars(data["price"])
        expiration = timestamp_from_str(data["expires_at"])

        return cls(
            collection=data["collection"],
            token_id=data["token_id"],
            seller=data["seller"],
            price=price,
            expiration=expiration,
            sale_type=sale_type,
            funds_recipient=data["funds_recipient"],
            reserve_for=data["reserve_for"],
            is_active=data["is_active"],
        )
