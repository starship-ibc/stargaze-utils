import json
from typing import List, Set


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

    def export_json(self, filename):
        """Exports the list of collection traits as a JSON file.

        Arguments:
        - filename: The path to the JSON file."""
        with open(filename, "w") as f:
            json.dump(list(self.tokens.values()), f)

    def export_csv(self, filename):
        """Exports the list of collection traits as a CSV file. This
        file contains two blank columns in between each trait column
        so it's easy to add stats for the traits. The CSV file is
        comma-separated and each column is surrounded by double-quotes.

        Arguments:
        - filename: The path to the CSV file."""
        headers = list(self.tokens[1].keys())
        with open(filename, "w") as f:
            f.write('"' + '","","",'.join(headers) + '"\n')
            for token in self.tokens.values():
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
        print("---")
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
