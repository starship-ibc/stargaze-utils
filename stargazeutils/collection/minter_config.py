from datetime import datetime

from ..coin import Coin
from ..common import DATETIME_FMT, timestamp_from_str
from .whitelist import Whitelist


class MinterConfig:
    """Represents the minter configuration object as
    returned by starsd cosmwasm query.
    """

    def __init__(
        self,
        admin: str,
        base_token_uri: str,
        num_tokens: int,
        per_address_limit: int,
        sg721_address: str,
        sg721_code_id: str,
        start_time: datetime,
        unit_price: Coin,
        whitelist: Whitelist = None,
    ):

        self.admin = admin
        self.base_token_uri = base_token_uri
        self.num_tokens = num_tokens
        self.per_address_limit = per_address_limit
        self.sg721_address = sg721_address
        self.sg721_code_id = sg721_code_id
        self.start_time = start_time
        self.unit_price = unit_price
        self.whitelist = whitelist

    def __eq__(self, o: object) -> bool:
        if type(o) is not type(self):
            return False
        if len(self.__dict__) != len(o.__dict__):
            return False
        for k,v in self.__dict__.items():
            if k not in o.__dict__:
                return False
            if v != o.__dict__[k]:
                return False
        return True

    def print(self):
        print("--- Minter Config ---")
        print(f"Admin: {self.admin}")
        print(f"Base token uri: {self.base_token_uri}")
        print(f"Num tokens: {self.num_tokens}")
        print(f"SG721 address: {self.sg721_address}")
        print(f"Start time: {self.start_time.strftime(DATETIME_FMT)}")
        print(f"Unit price: {self.unit_price}")
        print(f"Whitelist: {self.whitelist}")

    @classmethod
    def from_data(cls, data: dict):
        admin = data["admin"]
        base_token_uri = data["base_token_uri"]
        num_tokens = data["num_tokens"]
        per_address_limit = data["per_address_limit"]
        sg721_address = data["sg721_address"]
        sg721_code_id = data["sg721_code_id"]
        start_time = timestamp_from_str(data["start_time"])
        unit_price = Coin(data["unit_price"]["amount"], data["unit_price"]["denom"])
        whitelist = data["whitelist"]

        return cls(
            admin,
            base_token_uri,
            num_tokens,
            per_address_limit,
            sg721_address,
            sg721_code_id,
            start_time,
            unit_price,
            whitelist,
        )
