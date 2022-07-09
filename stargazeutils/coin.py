from decimal import Decimal

NATIVE_DENOM = "ustars"
NATIVE_MULTIPLIER = 1000000


class Coin:
    """Represents an amount and denomination"""

    def __init__(self, amount: Decimal, denom: str):
        """Initializes a new Coin.

        Arguments:
        - amount: The amount as a string
        - denom: The coin denomination
        """
        self.amount = Decimal(amount)
        self.denom = denom

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, o) -> bool:
        return (
            type(self) is type(o) and self.amount == o.amount and self.denom == o.denom
        )

    def __lt__(self, o) -> bool:
        if type(self) is not type(o):
            raise TypeError(
                "'<' not supported between instanced of "
                f"'{type(self).__name__}' and '{type(o).__name__}'"
            )
        return self.denom == o.denom and self.amount < o.amount

    def __le__(self, o) -> bool:
        if type(self) is not type(o):
            raise TypeError(
                "'<=' not supported between instanced of "
                f"'{type(self).__name__}' and '{type(o).__name__}'"
            )
        return self.denom == o.denom and self.amount <= o.amount

    def __str__(self) -> str:
        if self.denom == "ustars":
            star_amount = self.amount / NATIVE_MULTIPLIER
            return f"{star_amount} {self.denom[1:]}"
        return f"{self.amount} {self.denom}"

    def get_stars(self):
        if self.denom != NATIVE_DENOM:
            return None
        return self.amount / NATIVE_MULTIPLIER

    @classmethod
    def from_ustars(cls, ustars):
        """Creates a Coin object from ustars

        :param ustars: The ustars amount
        :return A new Coin
        :rtype Coin
        """
        return cls(Decimal(ustars), NATIVE_DENOM)

    @classmethod
    def from_stars(cls, stars):
        """Creates a Coin object from stars

        :param stars: The stars amount
        :return A new Coin
        :rtype Coin"""
        return cls(Decimal(stars) * NATIVE_MULTIPLIER, NATIVE_DENOM)
