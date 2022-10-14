#!/usr/bin/env python3

import argparse
import os

from stargazeutils.coin import Coin
from stargazeutils.collection import Sg721Client
from stargazeutils.common import (
    IGNORED_TRAITS,
    export_table_csv,
    print_table,
    slugified,
)
from stargazeutils.market import MarketClient
from stargazeutils.market.ask_collection import AskCollection
from stargazeutils.market.market_ask import DEFAULT_MARKET_CONTRACT

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
Fetch the current floor pricing for each trait in a given Stargaze collection.

Examples:

To print out the floor pricing for current punk asks by Trait:

    python3 get_floor_pricing.py "Stargaze Punks"

To print out the floor pricing without adding extra validation
(may be quicker, but contain invalid asks):

    python3 get_floor_pricing.py "Stargaze Punks" --no-strict

To output the current asks by trait:

    python3 get_floor_pricing.py "Stargaze Punks" --output csv
    """,
)

parser.add_argument("collection", type=str, help="The name of the Stargaze Collection.")
parser.add_argument(
    "--output",
    type=str,
    default="print",
    help="Use csv to save the output as a csv file",
)
parser.add_argument(
    "--strict",
    type=bool,
    default=True,
    action=argparse.BooleanOptionalAction,
    help="If False, disables strict validation.",
)


def fetch_asks_for_collection(
    collection_name: str,
    strict_validation: bool = True,
    market_contract: str = DEFAULT_MARKET_CONTRACT,
):
    print(f"Collection name: {collection_name}")
    print(f"Strict: {strict_validation}")

    market = MarketClient(market_contract)
    client = Sg721Client.from_collection_name(collection_name)

    cache_dir = os.path.join(os.curdir, "cache", "collections")
    json_file = slugified(collection_name) + ".json"
    json_trait_cache_file = os.path.join(cache_dir, json_file)

    print("")
    collection = client.fetch_nft_collection(json_trait_cache_file)
    collection.export_json(json_trait_cache_file)
    print(f"Trait cache file stored at {json_trait_cache_file}")

    return market.fetch_asks_for_collection(collection, strict_verify=strict_validation)


def get_floor_pricing_table(trait_asks, num_prices: int = 3):
    table = [
        [
            "Trait",
            "Value",
            "Num Asks",
            "Price 1",
            "Token 1",
            "Price 2",
            "Token 2",
            "Price 3",
            "Token 3",
        ]
    ]
    expected_length = 3 + (num_prices * 2)
    for trait, values in trait_asks.items():
        if trait in IGNORED_TRAITS:
            continue

        for value, asks in sorted(values.items(), key=lambda i: i[1][0]["ask"].price):
            row = [trait, value, str(len(asks))]
            for ask in asks[:num_prices]:
                row.extend([str(ask["ask"].price), str(ask["ask"].token_id)])
            row.extend([""] * (expected_length - len(row)))
            table.append(row)
    return table


def token_pricing_table(asks: AskCollection, token_id: int):
    ask = asks.get_token_ask(token_id)
    if not ask:
        print(f"Token {token_id} not listed")
        return

    table = [
        [
            "Trait",
            "Value",
            "Price 1",
            "Token 1",
            "Price 2",
            "Token 2",
            "Price 3",
            "Token 3",
            "Price 4",
            "Token 4",
        ]
    ]
    trait_asks = asks.create_asks_by_trait()
    for trait, value in ask["token_info"].items():
        traits = trait_asks.get(trait)
        if trait in ["id", "name", "image", "description"]:
            continue
        if not traits:
            print(f"- Didn't find trait {trait}")
            continue
        values = traits.get(value)
        if not values:
            print(f"- Didn't find value {value} in trait {trait}")
            continue
        row = [trait, value]
        for v_ask in values[:4]:
            diff = Coin.from_ustars(ask["ask"].price.amount - v_ask["ask"].price.amount)
            if diff.amount < 0:
                diff = Coin.from_ustars(-diff.amount)
                row.append(f"+{str(diff)}")
            else:
                row.append(f"-{str(diff)}")
            row.append(v_ask["ask"].token_id)

        table.append(row)
    return table


if __name__ == "__main__":
    args = parser.parse_args()
    collection_name = args.collection

    asks = fetch_asks_for_collection(collection_name, args.strict)
    trait_asks = asks.create_asks_by_trait()
    table = get_floor_pricing_table(trait_asks, num_prices=3)

    if args.output == "csv":
        csv_file = slugified(collection_name) + ".csv"
        export_table_csv(table, csv_file)
        exit(0)

    print_table(table)
