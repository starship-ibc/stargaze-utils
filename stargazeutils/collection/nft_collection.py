import json
from typing import List, Set


class NFTCollection:
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
    def from_json_file(cls, collection: str, filename: str):
        """Initializes an NFT collection object from a JSON file
        that has been saved to include key value pairs of the
        token ids and token information.

        Arguments:
        - collection: The sg721 collection address
        - filename: The JSON filename with the collection info
        """
        tokens = []
        with open(filename, "r") as f:
            tokens = json.load(f)
        return cls(collection, tokens)

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

    def filter_tokens(self, filters: dict) -> Set:
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
