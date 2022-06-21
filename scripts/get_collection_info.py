import logging

# We need to put this at the top before the inputs
# so the system respects the configuration.
logging.basicConfig(level=logging.INFO)

from stargazeutils.stargaze import QueryMethod, StargazeClient  # noqa: E402

sg_client = StargazeClient(query_method=QueryMethod.BINARY)
info = sg_client.print_sg721_info(only_new=True)
