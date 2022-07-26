from datetime import datetime

from stargazeutils.coin import Coin
from stargazeutils.collection.minter_config import MinterConfig

now = datetime.utcnow()


def test_minter_config_equality():
    c1 = MinterConfig(
        "admin", "/base", 5, 2, "addr1", "1", now, Coin("148000000", "ustars")
    )
    c2 = MinterConfig(
        "admin", "/base", 5, 2, "addr1", "1", now, Coin("148000000", "ustars")
    )

    assert c1 == c2
    assert c1 != {"a": {}}

    c2.admin = "new"
    assert c1 != c2

    c2.admin = c1.admin
    assert c1 == c2

    c2.key1 = "key1"
    assert c1 != c2

    c1.key2 = "key2"
    assert c1 != c2


def test_minter_config_should_print(capsys):
    m1 = MinterConfig(
        "admin", "/base", 3, 1, "addr1", "1", now, Coin("138000", "ustars")
    )
    m1.print()
    out = capsys.readouterr().out
    assert len(out.split("\n")) == 10
