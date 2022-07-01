import time
import requests
import logging

LOG = logging.getLogger(__name__)

def ipfs_to_http(ipfs_url: str) -> str:
        parts = ipfs_url.split("/")
        path = "/".join(parts[3:])
        return f"https://{parts[2]}.ipfs.dweb.link/{path}"

def get(ipfs_url: str, max_retries: int = 10, retry_delay: float = 0.5) -> requests.Response:
    http_url = ipfs_to_http(ipfs_url)
    count = 1
    while count <= max_retries:
        r = requests.get(http_url)
        if r.status_code == 200:
            return r
        LOG.warning(f"Error {count} processing url {http_url}: {r.status_code}")
        count +=1
        time.sleep(retry_delay)
    return r
