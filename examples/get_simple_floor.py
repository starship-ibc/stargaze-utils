#!/usr/bin/env python3

import argparse

from stargazeutils.collection import Sg721Client
from stargazeutils.market import MarketClient
from stargazeutils.market.market_ask import DEFAULT_MARKET_CONTRACT

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
Fetch the current floor of a Stargaze Collection

Examples:

    python3 get_simple_floor.py "Stargaze Punks"

    """,
)

parser.add_argument("collection", type=str, help="The name of the Stargaze Collection.")


args = parser.parse_args()
collection_name = args.collection

print(f"Collection name: {collection_name}")

market = MarketClient(DEFAULT_MARKET_CONTRACT)
client = Sg721Client.from_collection_name(collection_name)
ask = market.query_floor_price(client.sg721)

print(ask)
