import base64
import json
import logging
import subprocess
from enum import Enum
from typing import List

import requests

from stargazeutils.cache.sg721_cache import SG721Cache, SG721Info

LOG = logging.getLogger(__name__)


class QueryMethod(Enum):
    """Query method for getting information from the chain."""

    BINARY = 1
    REST = 2


class StargazeClient:
    """StargazeClient provides a connection to the staragze blockchain
    It allows for querying contracts and transactions and can be passed
    to other classes that need access to information from the chain. It
    also provides some basic methods for querying collection information."""

    def __init__(
        self,
        node: str = "https://rpc.stargaze-apis.com:443/",
        chain_id: str = "stargaze",
        rest_url: str = "https://rest.stargaze-apis.com",
        query_method: QueryMethod = QueryMethod.BINARY,
        sg721_cache: SG721Cache = None,
    ):
        """
        Initializes a StargazeClient

        Arguments:
        - node: The RPC stargaze node
        - chain_id: The stargaze chain id
        - rest_url: The REST stargaze URL without trailing slash
        - query_method: The primary method used to query the stargaze chain
        - sg721_cache: A cache for sg721 information to help speed basic queries
        """
        self.node = node
        self.chain_id = chain_id
        self.rest_url = rest_url
        self.query_method = query_method
        self._sg721_cache = sg721_cache or SG721Cache()

        self._query_suffix = ["--node", self.node, "--chain-id", self.chain_id]
        self._execute_suffix = [
            "--gas-prices",
            "0.01ustars",
            "--gas",
            "auto",
            "--gas-adjustment",
            "1.3",
        ] + self._query_suffix

    @staticmethod
    def _get_json(cmd: List[str]):
        """Executes a command returns a JSON object of the response.
        The passed in cmd list should be sanitized before use. Do not
        pass arbitrary input to this method without knowing what you
        are doing.

        Arguments:
        - cmd: A list of strings that will be executed
        """
        LOG.debug(f"Executing <{' '.join(cmd)}>")
        output = subprocess.check_output(cmd)
        return json.loads(output)

    def _query_rest_contract(self, contract: str, query: dict):
        """Queries a contract via the REST endpoint.

        Arguments:
        - contract: The cosmwasm contract address
        - query: The dictionary query to send"""
        encoded_query = base64.b64encode(json.dumps(query).encode()).decode()
        url = (
            f"{self.rest_url}/cosmwasm/wasm/v1/"
            + f"contract/{contract}/smart/{encoded_query}"
        )
        LOG.debug(f"url = {url}")
        return requests.get(url).json()

    def query_contract(self, contract: str, query: dict) -> dict:
        """Queries a contract and returns the dictionary
        returned from the JSON response.

        Arguments:
        - contract: The cosmwasm contract address to query
        - query: The dictionary query to submit
        """
        if self.query_method is QueryMethod.BINARY:
            cmd = [
                "starsd",
                "query",
                "wasm",
                "contract-state",
                "smart",
                contract,
                json.dumps(query),
            ] + self._query_suffix
            return StargazeClient._get_json(cmd)

        return self._query_rest_contract(contract, query)

    def get_sg721_info(self, collection_name) -> SG721Info:
        return self._sg721_cache.get_sg721_info_from_name(collection_name)

    def query_txs(self, params: dict):
        """Queries the transactions on the blockchain based on the
        given parameters. This only queries the transactions via
        REST. Binary support is not implemented at this time.

        Arguments:
        - params: The txs request parameters to submit
        """
        url = f"{self.rest_url}/txs"
        LOG.debug(f"Querying tx with params: {params}")
        return requests.get(url, params=params).json()

    def fetch_contracts(self, code_id: int):
        """Fetch all contract addresses for a given code id. This
        commands supports a paginated response.

        Arguments:
        - code_id: The initialized code id to fetch contracts for
        """
        page = 1
        cmd = [
            "starsd",
            "query",
            "wasm",
            "list-contract-by-code",
            "--page",
            str(page),
            str(code_id),
        ] + self._query_suffix
        contracts = []
        new_contracts = StargazeClient._get_json(cmd)["contracts"]

        while len(new_contracts) > 0:
            contracts.extend(new_contracts)
            page += 1
            cmd = [
                "starsd",
                "query",
                "wasm",
                "list-contract-by-code",
                "--page",
                str(page),
                str(code_id),
            ] + self._query_suffix
            new_contracts = StargazeClient._get_json(cmd)["contracts"]
        return contracts

    def fetch_sg721_contract_info(self, sg721: str) -> SG721Info:
        """Fetch the SG721 contract information for a given SG721
        contract address. This method caches the response so it
        only needs to query the chain at most once. Once the cache
        has been updated you can use self.sg721_cache.save_csv() to
        save the cache file for future use.

        Arguments:
        - sg721: The SG721 contract address to search
        """
        if self._sg721_cache.has_sg721_info(sg721):
            return self._sg721_cache.get_sg721_info(sg721)
        data = self.query_contract(sg721, {"contract_info": {}})["data"]
        return self._sg721_cache.update_sg721_contract_info(sg721, data)

    def fetch_sg721_minter(self, sg721: str) -> str:
        """Fetch the SG721 contract minter's address for a given SG721
        contract address. This method caches the response so it
        only needs to query the chain at most once. Once the cache
        has been updated you can use self.sg721_cache.save_csv() to
        save the cache file for future use.

        Arguments:
        - sg721: The SG721 contract address"""
        if self._sg721_cache.has_sg721_minter(sg721):
            return self._sg721_cache.get_sg721_info(sg721)
        minter = self.query_contract(sg721, {"minter": {}})["data"]["minter"]
        return self._sg721_cache.update_sg721_minter(sg721, minter)

    def print_sg721_info(self, only_new=False):
        """Fetch all NFT collections and then print the
        collection names. By default, only non-cached will
        be printed.

        Example output:
        Found 2 new collections
        - Collection 1
        - Collection 2
        -----

        Arguments:
        - only_new: Print only the new (non-cached) collections"""
        new_str = "new " if only_new else ""

        new_collection_str = ""
        for contract in self.fetch_contracts(1):
            LOG.debug(f"Fetching info for {contract}")
            if not only_new or not self._sg721_cache.has_complete_data(contract):
                info = self.fetch_sg721_contract_info(contract)
                self.fetch_sg721_minter(contract)

                new_collection_str += f"- {info.name}\n"

        self._sg721_cache.save_csv()
        if len(new_collection_str) > 0:
            print(f"Found {new_str}collections")
            print(new_collection_str)
            print("-----")
