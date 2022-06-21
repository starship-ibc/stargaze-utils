import os
import shutil

from stargazeutils.cache import Sg721Cache, Sg721Info
from tests.assets import test_sg721_cache_csv_path


def test_sg721_info_should_get_csv_row():
    info = Sg721Info("addr", "name", "symbol", "minter")
    row = info.get_csv_row()
    assert row == '"addr","name","symbol","minter"'


def test_sg721_info_should_parse_csv_row():
    row = '"addr","name","symbol","minter"\n'
    info = Sg721Info.parse_csv_row(row)
    assert info.sg721 == "addr"
    assert info.name == "name"
    assert info.symbol == "symbol"
    assert info.minter == "minter"


def test_sg721_cache_should_load_csv():
    cache = Sg721Cache(test_sg721_cache_csv_path)
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
    cache = Sg721Cache(test_sg721_cache_csv_path)
    assert new_sg721 not in cache._sg721
    cache.update_sg721_contract_info(new_sg721, {"name": "name3", "symbol": "symbol3"})
    cache.update_sg721_minter(new_sg721, "minter3")
    cache.save_csv()

    cache2 = Sg721Cache(test_sg721_cache_csv_path)
    shutil.copyfile(backup_path, test_sg721_cache_csv_path)
    os.remove(backup_path)

    assert new_sg721 in cache2._sg721
    assert cache._sg721[new_sg721].sg721 == "addr3"
    assert cache._sg721[new_sg721].name == "name3"
    assert cache._sg721[new_sg721].symbol == "symbol3"
    assert cache._sg721[new_sg721].minter == "minter3"


def test_sg721_cache_has_sg721_info_should_return_true():
    cache = Sg721Cache(test_sg721_cache_csv_path)
    assert cache.has_sg721_info("addr1")


def test_sg721_cache_not_has_sg721_info_should_return_false():
    cache = Sg721Cache(test_sg721_cache_csv_path)
    assert not cache.has_sg721_info("nothere")


def test_sg721_cache_has_minter_should_return_true():
    cache = Sg721Cache(test_sg721_cache_csv_path)
    assert cache.has_sg721_minter("addr1")


def test_sg721_cache_not_has_minter_should_return_false():
    cache = Sg721Cache(test_sg721_cache_csv_path)
    assert not cache.has_sg721_minter("nothere")


def test_sg721_cache_has_complete_data_should_return_true():
    cache = Sg721Cache(test_sg721_cache_csv_path)
    assert cache.has_complete_data("addr1")


def test_sg721_cache_no_info_has_complete_data_should_return_false():
    cache = Sg721Cache(test_sg721_cache_csv_path)
    assert not cache.has_complete_data("onlyminter")


def test_sg721_cache_no_minter_has_complete_data_should_return_false():
    cache = Sg721Cache(test_sg721_cache_csv_path)
    assert not cache.has_complete_data("onlyinfo")


def test_sg721_cache_when_cached_should_get_info():
    addr = "addr1"
    cache = Sg721Cache(test_sg721_cache_csv_path)
    assert addr in cache._sg721
    assert cache._sg721[addr].sg721 == "addr1"
    assert cache._sg721[addr].name == "name1"
    assert cache._sg721[addr].symbol == "symbol1"
    assert cache._sg721[addr].minter == "minter1"


def test_sg721_cache_when_not_cached_should_get_none():
    cache = Sg721Cache(test_sg721_cache_csv_path)
    assert cache.get_sg721_info("nothere") is None


def test_sg721_cache_should_update_info_from_data():
    addr = "addr1"
    cache = Sg721Cache(test_sg721_cache_csv_path)
    cache.update_sg721_contract_info(addr, {"name": "newname", "symbol": "newsymbol"})
    info = cache.get_sg721_info(addr)
    assert info.name == "newname"
    assert info.symbol == "newsymbol"
    assert info.minter == "minter1"


def test_sg721_cache_should_update_minter():
    addr = "addr1"
    cache = Sg721Cache(test_sg721_cache_csv_path)
    cache.update_sg721_minter(addr, "newminter")
    info = cache.get_sg721_info(addr)
    assert info.name == "name1"
    assert info.symbol == "symbol1"
    assert info.minter == "newminter"
