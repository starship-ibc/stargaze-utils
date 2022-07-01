from .. import ipfs
import json
import logging
import time
from datetime import datetime
from pprint import pprint
from typing import List

import requests

from ..stargaze import StargazeClient
from .collection_info import CollectionInfo
from .minter_config import MinterConfig
from .whitelist import Whitelist

LOG = logging.getLogger(__name__)


class Sg721Client:
    """
    An SG721 NFT client for getting information from the blockchain

    Minter queries:
        - config
        - mintable_num_tokens
        - start_time
        - mint_price
        - mint_count

    Token (SG721) queries:
        - owner_of
        - approval
        - all_operators
        - num_tokens
        - contract_info
        - nft_info
        - all_nft_info
        - tokens
        - all_tokens
        - minter
        - collection_info
    """

    def __init__(
        self, sg721: str, minter: str = None, sg_client: StargazeClient = None
    ):
        self.sg721 = sg721
        self.sg_client = sg_client or StargazeClient()

        self.minter = minter or self.sg_client.fetch_sg721_minter(self.sg721)
        self._minter_config = None
        self._whitelist_config = None
        self._collection_info = None

    def query_sg721(self, query):
        return self.sg_client.query_contract(self.sg721, query)["data"]

    def query_minter(self, query):
        return self.sg_client.query_contract(self.minter, query)["data"]

    def fetch_tokens_owned_by(self, owner: str) -> List[int]:
        return self.query_sg721({"tokens": {"owner": owner}})["tokens"]

    def query_minter_config(self) -> MinterConfig:
        if self._minter_config is None:
            self._minter_config = MinterConfig.from_data(self.query_minter({"config": {}}))
        return self._minter_config

    def query_collection_info(self) -> CollectionInfo:
        if self._collection_info is None:
            data = self.query_sg721({"collection_info": {}})
            self._collection_info = CollectionInfo.from_data(data)
        return self._collection_info

    def query_whitelist(self) -> Whitelist:
        if self._whitelist_config is None:
            wl_contract = self.query_minter_config().whitelist
            if wl_contract is None:
                return None
            whitelist_data = self.sg_client.query_contract(wl_contract, {"config": {}})["data"]
            self._whitelist_config = Whitelist.from_data(whitelist_data)
        return self._whitelist_config

    def fetch_minted_tokens(self, start_after: str = "0", limit=30):
        minted_tokens = []
        tokens = self.query_sg721(
            {"all_tokens": {"start_after": start_after, "limit": limit}}
        )["tokens"]
        while len(tokens) == limit:
            start_after = tokens[-1]
            LOG.debug(f"Fetching more tokens after {start_after}")
            minted_tokens += tokens
            tokens = self.query_sg721(
                {"all_tokens": {"start_after": start_after, "limit": limit}}
            )["tokens"]
        minted_tokens += tokens
        return minted_tokens

    def fetch_owner_of_token(self, token_id):
        return self.query_sg721({"owner_of": {"token_id": str(token_id)}})["owner"]

    def fetch_num_minted_tokens(self):
        return self.query_sg721({"num_tokens": {}})["count"]

    def query_contract_info(self):
        return self.query_sg721({"contract_info": {}})

    def query_nft_info(self, token_id: str):
        return self.query_sg721({"all_nft_info": {"token_id": token_id}})

    # def create_mintable_list(self, count=None):
    #     if count is None:
    #         count = self.query_minter_config().num_tokens

    #     return sorted([x for x in range(1, count + 1)])

    def fetch_holders(self):
        tokens = self.fetch_minted_tokens()
        holders = set()
        for token in tokens:
            if len(tokens) > 1000 and int(token) % 10 == 0:
                LOG.debug(f"Fetching owner for token {token}")
            owner = self.query_sg721({"owner_of": {"token_id": token}})["owner"]
            # print(owner)
            holders.add(owner)
        return holders

    def fetch_traits_for_token(self, token_id):
        config = self.query_minter_config()
        url = f"{config.base_token_uri}/{token_id}"

        print(f"Fetching attributes from {url}")
        LOG.info(f"Fetching attributes from {url}")
        metadata = ipfs.get(url).json()
        traits = {}
        for attr in metadata["attributes"]:
            if "trait_value" in attr:
                trait = attr["trait_type"]
                value = attr["trait_value"]
                traits[trait] = value
            elif "value" in attr:
                trait = attr["trait_type"]
                value = attr["value"]
                traits[trait] = value
        traits["id"] = token_id
        traits["name"] = metadata["name"]
        traits["image"] = metadata["image"]
        if 'description' in metadata:
            traits['description'] = metadata['description']
        if "dna" in metadata:
            traits['dna'] = metadata['dna']
        if "edition" in metadata:
            traits['edition'] = metadata['edition']
        
        return traits

    def fetch_traits(self):
        config = self.query_minter_config()
        tokens = range(1, config.num_tokens + 1)
        return [self.fetch_traits_for_token(id) for id in tokens]

    def export_traits_json(self, filename):
        traits = self.fetch_traits()
        with open(filename, "w") as f:
            json.dump(traits, f)

    def export_traits_csv(self, filename):
        traits = self.fetch_traits()
        headers = list(traits[0].keys())
        with open(filename, "w") as f:
            f.write('"' + '","","",'.join(headers) + '"\n')
            for token in traits:
                for col in headers[:-1]:
                    value = "null"
                    if col in token:
                        value = token[col]
                    f.write('"' + str(value) + '","","",')
                f.write('"' + str(token[headers[-1]]) + '"\n')

    def fetch_trait_rarity(self):
        tokens_info = self.fetch_traits()
        traits = {}
        for token in tokens_info:
            for trait in token.keys():
                if trait not in ["id", "name", "image", "edition", "description", "dna"]:
                    if trait not in traits:
                        traits[trait] = {token[trait]: 1}
                    elif token[trait] not in traits[trait]:
                        traits[trait][token[trait]] = 1
                    else:
                        traits[trait][token[trait]] += 1

        return traits

    def print_trait_rarity(self):
        traits = self.fetch_trait_rarity()
        print("\n---")
        print("Trait Rarity")
        total_tokens = sum(list(traits.values())[0].values())
        print(f"Total Tokens: {total_tokens}")
        print("---\n")
        for trait_name, trait_options in traits.items():
            print(f"*** {trait_name} ***")
            print(f"# Options: {len(trait_options.keys())}")
            for o, v in sorted(trait_options.items(), key=lambda x: x[1]):
                print(f"- {o:<25}: {v:<5} ({v / total_tokens * 100:0.2f}%)")
            print("\n")
