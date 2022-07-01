import json
import logging
from typing import List, Set

from .. import ipfs
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
        """Initializes the SG721Client with at least the SG721 address. If a minter
        address is not included, then it will be automatically queries from the
        chain. A custom StargazeClient may be included, but if not a new instance
        of one will be created for communication with the blockchain using default
        parameters.

        Arguments:
        - sg721: The collection sg721 address
        - minter: The collection minter address
        - sg_client: A StargazeClient object
        """
        self.sg721 = sg721
        self.sg_client = sg_client or StargazeClient()

        self.minter = minter or self.sg_client.fetch_sg721_minter(self.sg721)
        self._minter_config = None
        self._whitelist_config = None
        self._collection_info = None

    def query_sg721(self, query: dict) -> dict:
        """Queries the SG721 address with a given cosmwasm query. Returns
        the "data" element of the expected json response.

        Arguments:
        - query: The cosmwasm query dictionary.
        """
        return self.sg_client.query_contract(self.sg721, query)["data"]

    def query_minter(self, query):
        """Queries the minter address with a given cosmwasm query. Returns
        the "data" element of the expected json response.

        Arguments:
        - query: The cosmwasm query dictionary.
        """
        return self.sg_client.query_contract(self.minter, query)["data"]

    def query_tokens_owned_by(self, owner: str) -> List[int]:
        """Queries the tokens owned by a given address. Returns a string
        of token ids.

        Arguments:
        - owner: The owner's stars address.
        """
        return self.query_sg721({"tokens": {"owner": owner}})["tokens"]

    def query_minter_config(self) -> MinterConfig:
        """Queries for the minter configuration if not cached. The response
        is converted to a MinterConfig and cached in the SG721 object so that
        repeated calls to the blockchain aren't needed.
        """
        if self._minter_config is None:
            self._minter_config = MinterConfig.from_data(
                self.query_minter({"config": {}})
            )
        return self._minter_config

    def query_collection_info(self) -> CollectionInfo:
        """Queries for the sg721 collection info. Returns a CollectionInfo
        object. The response is cached so that repeated calls to the
        blockchain aren't needed.
        """
        if self._collection_info is None:
            data = self.query_sg721({"collection_info": {}})
            self._collection_info = CollectionInfo.from_data(data)
        return self._collection_info

    def query_whitelist(self) -> Whitelist:
        """Queries for the minter whitelist. Returns a Whitelist object.
        The whitelist info is cached so that repeated calls to the
        blockchain aren't needed.
        """
        if self._whitelist_config is None:
            wl_contract = self.query_minter_config().whitelist
            if wl_contract is None:
                return None
            whitelist_data = self.sg_client.query_contract(wl_contract, {"config": {}})[
                "data"
            ]
            self._whitelist_config = Whitelist.from_data(whitelist_data)
        return self._whitelist_config

    def fetch_minted_tokens(self, start_after: str = "0", limit=30) -> List[int]:
        """Fetches all minted token ids for the given collection. Returns
        a list of token id integers. This method handles pagination and will
        return a list of all minted token ids by default.

        Arguments:
        - start_after: You can query only token ids after a given value if desired.
        - limit: How many tokens are queried at a time. The response is often paginated.
        """
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

    def query_owner_of_token(self, token_id) -> str:
        """Queries for the owner of a given token id. Returns the owner
        stars address if one is available, or an empty string if the token
        is not owned.

        Arguments:
        - token_id: The id of the token to query."""
        return self.query_sg721({"owner_of": {"token_id": str(token_id)}})["owner"]

    def query_num_minted_tokens(self) -> int:
        """Queries for the number of currently minted tokens of the give
        collection. Returns the number of minted tokens.
        """
        return self.query_sg721({"num_tokens": {}})["count"]

    def query_contract_info(self) -> dict:
        """Queries for the SG721 contract info. Returns the data
        dictionary response from stars cosmwasm.
        """
        return self.query_sg721({"contract_info": {}})

    def query_nft_info(self, token_id: str) -> dict:
        """Queries for "all nft info" of a given token id. Returns
        the data dictionary response from stars cosmwasm."""
        return self.query_sg721({"all_nft_info": {"token_id": token_id}})

    # def create_mintable_list(self, count=None):
    #     if count is None:
    #         count = self.query_minter_config().num_tokens

    #     return sorted([x for x in range(1, count + 1)])

    def fetch_holders(self) -> Set[str]:
        """Fetches a set of hodlers of the current collection. This method may
        take a while as it queries every owner of every minted token.
        """
        tokens = self.fetch_minted_tokens()
        holders = set()
        for token in tokens:
            if len(tokens) > 1000 and int(token) % 10 == 0:
                LOG.debug(f"Fetching owner for token {token}")
            owner = self.query_sg721({"owner_of": {"token_id": token}})["owner"]
            holders.add(owner)
        return holders

    def fetch_traits_for_token(self, token_id) -> dict:
        """Fetches the traits for a given token based on what
        it finds in IPFS metadata. This method may need to be modified
        to handle different methods that collection contracts store the
        metadata. Right now it assumes that the data is stored at the
        "<base_token_uri>/<token_id>" path but this is not always the
        case. Returns a dictionary of traits including name, id, etc.

        Depending on the stability of IPFS, this method may take a while
        to return the information so caching is recommended. One easy
        way to ensure the data is cached is by using the "requests_cache"
        package and using the following near the beginning of your system.

        ```py
        import requests_cache
        requests_cache.install_cache("stargaze-ipfs")
        ```

        Arguments:
        - token_id: The token to fetch traits for.
        """
        config = self.query_minter_config()
        url = f"{config.base_token_uri}/{token_id}"

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
        if "description" in metadata:
            traits["description"] = metadata["description"]
        if "dna" in metadata:
            traits["dna"] = metadata["dna"]
        if "edition" in metadata:
            traits["edition"] = metadata["edition"]

        return traits

    def fetch_traits(self) -> List[dict]:
        """Fetches a list of traits for all minted tokens."""
        config = self.query_minter_config()
        tokens = range(1, config.num_tokens + 1)
        return [self.fetch_traits_for_token(id) for id in tokens]

    def export_traits_json(self, filename):
        """Exports the list of collection traits as a JSON file.

        Arguments:
        - filename: The path to the JSON file."""
        traits = self.fetch_traits()
        with open(filename, "w") as f:
            json.dump(traits, f)

    def export_traits_csv(self, filename):
        """Exports the list of collection traits as a CSV file. This
        file contains two blank columns in between each trait column
        so it's easy to add stats for the traits. The CSV file is
        comma-separated and each column is surrounded by double-quotes.

        Arguments:
        - filename: The path to the CSV file."""
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

    def fetch_trait_rarity(self) -> dict:
        """Fetches a dictinoary of trait rarity information. Returns
        the data in this format:

        ```json
        {
            "trait_name": {"trait_value": [<token_id>, ...], ...},
            ...
        }
        ```
        """
        tokens_info = self.fetch_traits()
        traits = {}
        for token in tokens_info:
            for trait in token.keys():
                if trait not in [
                    "id",
                    "name",
                    "image",
                    "edition",
                    "description",
                    "dna",
                ]:
                    if trait not in traits:
                        traits[trait] = {token[trait]: 1}
                    elif token[trait] not in traits[trait]:
                        traits[trait][token[trait]] = 1
                    else:
                        traits[trait][token[trait]] += 1

        return traits

    def print_trait_rarity(self):
        """Prints the trait rarity information including the following:
        - Total tokens
        - Each trait type
        - Each trait value, count of tokens, and percentage of total tokens
        """
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
