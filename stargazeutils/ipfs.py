import logging
import time

import requests

LOG = logging.getLogger(__name__)


def ipfs_to_http(ipfs_url: str) -> str:
    """Converts an IPFS address to an HTTPS address. Currently
    only dweb.link is supported.

    Arguments:
    - ipfs_url: The IPFS url to convert."""
    parts = ipfs_url.split("/")
    path = "/".join(parts[3:])
    return f"https://{parts[2]}.ipfs.dweb.link/{path}"


def get(
    ipfs_url: str, max_retries: int = 10, retry_delay: float = 0.5
) -> requests.Response:
    """Gets the response from an IPFS url. Because IPFS is not
    stable, a built-in retry and delay mechanism is included. If,
    after the max_retries, a 200 response is still not received, then
    the most recent (failed) response will be returned.

    Arguments
    - ipfs_url: The url to fetch
    - max_retries: Number of retries before giving up
    - retry_delay: The delay in seconds between retrying
    """
    http_url = ipfs_to_http(ipfs_url)
    count = 1
    while count <= max_retries:
        r = requests.get(http_url)
        if r.status_code == 200:
            return r
        LOG.warning(f"Error {count} processing url {http_url}: {r.status_code}")
        count += 1
        time.sleep(retry_delay)
    return r
