import logging

import requests

LOG = logging.getLogger(__name__)


def fetch_unstable_json(
    url: str,
    params: dict,
    expected_pages: int = None,
    expected_total: int = None,
    best_data=None,
    guessing=5,
):
    """Fetches JSON from an unstable stargaze URL. There is a bug
    in the current API that means that when querying transactions,
    the "total_count may return a different number each time. This
    method returns the most accurate number by querying the page
    multiple times and looking for the highest expected_total
    and expected_pages and using those as the best data.

    :param url: The paged URL to query
    :param params: The URL params
    :param expected_pages: The expected page count of the response
    :param expected_total: The expected total results
    :param best_data: The current "best" data from the URL
    :param guessing: The remaining guesses for the URL
    """
    data = requests.get(url, params=params).json()
    if "error" in data:
        return fetch_unstable_json(
            url, params, expected_pages, expected_total, best_data, guessing
        )

    page_count = int(data["page_total"])
    item_count = int(data["total_count"])

    if (
        guessing == 0
        and expected_total is not None
        and expected_pages is not None
        and expected_total == item_count
        and expected_pages == page_count
    ):
        LOG.info(f"Found {expected_pages} pages with {expected_total} items")
        return data

    if guessing == 0:
        return fetch_unstable_json(
            url, params, expected_pages, expected_total, best_data, 0
        )

    if expected_pages is None or expected_pages < page_count:
        expected_pages = page_count
        best_data = data
        LOG.debug(f"New expected page count: {expected_pages}")
    if expected_total is None or expected_total < item_count:
        expected_total = item_count
        best_data = data
        LOG.debug(f"New expected item count: {expected_total}")
    if guessing > 0:
        return fetch_unstable_json(
            url, params, expected_pages, expected_total, best_data, guessing - 1
        )

    LOG.info(f"Found {expected_pages} pages with {expected_total} items")
    return best_data


def fetch_unstable_paged_data(url, params, limit=100):
    """Fetches unstable paginated data based on a base URL,
    and a set of parameters. Sometimes stargaze API will return
    inconsistent data so this aims to and resolve the issue.

    :param url: The base txs URL
    :param params: The URL parameters
    :param limit: The item limit per page"""
    params["limit"] = limit
    params["page"] = 1
    LOG.info("Fetching initial page")
    data = fetch_unstable_json(url, params)
    pages = [data]
    known_total = int(data["total_count"])
    known_pages = int(data["page_total"])
    for i in range(2, known_pages + 1):
        LOG.info(f"Reading page {i}")
        params["page"] = i
        pages.append(
            fetch_unstable_json(url, params, known_pages, known_total, guessing=0)
        )
    return pages
