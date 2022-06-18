import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("stargazeutils.cache.sg721cache").setLevel(logging.INFO)

from stargazeutils.stargaze import QueryMethod, StargazeClient

sg_client = StargazeClient(query_method=QueryMethod.BINARY)

info = sg_client.print_sg721_info(only_new=True)
