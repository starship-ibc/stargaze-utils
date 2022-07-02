import logging

LOG = logging.getLogger(__name__)


class SG721Info:
    """Represents SG721 information that can be cached."""

    def __init__(
        self, sg721_addr: str, name: str = None, symbol: str = None, minter: str = None
    ):
        """Initializes an SG721Info object.

        Arguments:
        - sg721_addr: The stargaze address for the collection
        - name: The colection name
        - symbol: The NFT symbol
        - minter: The minter address
        """
        self.sg721 = sg721_addr
        self.name = name
        self.symbol = symbol
        self.minter = minter

    def as_csv_row(self) -> str:
        """Returns the object as a CSV row."""
        return f'"{self.sg721}","{self.name}","{self.symbol}","{self.minter}"'

    def __repr__(self):
        name = self.name or "None"
        symbol = self.symbol or "None"
        minter = self.minter or "None"
        return f"<{name} ({symbol}) sg721={self.sg721} minter={minter}>"

    def __str__(self):
        return self.name or "<None>"

    def __eq__(self, o: object) -> bool:
        return (
            type(self) is type(o)
            and len(self.__dict__) == len(o.__dict__)
            and self.sg721 == o.sg721
            and self.name == o.name
            and self.symbol == o.symbol
            and self.minter == o.minter
        )

    @classmethod
    def parse_csv_row(cls, line: str):
        """Parses a line from a CSV file into an SG721Info object. The
        line is expected to be comma separated with fields in double-quotes.

        Arguments:
        - line: The csv line to parse."""
        try:
            sg721_addr, name, symbol, minter = line.split('","')
        except ValueError as e:
            LOG.warning(f"Error processing line {e}: {line}")
            raise e
        name = name or None
        symbol = symbol or None
        minter = minter[:-2] or None
        return cls(sg721_addr[1:], name, symbol, minter)
