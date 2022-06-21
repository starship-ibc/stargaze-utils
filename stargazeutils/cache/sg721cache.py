import logging
import os

LOG = logging.getLogger(__name__)


class Sg721Info:
    def __init__(self, sg721_addr, name=None, symbol=None, minter=None):
        self.sg721 = sg721_addr
        self.name = name
        self.symbol = symbol
        self.minter = minter

    def get_csv_row(self):
        return f'"{self.sg721}","{self.name}","{self.symbol}","{self.minter}"'

    def __repr__(self):
        name = self.name or "None"
        symbol = self.symbol or "None"
        minter = self.minter or "None"
        return f"<{name} ({symbol}) sg721={self.sg721} minter={minter}>"

    def __str__(self):
        return self.name or "<None>"

    @classmethod
    def parse_csv_row(cls, line):
        try:
            sg721_addr, name, symbol, minter = line.split('","')
        except ValueError as e:
            LOG.warning(f"Error processing line {e}: {line}")
            raise e
        name = name or None
        symbol = symbol or None
        minter = minter[:-2] or None
        return cls(sg721_addr[1:], name, symbol, minter)


class Sg721Cache:
    def __init__(self, cache_file="cache/sg721_collections.csv"):
        self.cache_file = cache_file
        self._sg721 = {}

        self._load_csv()

    def _load_csv(self):
        if not os.path.exists(self.cache_file):
            return

        self._sg721 = {}
        lines = []

        with open(self.cache_file) as f:
            lines = f.readlines()

        for line in lines:
            sg721_info = Sg721Info.parse_csv_row(line)
            LOG.debug(f"Loaded info for {sg721_info}")
            self._sg721[sg721_info.sg721] = sg721_info

        LOG.info(f"Loaded {len(lines)} collections")

    def save_csv(self):
        if self._sg721 is None:
            return None

        with open(self.cache_file, "w") as f:
            LOG.info(f"Saving {len(self._sg721)} collections")
            for info in self._sg721.values():
                f.write(info.get_csv_row() + "\n")

    def has_sg721_info(self, sg721_addr: str) -> bool:
        if sg721_addr not in self._sg721:
            return False
        info = self._sg721[sg721_addr]
        if info.name is None or info.symbol is None:
            return False
        return True

    def has_sg721_minter(self, sg721_addr: str) -> bool:
        if sg721_addr not in self._sg721:
            return False
        info = self._sg721[sg721_addr]
        if info.minter is None:
            return False
        return True

    def has_complete_data(self, sg721_addr: str) -> bool:
        if sg721_addr not in self._sg721:
            return False
        info = self._sg721[sg721_addr]
        if info.name is None or info.symbol is None or info.minter is None:
            return False
        return True

    def get_sg721_info(self, sg721: str) -> Sg721Info:
        if sg721 not in self._sg721:
            return None
        return self._sg721[sg721]

    def update_sg721_contract_info(self, sg721_addr, data: dict) -> Sg721Info:
        info = self.get_sg721_info(sg721_addr)
        if info is None:
            info = Sg721Info(sg721_addr)

        info.name = data["name"]
        info.symbol = data["symbol"]
        self._sg721[sg721_addr] = info
        return info

    def update_sg721_minter(self, sg721_addr: str, minter_addr: str) -> Sg721Info:
        info = self.get_sg721_info(sg721_addr)
        if info is None:
            info = Sg721Info(sg721_addr)

        info.minter = minter_addr
        self._sg721[sg721_addr] = info
        return info
