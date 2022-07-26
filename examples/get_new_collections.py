#!/usr/bin/env python3
#
# This script prints out a list of new collections
# since the last time this script was run. It also
# automatically updates the local cache file that
# holds the SG721 and minter information for each
# collection.
#
# Usage:
#  poetry run python3 examples/get_new_collections.py

import logging

# We need to put this at the top before the inputs
# so the system respects the configuration.
logging.basicConfig(level=logging.INFO)

from stargazeutils.stargaze import QueryMethod, StargazeClient  # noqa: E402

sg_client = StargazeClient(query_method=QueryMethod.BINARY)
sg_client.print_sg721_info(only_new=True)
