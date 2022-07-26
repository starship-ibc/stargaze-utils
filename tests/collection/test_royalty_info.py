from stargazeutils.collection import RoyaltyInfo


def test_royalty_info_should_parse_json():
    addr = "addr1"
    share = 0.1
    data = {"payment_address": addr, "share": str(share)}
    r = RoyaltyInfo.from_data(data)

    assert r.payment_address == addr
    assert r.share == share


def test_royalty_info_should_represent_object():
    addr = "addr1"
    royalty = 10
    r = RoyaltyInfo(addr, royalty / 100)
    assert str(royalty) in r.__repr__()
    assert addr in r.__repr__()


def test_royalty_info_equality():
    r1 = RoyaltyInfo("addr1", "0.1")
    r2 = RoyaltyInfo("addr1", "0.1")

    assert r1 == r2
    assert r1 != {"a": {}}

    r2.payment_address = "new"
    assert r1 != r2

    r2.payment_address = r1.payment_address
    assert r1 == r2

    r2.key1 = "key1"
    assert r1 != r2

    r1.key2 = "key2"
    assert r1 != r2
