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
