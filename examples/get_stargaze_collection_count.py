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

import requests_cache

from stargazeutils.collection import Sg721Client
from stargazeutils.common import export_table_csv, print_table
from stargazeutils.stargaze import QueryMethod, StargazeClient

logging.basicConfig(level=logging.INFO)
requests_cache.install_cache("stargaze-node")

sg_client = StargazeClient(query_method=QueryMethod.REST)
contracts = sg_client.fetch_contracts(1)

table = [["Name", "Tokens", "Minted"]]
for contract in contracts:
    info = sg_client.fetch_sg721_contract_info(contract)
    info = sg_client.fetch_sg721_minter(contract)
    print(f"- Fetched info for <{info.sg721}> {info.name}")

    sg721 = Sg721Client(info.sg721, info.minter, sg_client=sg_client)
    minter_config = sg721.query_minter_config()
    minted_tokens = sg721.query_num_minted_tokens()
    table.append([info.name, minter_config.num_tokens, minted_tokens])

print_table(table)
export_table_csv(table, "collections.csv")
