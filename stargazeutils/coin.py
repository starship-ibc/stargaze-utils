class Coin:
    def __init__(self, amount: str, denom: str):
        self.amount = amount
        self.denom = denom

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.denom == "ustars":
            star_amount = int(int(self.amount) / 1000000)
            return f"{star_amount} {self.denom[1:]}"
        return f"{self.amount} {self.denom}"