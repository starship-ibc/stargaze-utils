class RoyaltyInfo:
    """Object with royalty information for an NFT collection"""

    def __init__(self, payment_address: str, share: float):
        """Initializes a RoyaltyInfo object

        Arguments:
        - payment_address: The royal payment stars address
        - share: The royalty share percentage
        """
        self.payment_address = payment_address
        self.share = share

    def __repr__(self):
        pct = self.share * 100
        return f"<Royalty {pct:0.0f}% to {self.payment_address}>"

    @classmethod
    def from_data(cls, data: dict):
        """Initializes a RoyaltyInfo object from data returned
        by a stargaze query. The data argument is expected to
        include a payment_address and share.

        Arguments:
        - data: The starsd response with payment_address and share info"""
        return cls(data["payment_address"], float(data["share"]))
