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

    @classmethod
    def from_data(cls, data: dict):
        """Initializes a RoyaltyInfo object from data returned
        by a stargaze query. The data argument is expected to
        include a payment_address and share.

        Arguments:
        - data: The starsd response with payment_address and share info"""
        return cls(data["payment_address"], float(data["share"]))
