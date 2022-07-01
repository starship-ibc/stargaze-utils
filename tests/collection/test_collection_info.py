from stargazeutils.collection import CollectionInfo, RoyaltyInfo


def test_collection_info_should_parse_data():
    creator = "Alice"
    description = "Example NFT"
    payment_addr = "addr1"
    share = 0.1
    image_url = "ifps://image1"
    external_link = "https://www.example.com/"
    data = {
        "creator": creator,
        "description": description,
        "royalty_info": {"payment_address": payment_addr, "share": str(share)},
        "image": image_url,
        "external_link": external_link,
    }
    info = CollectionInfo.from_data(data)

    assert info.creator == creator
    assert info.description == description
    assert info.image_url == image_url
    assert info.external_link == external_link
    assert info.royalty_info.payment_address == payment_addr
    assert info.royalty_info.share == share


def test_collection_info_should_print_info(capsys):
    creator = "Alice"
    description = "Example NFT"
    payment_addr = "addr1"
    share = 0.1
    image_url = "ifps://image1"
    external_link = "https://www.example.com/"
    r = RoyaltyInfo(payment_addr, share)
    info = CollectionInfo(creator, description, r, image_url, external_link)

    info.print()
    captured = capsys.readouterr()
    assert creator in captured.out
    assert description in captured.out
    assert payment_addr in captured.out
    assert image_url in captured.out
    assert external_link in captured.out


def test_collection_info_equality():
    info1 = CollectionInfo(
        "creator", "description", RoyaltyInfo("addr", 0.02), "/images", "/link"
    )
    info2 = CollectionInfo(
        "creator", "description", RoyaltyInfo("addr", 0.02), "/images", "/link2"
    )

    assert info1 != info2
    info2.external_link = info1.external_link
    assert info1 != {"error": {}}

    info2.tmp = "tmp"
    assert info1 != info2

    info1.key = "key"
    assert info1 != info2
