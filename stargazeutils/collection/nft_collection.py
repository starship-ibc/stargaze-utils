import json
import logging
from typing import List, Set

from stargazeutils.common import export_table_csv, print_table

LOG = logging.getLogger(__name__)


class NFTCollection:
    """Represents an NFT Collection and the token metadata."""

    def __init__(self, sg721: str, tokens: List[dict]):
        """Initializes a new collection with a list of token
        dictionaries including trait information. Make sure the
        tokens include at least an 'id' although other common
        keys are often expected.

        Arguments:
        - sg721: The sg721 contract address
        - tokens: A list of token dictionaries that have all traits.
        The trait dictionary should include at minimum an 'id' key
        and value."""
        self.sg721 = sg721
        self.tokens = {t["id"]: t for t in tokens}
        self._create_trait_cache()

    @classmethod
    def from_json_file(cls, sg721: str, filename: str):
        """Initializes an NFT collection object from a JSON file
        that has been saved to include key value pairs of the
        token ids and token information.

        Arguments:
        - sg721: The sg721 collection address
        - filename: The JSON filename with the collection info
        """
        tokens = []
        with open(filename, "r") as f:
            tokens = json.load(f)
        return cls(sg721, tokens)

    def _create_trait_cache(self):
        """The trait cache organizes the tokens by trait instead
        of by id to aid in filtering of tokens."""
        self.traits = {}
        for id, token in self.tokens.items():
            for trait, value in token.items():
                if trait not in ["id", "image", "name"]:
                    if trait not in self.traits:
                        self.traits[trait] = {}
                    if value not in self.traits[trait]:
                        self.traits[trait][value] = []
                    self.traits[trait][value].append(id)

    def filter_tokens(self, filters: dict) -> Set[str]:
        """Filter the token set based on a set of filters. The filters
        argument is a {trait_name:[values]} where each key is the trait key
        and the list is a list of acceptable trait values. If there is more
        than one trait key filtered on, then the intersection of the valid
        tokens is returned (this is an AND operation).

        Arguments:
        - filters: {trait_name:[trait_value,...]}
        """
        token_set = set()
        for trait, values in filters.items():
            trait_tokens = []
            for value in values:
                trait_tokens.extend(self.traits[trait][value])
            if len(token_set) == 0:
                token_set = set(trait_tokens)
            else:
                token_set = token_set.intersection(set(trait_tokens))

        return token_set

    def export_json(self, filename):
        """Exports the list of collection traits as a JSON file.

        Arguments:
        - filename: The path to the JSON file."""
        with open(filename, "w") as f:
            json.dump(list(self.tokens.values()), f)

    def get_tokens_info_table(
        self,
        token_ids: List[int] = None,
        excluded_traits: List[str] = [],
        sort_key: str = None,
    ) -> List[List]:
        token_ids = token_ids or self.tokens.keys()
        headers = ["id"]
        excluded_traits.append("id")
        for header in self.tokens[1].keys():
            if header not in excluded_traits:
                headers.append(header)

        table = []
        for id in token_ids:
            row = []
            for col in headers:
                value = "null"
                if col in self.tokens[id]:
                    value = self.tokens[id][col]
                row.append(value)
            table.append(row)

        if sort_key is not None:
            if sort_key not in headers:
                LOG.warning(f"Sort key {sort_key} not found, skipping sorting")
            else:
                index = headers.index(sort_key)
                table.sort(key=lambda x: x[index])
        table.insert(0, headers)
        return table

    def export_csv(self, filename):
        """Exports the list of collection traits as a CSV file. This
        file contains two blank columns in between each trait column
        so it's easy to add stats for the traits. The CSV file is
        comma-separated and each column is surrounded by double-quotes.

        Arguments:
        - filename: The path to the CSV file."""
        tokens_table = self.get_tokens_info_table()
        export_table_csv(tokens_table, filename)

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
        traits = {}
        for token in self.tokens.values():
            for trait in token.keys():
                if trait not in [
                    "id",
                    "name",
                    "image",
                    "edition",
                    "description",
                    "dna",
                    "hubble_rank",
                    "Identity Number",
                ]:
                    if trait not in traits:
                        traits[trait] = {token[trait]: 1}
                    elif token[trait] not in traits[trait]:
                        traits[trait][token[trait]] = 1
                    else:
                        traits[trait][token[trait]] += 1

        return traits

    def get_trait_rarity_table(self) -> List[List]:
        """Gets a list of trait rarity info that can be printed
        using print_table.
        """
        traits = self.fetch_trait_rarity()
        if len(traits) == 0:
            return [["No traits"]]

        total_tokens = sum(list(traits.values())[0].values())
        table = []
        table.append(["Total Tokens", total_tokens, ""])

        for trait_name, trait_options in traits.items():
            table.append(["", "", ""])
            table.append([f"{len(trait_options.keys())} {trait_name}", "", ""])
            for o, v in sorted(trait_options.items(), key=lambda x: x[1]):
                table.append([f"- {o}", v, f"{v/total_tokens * 100:0.2f}%"])

        return table

    def print_trait_rarity(self):
        """Prints the trait rarity information including the following:
        - Total tokens
        - Each trait type
        - Each trait value, count of tokens, and percentage of total tokens
        """
        table = self.get_trait_rarity_table()
        print_table(table, header="Trait Rarity", delimiter="")
