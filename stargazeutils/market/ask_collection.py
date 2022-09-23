import logging
from typing import List

from stargazeutils.common import export_table_csv, print_table

from ..collection import NFTCollection
from .market_ask import MarketAsk, SaleType

LOG = logging.getLogger(__name__)


class AskCollection:
    """Represents a set of listings for a given collection."""

    def __init__(self, asks: List[MarketAsk], token_info: NFTCollection):
        """Initializes a new AskCollection.

        :param asks: The list of listings for a given collection.
        :param token_info: The token metadata for the tokens in the collection.
        """
        self.sg721 = asks[0].collection
        self.asks = asks
        self.token_info = token_info
    
    def get_token_ask(self, token_id: int):
        for ask in self.asks:
            if ask.token_id == token_id:
                return {"ask": ask, "token_info": self.token_info.tokens[token_id]}
        return None

    def create_asks_by_trait(self, include_auctions: bool = True) -> dict[str,dict[str,List[dict]]]:
        """Creates a dictionary of  asks by trait
        including the metadata. The returning dictionary
        follows the pattern:

        {
            "trait_name": {
                "trait_value": [
                    {"ask": MarketAsk, "token_info": dict},
                    ...
                ]
            }
        }

        The trait_value array of asks is sorted by price.

        :param include_auctions Should the response include auctions?
        :return A dictionary as described above
        """

        def create_ask_trait(ask: MarketAsk):
            return {"ask": ask, "token_info": self.token_info.tokens[ask.token_id]}

        trait_asks = {}
        for ask in self.asks:
            id = ask.token_id
            token_info = self.token_info.tokens[id]

            for trait, value in token_info.items():
                if trait in [
                    "id",
                    "image",
                    "description",
                    "dna",
                    "name",
                    "rank",
                    "score",
                    "edition",
                ]:
                    continue

                if trait not in trait_asks:
                    trait_asks[trait] = {}
                if value not in trait_asks[trait]:
                    trait_asks[trait][value] = []
                if include_auctions or ask.sale_type == SaleType.FIXED_PRICE:
                    trait_asks[trait][value].append(create_ask_trait(ask))

        for t, tv in trait_asks.items():
            for u, v in tv.items():
                v.sort(key=lambda x: x["ask"].price)

        if len(trait_asks) == 0 and len(self.asks) > 0:
            LOG.info("No traits. Showing only floor prices")

            trait_asks["all"] = {
                "all": [
                    create_ask_trait(a)
                    for a in sorted(self.asks, key=lambda a: a.price)
                ]
            }

        return trait_asks

    def get_csv_table(self, extra_fields: List[str]) -> List[List]:
        """Gets a table of asks as a csv file including the
        token metadata provided by the token_info parameter. The
        headers should be a list of traits to include as the columns.
        By default, only the price and id are included. The extra_fields
        values for each ask are retrieved from self.token_info.

        :param extra_fields: A list of traits to export
        """
        headers = ["id", "price", "seller", "valid", "reason"]
        headers.extend(extra_fields)

        table = [headers]
        for ask in self.asks:
            token = self.token_info.tokens[ask.token_id]
            stars_price = ask.price.get_stars()
            line = [
                str(ask.token_id),
                str(stars_price),
                str(ask.seller),
                str(ask.is_valid()),
                ask.reason.name,
            ] + [str(token[h]) for h in extra_fields]
            table.append(line)

        return table

    def export_csv(self, extra_fields: List[str], filename: str):
        """Exports a list of asks as a csv file including the
        token metadata provided by the token_info parameter. The
        headers should be a list of traits to include as the columns.
        By default, only the price and id are included. The extra_fields
         values for each ask are retrieved from self.token_info.

        :param extra_fields: A list of traits to export
        :param filename: The filename of the exported csv file
        """
        table = self.get_csv_table(extra_fields)
        export_table_csv(table, filename)

    def get_avg_trait_pricing_table(self):
        ask_dict = {ask.token_id: ask for ask in self.asks}
        listed_tokens_set = set(ask_dict.keys())

        table = [
            ["Trait", "Value", "Num Listings", "Min Price", "Avg Price", "Max Price"]
        ]
        for trait, values in self.token_info.traits.items():
            if trait in ["token_id", "image", "hubble_rank", "dna", "description"]:
                continue

            for value, tokens in values.items():
                listed_tokens = listed_tokens_set.intersection(set(tokens))
                listed_prices = [ask_dict[x].price.get_stars() for x in listed_tokens]

                avg_price = 0
                min_price = 0
                max_price = 0
                if len(listed_tokens) > 0:
                    avg_price = sum(listed_prices) / len(listed_prices)
                    min_price = min(listed_prices)
                    max_price = max(listed_prices)

                table.append(
                    [
                        trait,
                        value,
                        len(listed_tokens),
                        str(min_price),
                        str(avg_price),
                        str(max_price),
                    ]
                )

        return table

    def print_avg_trait_pricing(self):
        table = self.get_avg_trait_pricing_table()
        print_table(table)
