#!/usr/bin/env python3

import argparse
import logging
import os

import requests_cache

from stargazeutils.collection.sg721 import Sg721Client
from stargazeutils.ipfs import IpfsClient
from stargazeutils.stargaze import StargazeClient

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
This script fetches information for a given collection and then
begins fetching all token metadata from IPFS. The initial fetch
can take a while so if you want more detailed feedback, set the
logging level to DEBUG.

Once the metadata has been fetched, it's exported to JSON
file in the "cache/collections" directory so if the script is
run again, you will notice a distinct increase in speed.

If you have a private IPFS server, you also can set the IPFS_ROOT
environment variable to your root ipfs server. If set via argument,
any environment variable will be ignored.""",
)

parser.add_argument("collection_name", help="The name of the collection")
parser.add_argument(
    "--ipfs",
    metavar="IPFS_ROOT",
    type=str,
    required=False,
    help=(
        "Use an optional IPFS root address."
        "Can also be set via the IPFS_ROOT environment variable"
    ),
)
parser.add_argument(
    "--level",
    metavar="LOG_LEVEL",
    type=str,
    required=False,
    default="INFO",
    help="Sets the logging level. Can be DEBUG, INFO, WARNING, or CRITIAL",
)

args = parser.parse_args()

logging.basicConfig(level=args.level)

collection_name = args.collection_name
ipfs_root = args.ipfs or os.environ.get(
    "IPFS_ROOT", default="https://stargaze.mypinata.cloud"
)

requests_cache.install_cache("stargaze-ipfs")
sg_client = StargazeClient()
ipfs_client = IpfsClient(ipfs_root)
client = Sg721Client.from_collection_name(collection_name, sg_client, ipfs_client)

if client is None:
    print(f"Collection '{collection_name}' not found.")
    exit(1)

print("")
client.query_collection_info().print()
print(f"Minter: {client.minter}")
print("")
client.query_minter_config().print()
minted_tokens = client.query_num_minted_tokens()
print(f"Minted tokens: {minted_tokens}")

cache_dir = os.path.join(os.curdir, "cache", "collections")
json_file = collection_name.lower().replace(" ", "-") + ".json"
json_trait_cache_file = os.path.join(cache_dir, json_file)

print("")
traits = client.fetch_nft_collection(json_trait_cache_file)
traits.export_json(json_trait_cache_file)
print(f"Trait cache file stored at {json_trait_cache_file}")

print("")
traits.print_trait_rarity()
