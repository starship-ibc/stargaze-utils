from datetime import datetime

from ..coin import Coin
from ..common import DATETIME_FMT, timestamp_from_str


class Whitelist:
    """Represents the whitelist information received
    by a starsd query.
    """

    def __init__(
        self,
        start_time: datetime,
        end_time: datetime,
        unit_price: Coin,
        per_address_limit: int,
        member_limit: int,
        num_members: int,
        is_active: bool = True,
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.unit_price = unit_price
        self.per_address_limit = per_address_limit
        self.member_limit = member_limit
        self.num_members = num_members
        self.is_active = is_active

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
        print("--- Whitelist ---")
        print(f"Num members: {self.num_members}")
        print(f"Start time: {self.start_time.strftime(DATETIME_FMT)}")
        print(f"End time: {self.end_time.strftime(DATETIME_FMT)}")
        print(f"Unit price: {self.unit_price}")
        print(f"Is active: {self.is_active}")
        print(f"Member limit: {self.member_limit}")

    @classmethod
    def from_data(cls, data: dict):
        end_time = timestamp_from_str(data["end_time"])
        is_active = data["is_active"]
        member_limit = data["member_limit"]
        num_members = data["num_members"]
        per_address_limit = data["per_address_limit"]
        start_time = timestamp_from_str(data["start_time"])
        unit_price = Coin(data["unit_price"]["amount"], data["unit_price"]["denom"])

        return cls(
            start_time,
            end_time,
            unit_price,
            per_address_limit,
            member_limit,
            num_members,
            is_active,
        )
