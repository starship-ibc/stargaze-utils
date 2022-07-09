#!/usr/bin/env python3
#
# This scripts gets the current owner for a given
# collection and token id.

import sys

from stargazeutils.collection import Sg721Client

if len(sys.argv) < 3:
    print("Need to specify a collection name and token id")
    exit(1)

collection_name = sys.argv[1]
token_id = sys.argv[2]

client = Sg721Client.from_collection_name(collection_name)
owner = client.query_owner_of_token(token_id)

print(f"Owner of {collection_name} {token_id} is {owner}")
