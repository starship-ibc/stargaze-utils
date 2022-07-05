import logging
import os
import sys

import requests_cache

from stargazeutils.collection.sg721 import Sg721Client

# We need to put this at the top before the inputs
# so the system respects the configuration.
logging.basicConfig(level=logging.INFO)

from stargazeutils.stargaze import QueryMethod, StargazeClient  # noqa: E402

requests_cache.install_cache("stargaze-ipfs")

sg_client = StargazeClient(query_method=QueryMethod.BINARY)
# sg_client.print_sg721_info(only_new=True)

if len(sys.argv) < 2:
    print("No collection specified.")
    exit(0)

collection_name = sys.argv[1]

client = Sg721Client.from_collection_name(collection_name, sg_client)

print("")
client.query_collection_info().print()
print("")
client.query_minter_config().print()

cache_dir = os.path.join(os.curdir, "cache", "collections")
json_file = collection_name.replace(" ", "-") + ".json"
json_trait_cache_file = os.path.join(cache_dir, json_file)

traits = client.fetch_nft_collection(json_trait_cache_file)
traits.export_json(json_trait_cache_file)

print("")
traits.print_trait_rarity()
