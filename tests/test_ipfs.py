from requests_mock import ANY as ANY_url

from stargazeutils import ipfs
from tests.assets import test_vals


def test_ipfs_should_get_response(requests_mock):
    url = f"ipfs://{test_vals.ipfs_cid}/path"
    expected_json = {"data": {"result": "success"}}
    requests_mock.get(
        ANY_url,
        json=expected_json,
    )

    data = ipfs.get(url).json()
    assert data == expected_json


def test_ipfs_should_retry(requests_mock):
    url = f"ipfs://{test_vals.ipfs_cid}/path"
    expected_json = {"data": {"result": "success"}}
    requests_mock.get(
        ANY_url,
        [
            {"status_code": 500},
            {"status_code": 500},
            {"json": expected_json, "status_code": 200},
        ],
    )

    data = ipfs.get(url, retry_delay=0.01).json()
    assert data == expected_json


def test_ipfs_should_return_last_error(requests_mock):
    url = f"ipfs://{test_vals.ipfs_cid}/path"
    requests_mock.get(
        ANY_url,
        [{"status_code": 500}],
    )

    r = ipfs.get(url, retry_delay=0.01)
    assert r.status_code == 500
