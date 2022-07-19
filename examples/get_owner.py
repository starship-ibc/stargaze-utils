#!/usr/bin/env python3

import argparse

from stargazeutils.collection import Sg721Client

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Gets the current owner for a given collection and token id.",
)
parser.add_argument(
    "collection_name", type=str, help="The name of the Stargaze collection"
)
parser.add_argument("token_id", type=int, help="The token id to query.")
args = parser.parse_args()

client = Sg721Client.from_collection_name(args.collection_name)
owner = client.query_owner_of_token(args.token_id)

print(f"Owner of {args.collection_name} {args.token_id} is {owner}")
