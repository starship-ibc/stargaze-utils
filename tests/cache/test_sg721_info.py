import pytest

from stargazeutils.cache import SG721Info


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
