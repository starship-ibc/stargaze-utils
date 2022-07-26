from stargazeutils.ipfs import IpfsClient
from tests.assets import test_vals


def test_ipfs_should_get_response(requests_mock):
    root_url = "https://example.com/"
    ipfs = IpfsClient(ipfs_root=root_url)

    url = f"ipfs://{test_vals.ipfs_cid}/path"
    expected_json = {"data": {"result": "success"}}
    print(f"{root_url}ipfs/{test_vals.ipfs_cid}/path")
    requests_mock.get(
        f"{root_url}ipfs/{test_vals.ipfs_hash}/path",
        json=expected_json,
    )

    data = ipfs.get(url).json()
    assert data == expected_json


def test_ipfs_should_retry(requests_mock):
    root_url = "https://example.com/"
    ipfs = IpfsClient(ipfs_root=root_url)

    url = f"ipfs://{test_vals.ipfs_cid}/path"
    expected_json = {"data": {"result": "success"}}
    requests_mock.get(
        f"{root_url}ipfs/{test_vals.ipfs_hash}/path",
        [
            {"status_code": 500},
            {"status_code": 500},
            {"json": expected_json, "status_code": 200},
        ],
    )

    data = ipfs.get(url, retry_delay=0.01).json()
    assert data == expected_json


def test_ipfs_should_return_last_error(requests_mock):
    root_url = "https://example.com/"
    ipfs = IpfsClient(ipfs_root=root_url)

    url = f"ipfs://{test_vals.ipfs_cid}/path"
    requests_mock.get(
        f"{root_url}ipfs/{test_vals.ipfs_hash}/path",
        [{"status_code": 500}],
    )

    r = ipfs.get(url, retry_delay=0.01)
    assert r.status_code == 500
