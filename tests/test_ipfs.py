from stargazeutils import ipfs


def test_ipfs_should_get_response(requests_mock):
    url = "ipfs://test/path"
    expected_json = {"data": {"result": "success"}}
    requests_mock.get("https://test.ipfs.dweb.link/path", json=expected_json)

    data = ipfs.get(url).json()
    assert data == expected_json


def test_ipfs_should_retry(requests_mock):
    url = "ipfs://test/path"
    expected_json = {"data": {"result": "success"}}
    requests_mock.get(
        "https://test.ipfs.dweb.link/path",
        [
            {"status_code": 500},
            {"status_code": 500},
            {"json": expected_json, "status_code": 200},
        ],
    )

    data = ipfs.get(url, retry_delay=0.01).json()
    assert data == expected_json


def test_ipfs_should_return_last_error(requests_mock):
    url = "ipfs://test/path"
    requests_mock.get("https://test.ipfs.dweb.link/path", [{"status_code": 500}])

    r = ipfs.get(url, retry_delay=0.01)
    assert r.status_code == 500
