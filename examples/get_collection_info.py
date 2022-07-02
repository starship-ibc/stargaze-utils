import logging
import sys

import requests_cache

from stargazeutils.collection.sg721 import Sg721Client

# We need to put this at the top before the inputs
# so the system respects the configuration.
logging.basicConfig(level=logging.INFO)

from stargazeutils.stargaze import QueryMethod, StargazeClient  # noqa: E402

requests_cache.install_cache("stargaze-ipfs")

sg_client = StargazeClient(query_method=QueryMethod.BINARY)
sg_client.print_sg721_info(only_new=True)

collection_name = sys.argv[1]

info = sg_client._sg721_cache.get_sg721_info_from_name(collection_name)
client = Sg721Client(info.sg721, info.minter, sg_client)

client.query_collection_info().print()
client.query_minter_config().print()

# client.fetch_traits()
