import base64
import json
import logging
import subprocess
from enum import Enum

import requests

from stargazeutils.cache.sg721cache import Sg721Cache, Sg721Info

LOG = logging.getLogger(__name__)


class QueryMethod(Enum):
    BINARY = 1
    REST = 2


class StargazeClient:
    def __init__(
        self,
        node="https://rpc.stargaze-apis.com:443/",
        chain_id="stargaze",
        rest_url="https://rest.stargaze-apis.com",
        query_method: QueryMethod = QueryMethod.BINARY,
        sg721_cache: Sg721Cache = None,
    ):
        self.node = node
        self.chain_id = chain_id
        self.rest_url = rest_url
        self.query_method = query_method
        self._sg721_cache = sg721_cache or Sg721Cache()

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
    def _get_json(cmd):
        LOG.debug(f"Executing <{' '.join(cmd)}>")
        output = subprocess.check_output(cmd)
        return json.loads(output)

    def _query_rest_contract(self, contract: str, query: dict):
        encoded_query = base64.b64encode(json.dumps(query).encode()).decode()
        url = (
            f"{self.rest_url}/cosmwasm/wasm/v1/"
            + f"contract/{contract}/smart/{encoded_query}"
        )
        print(f"url = {url}")
        return requests.get(url).json()

    def query_contract(self, contract: str, query: dict) -> dict:
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

    def query_txs(self, params: dict):
        url = f"{self.rest_url}/txs"
        LOG.debug(f"Querying tx with params: {params}")
        return requests.get(url, params=params).json()

    def fetch_contracts(self, code_id: int):
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

    def fetch_sg721_contract_info(self, sg721: str) -> Sg721Info:
        if self._sg721_cache.has_sg721_info(sg721):
            return self._sg721_cache.get_sg721_info(sg721)
        data = self.query_contract(sg721, {"contract_info": {}})["data"]
        return self._sg721_cache.update_sg721_contract_info(sg721, data)

    def fetch_sg721_minter(self, sg721: str) -> str:
        if self._sg721_cache.has_sg721_minter(sg721):
            return self._sg721_cache.get_sg721_info(sg721)
        minter = self.query_contract(sg721, {"minter": {}})["data"]["minter"]
        return self._sg721_cache.update_sg721_minter(sg721, minter)

    def print_sg721_info(self, only_new=False):
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
