import os
import shutil

import pytest

from stargazeutils.cache import SG721Cache, SG721Info
from tests.assets import test_sg721_cache_csv_path


def test_sg721_info_should_return_csv_row():
    info = SG721Info("addr", "name", "symbol", "minter")
    row = info.as_csv_row()
    assert row == '"addr","name","symbol","minter"'


def test_sg721_info_should_parse_csv_row():
    row = '"addr","name","symbol","minter"\n'
    info = SG721Info.parse_csv_row(row)
    assert info.sg721 == "addr"
    assert info.name == "name"
    assert info.symbol == "symbol"
    assert info.minter == "minter"


def test_sg721_info_can_be_represented_for_debugging():
    row = '"addr","name","symbol","minter"\n'
    info = SG721Info.parse_csv_row(row)
    assert info.name in info.__repr__()


def test_sg721_info_given_invalid_row_should_raise_exception():
    row = '"invalidrow"'
    with pytest.raises(ValueError):
        SG721Info.parse_csv_row(row)
    assert True


def test_sg721_cache_should_create_csv_when_not_exists():
    filename = "testcache.tmp"
    assert not os.path.exists(filename)

    cache = SG721Cache(filename)
    cache.save_csv()

    assert os.path.exists(filename)
    os.remove(filename)


def test_sg721_cache_should_load_csv():
    cache = SG721Cache(test_sg721_cache_csv_path)
    assert "addr1" in cache._sg721
    assert cache._sg721["addr1"].sg721 == "addr1"
    assert cache._sg721["addr1"].name == "name1"
    assert cache._sg721["addr1"].symbol == "symbol1"
    assert cache._sg721["addr1"].minter == "minter1"

    assert "addr2" in cache._sg721
    assert cache._sg721["addr2"].sg721 == "addr2"
    assert cache._sg721["addr2"].name == "name2"
    assert cache._sg721["addr2"].symbol == "symbol2"
    assert cache._sg721["addr2"].minter == "minter2"


def test_sg721_cache_should_save_csv():
    backup_path = "./sg721-backup.csv"
    new_sg721 = "addr3"

    shutil.copyfile(test_sg721_cache_csv_path, backup_path)
    try:
        cache = SG721Cache(test_sg721_cache_csv_path)
        assert new_sg721 not in cache._sg721
        cache.update_sg721_contract_info(
            new_sg721, {"name": "name3", "symbol": "symbol3"}
        )
        cache.update_sg721_minter(new_sg721, "minter3")
        cache.save_csv()

        cache2 = SG721Cache(test_sg721_cache_csv_path)
    finally:
        shutil.copyfile(backup_path, test_sg721_cache_csv_path)
        os.remove(backup_path)

    assert new_sg721 in cache2._sg721
    assert cache._sg721[new_sg721].sg721 == "addr3"
    assert cache._sg721[new_sg721].name == "name3"
    assert cache._sg721[new_sg721].symbol == "symbol3"
    assert cache._sg721[new_sg721].minter == "minter3"


def test_sg721_cache_has_sg721_info_should_return_true():
    addr = "test-addr"
    cache = SG721Cache(test_sg721_cache_csv_path)
    cache._sg721[addr] = SG721Info(addr, "name", "symbol")
    assert cache.has_sg721_info(addr)


def test_sg721_cache_not_has_sg721_info_should_return_false():
    cache = SG721Cache(test_sg721_cache_csv_path)
    assert not cache.has_sg721_info("nothere")


def test_sg721_cache_given_only_minter_has_sg721_info_should_return_false():
    addr = "test-addr"
    cache = SG721Cache(test_sg721_cache_csv_path)
    cache._sg721[addr] = SG721Info(addr, minter="minter")
    assert not cache.has_sg721_info(addr)


def test_sg721_cache_has_minter_should_return_true():
    addr = "test-addr"
    cache = SG721Cache(test_sg721_cache_csv_path)
    cache._sg721[addr] = SG721Info(addr, minter="minter")
    assert cache.has_sg721_minter(addr)


def test_sg721_cache_not_has_minter_should_return_false():
    cache = SG721Cache(test_sg721_cache_csv_path)
    assert not cache.has_sg721_minter("nothere")


def test_sg721_cache_given_only_info_has_minter_should_return_false():
    addr = "test-addr"
    cache = SG721Cache(test_sg721_cache_csv_path)
    cache._sg721[addr] = SG721Info(addr, "name", "symbol")
    assert not cache.has_sg721_minter(addr)


def test_sg721_cache_has_complete_data_should_return_true():
    addr = "test-addr"
    cache = SG721Cache(test_sg721_cache_csv_path)
    cache._sg721[addr] = SG721Info(addr, "name", "symbol", "minter")
    assert cache.has_complete_data(addr)


def test_sg721_cache_given_unknown_has_complete_data_should_return_false():
    cache = SG721Cache(test_sg721_cache_csv_path)
    assert not cache.has_complete_data("notthere")


def test_sg721_cache_no_info_has_complete_data_should_return_false():
    addr = "test-addr"
    cache = SG721Cache(test_sg721_cache_csv_path)
    cache._sg721[addr] = SG721Info(addr, minter="minter")
    assert not cache.has_complete_data(addr)


def test_sg721_cache_no_minter_has_complete_data_should_return_false():
    addr = "test-addr"
    cache = SG721Cache(test_sg721_cache_csv_path)
    cache._sg721[addr] = SG721Info(addr, "name", "symbol")
    assert not cache.has_complete_data(addr)


def test_sg721_cache_when_cached_should_get_info():
    addr = "addr1"
    cache = SG721Cache(test_sg721_cache_csv_path)
    assert addr in cache._sg721
    assert cache._sg721[addr].sg721 == "addr1"
    assert cache._sg721[addr].name == "name1"
    assert cache._sg721[addr].symbol == "symbol1"
    assert cache._sg721[addr].minter == "minter1"


def test_sg721_cache_when_not_cached_should_get_none():
    cache = SG721Cache(test_sg721_cache_csv_path)
    assert cache.get_sg721_info("nothere") is None


def test_sg721_cache_should_update_info_from_data():
    addr = "addr-test"
    expected_info = SG721Info(addr, "test-name", "test-symbol", "test-minter")
    cache = SG721Cache(test_sg721_cache_csv_path)
    cache._sg721[addr] = expected_info

    info1 = cache.get_sg721_info(addr)
    assert info1.name == expected_info.name
    assert info1.symbol == expected_info.symbol
    assert info1.minter == expected_info.minter

    info2 = cache.update_sg721_contract_info(
        addr, {"name": "newname", "symbol": "newsymbol"}
    )
    assert info2.name == "newname"
    assert info2.symbol == "newsymbol"
    assert info2.minter == expected_info.minter

    info3 = cache.get_sg721_info(addr)
    assert info3.name == "newname"
    assert info3.symbol == "newsymbol"
    assert info3.minter == expected_info.minter


def test_sg721_cache_should_update_minter():
    addr = "addr-test"
    expected_info = SG721Info(addr, "test-name", "test-symbol", "test-minter")
    cache = SG721Cache(test_sg721_cache_csv_path)
    cache._sg721[addr] = expected_info

    info1 = cache.get_sg721_info(addr)
    assert info1.name == expected_info.name
    assert info1.symbol == expected_info.symbol
    assert info1.minter == expected_info.minter

    info2 = cache.update_sg721_minter(addr, "newminter")
    assert info2.name == expected_info.name
    assert info2.symbol == expected_info.symbol
    assert info2.minter == "newminter"

    info2 = cache.get_sg721_info(addr)
    assert info2.name == expected_info.name
    assert info2.symbol == expected_info.symbol
    assert info2.minter == expected_info.minter
