#!/usr/bin/env python3

import argparse
import os
from typing import List

from stargazeutils.collection import Sg721Client
from stargazeutils.common import MARKET_CONTRACT, export_table_csv, print_table
from stargazeutils.market import MarketClient

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
    """
)

parser.add_argument("collection", type=str, help="The name of the Stargaze Collection.")
parser.add_argument(
    "--output", type=str, default="print", help="Use csv to save the output as a csv file"
)
parser.add_argument(
    "--strict",
    type=bool,
    default=True,
    action=argparse.BooleanOptionalAction,
    help="If False, disables strict validation.",
)


def get_floor_pricing_table(
    collection_name: str,
    selected_traits: List[str],
    strict_validation: bool = True,
    num_prices: int = 3,
) -> dict:
    print(f"Collection name: {collection_name}")
    print(f"Selected traits: {selected_traits}")
    print(f"Strict: {strict_validation}")

    market = MarketClient(MARKET_CONTRACT)
    client = Sg721Client.from_collection_name(collection_name)

    cache_dir = os.path.join(os.curdir, "cache", "collections")
    json_file = collection_name.lower().replace(" ", "-") + ".json"
    json_trait_cache_file = os.path.join(cache_dir, json_file)

    print("")
    collection = client.fetch_nft_collection(json_trait_cache_file)
    collection.export_json(json_trait_cache_file)
    print(f"Trait cache file stored at {json_trait_cache_file}")

    asks = market.fetch_asks_for_collection(collection, strict_verify=strict_validation)
    trait_asks = asks.create_asks_by_trait()

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
        if trait in ["hubble_rank", "id", "image", "name"]:
            continue
        for value, asks in values.items():
            row = [trait, value, str(len(asks))]
            for ask in asks[:num_prices]:
                row.extend([str(ask["ask"].price), str(ask["ask"].token_id)])
            row.extend([""] * (expected_length - len(row)))
            table.append(row)
    return table


args = parser.parse_args()
collection_name = args.collection
selected_traits = args.traits

table = get_floor_pricing_table(collection_name, selected_traits, args.strict)

if args.output == "csv":
    csv_file = collection_name.lower().replace(" ", "-") + ".csv"
    export_table_csv(table, csv_file)
    exit(0)

print_table(table)
