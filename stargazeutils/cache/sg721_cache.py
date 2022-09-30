import logging
import os
from typing import List

from .sg721_info import SG721Info

LOG = logging.getLogger(__name__)


class SG721Cache:
    """An SG721 cache that stores the information about collection
    for quick retrieval and to help reduce redundant calls of
    immutable responses from the blockchain.

    The cache is currently backed by a CSV file.
    """

    def __init__(self, cache_file="cache/sg721_collections.csv"):
        """Initializes the cache with a given CSV file."""
        self.cache_file = cache_file
        self._sg721: dict[str,SG721Info] = {}

        self._load_csv()

    def _load_csv(self):
        if not os.path.exists(self.cache_file):
            return

        self._sg721: dict[str,SG721Info] = {}
        lines = []

        with open(self.cache_file) as f:
            lines = f.readlines()

        for line in lines:
            sg721_info = SG721Info.parse_csv_row(line)
            LOG.debug(f"Loaded info for {sg721_info}")
            self._sg721[sg721_info.sg721] = sg721_info

        LOG.info(f"Loaded {len(lines)} collections")

    def save_csv(self):
        """Saves the current cache info as a CSV file. The file
        path used is same as where the cache was loaded from.
        """
        with open(self.cache_file, "w") as f:
            LOG.info(f"Saving {len(self._sg721)} collections")
            for info in self._sg721.values():
                f.write(info.as_csv_row() + "\n")

    def has_sg721_info(self, sg721_addr: str) -> bool:
        """Checks if sg721 info is cached for a given address.

        Arguments:
        - sg721_addr: The sg721 address"""
        if sg721_addr not in self._sg721:
            return False
        info = self._sg721[sg721_addr]
        if info.name is None or info.symbol is None:
            return False
        return True

    def has_sg721_minter(self, sg721_addr: str) -> bool:
        """Checks if the sg721 minter is cached for a given address.

        Arguments:
        - sg721_addr: The sg721 address"""
        if sg721_addr not in self._sg721:
            return False
        info = self._sg721[sg721_addr]
        if info.minter is None:
            return False
        return True

    def has_complete_data(self, sg721_addr: str) -> bool:
        """Checks if all available data (info and minter) is
        cached for a given address.

        Arguments:
        - sg721_addr: The sg721 address
        """
        if sg721_addr not in self._sg721:
            return False
        info = self._sg721[sg721_addr]
        if info.name is None or info.symbol is None or info.minter is None:
            return False
        return True

    def get_sg721_info(self, sg721: str) -> SG721Info:
        """Gets the currently cached SG721Info for a given address,
        or None if there is no information available.

        Arguments:
        - sg721_addr: The sg721 address
        """
        if sg721 not in self._sg721:
            return None
        return self._sg721[sg721]

    def get_sg721_info_from_name(self, collection_name: str) -> SG721Info:
        """Gets the cached SG721Info for a given collection name.
        If the name does not exist, returns None. If there are
        multiple collections with the same name, returns the
        newest collection.

        Arguments:
        - collection_name: The name of the collection to search.
        """
        for sg721, info in reversed(self._sg721.items()):
            if info.name == collection_name:
                return info

        return None

    def update_sg721_contract_info(self, sg721_addr, data: dict) -> SG721Info:
        """Updates the SG721 with the contract info (name and symbol)
        and returns the updated SG721Info object.

        Arguments:
        - sg721_addr: The sg721 address
        - data: A dictionary with the name and symbol for the collection
        """
        info = self.get_sg721_info(sg721_addr)
        if info is None:
            info = SG721Info(sg721_addr)

        info.name = data["name"]
        info.symbol = data["symbol"]
        self._sg721[sg721_addr] = info
        return info

    def update_sg721_minter(self, sg721_addr: str, minter_addr: str) -> SG721Info:
        """Updates the SG721 with the minter address
        and returns the updated SG721Info object.

        Arguments:
        - sg721_addr: The sg721 address
        - minter_addr: The associated minter address
        """
        info = self.get_sg721_info(sg721_addr)
        if info is None:
            info = SG721Info(sg721_addr)

        info.minter = minter_addr
        self._sg721[sg721_addr] = info
        return info

    def get_sg721s(self, names: List[str] = None):
        """Returns the sg721 for a list of named collections. If not, then
        all sg721 addresses will be returned."""

        if names is None:
            return list(self._sg721.keys())

        sg721s = []
        for sg721,info in self._sg721.items():
            if info.name in names:
                names.remove(info.name)
                sg721s.append(sg721)
        
        return sg721s
