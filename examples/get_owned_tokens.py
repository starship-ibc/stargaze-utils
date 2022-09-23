#!/usr/bin/env python3

import argparse
import os

from stargazeutils.collection import Sg721Client
from stargazeutils.common import print_table, slugified

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
Fetches info on the currently owned tokens in a collection for a
given address and prints out the results as a table with token
trait information. This table can be customized by excluding
specific traits (often image or name) and can be sorted by any
of the column headers.

Example:

poetry run python examples/get_owned_tokens.py \
    "Stargaze Punks" \
    stars1zja6krwtcaa2ushn3z2m658k38qlg9qwg8casg \
    --excluded_traits image name Glow Eyes Hair Mouth Bubble \
    --sort hubble_rank
""",
)
parser.add_argument(
    "collection_name", type=str, help="The name of the collection to query"
)
parser.add_argument(
    "owner_addr", type=str, help="The owner's stars address to check for owned tokens"
)
parser.add_argument(
    "--excluded_traits",
    metavar="TRAIT",
    type=str,
    default=[],
    required=False,
    nargs="+",
    help="Optional traits to exclude from the printout",
)
parser.add_argument(
    "--sort",
    metavar="TRAIT",
    type=str,
    default=None,
    required=False,
    help="An optional trait for sorting the output table",
)
args = parser.parse_args()
collection_name = args.collection_name
owner_addr = args.owner_addr

client = Sg721Client.from_collection_name(collection_name)
tokens = client.query_tokens_owned_by(owner_addr)

print("---")
print(f"Collection {collection_name}")
print(f"Owner: {owner_addr}")
print(f"Owned tokens: {len(tokens)}")

cache_dir = os.path.join(os.curdir, "cache", "collections")
json_file = slugified(collection_name)
json_trait_cache_file = os.path.join(cache_dir, json_file)

print("")
collection = client.fetch_nft_collection(json_trait_cache_file)
collection.export_json(json_trait_cache_file)
print(f"Trait cache file stored at {json_trait_cache_file}")

tokens_table = collection.get_tokens_info_table(
    tokens, excluded_traits=args.excluded_traits, sort_key=args.sort
)
print_table(tokens_table)
