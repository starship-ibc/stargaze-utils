from datetime import datetime, timedelta
from stargazeutils.coin import Coin
from stargazeutils.collection import Whitelist

now = datetime.utcnow()

def test_whitelist_should_test_inequality():
    w1 = Whitelist(now, now + timedelta(1), Coin(148, 'ustars'), 1, 100, 20)
    w2 = Whitelist(now, now + timedelta(1), Coin(148, 'ustars'), 1, 100, 20)

    assert w1 == w2

def test_whitelist_given_unequal_start_time_should_be_unequal():
    w1 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20)
    w2 = Whitelist(now + timedelta(1), now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20)

    assert w1 != w2

def test_whitelist_given_unequal_end_time_should_be_unequal():
    w1 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20)
    w2 = Whitelist(now, now + timedelta(1), Coin(148, 'ustars'), 1, 100, 20)

    assert w1 != w2

def test_whitelist_given_unequal_price_should_be_unequal():
    w1 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20)
    w2 = Whitelist(now, now + timedelta(2), Coin(200, 'ustars'), 1, 100, 20)

    assert w1 != w2

def test_whitelist_given_unequal_limit_should_be_unequal():
    w1 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20)
    w2 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 2, 100, 20)

    assert w1 != w2

def test_whitelist_given_unequal_max_members_should_be_unequal():
    w1 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20)
    w2 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 200, 20)

    assert w1 != w2

def test_whitelist_given_unequal_member_count_should_be_unequal():
    w1 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20)
    w2 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 50)

    assert w1 != w2

def test_whitelist_given_unequal_active_should_be_unequal():
    w1 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20)
    w2 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20, False)

    assert w1 != w2

def test_whitelist_given_not_whitelist_should_be_unequal():
    w1 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20)

    assert w1 != {"name": "Alice"}

def test_whitelist_given_modified_should_be_unequal():
    w1 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20)
    w2 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20)
    
    w2.wl_name = "Mystery list"
    assert w1 != w2

    w1.name_it = "Whitelist"
    assert w1 != w2

def test_whitelist_should_print(capsys):
    w1 = Whitelist(now, now + timedelta(2), Coin(148, 'ustars'), 1, 100, 20)
    w1.print()
    out = capsys.readouterr().out
    assert len(out.split('\n')) == 8
