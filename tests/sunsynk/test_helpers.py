"""Test helpers."""
from sunsynk.helpers import SSTime, ensure_tuple, signed, int_round
from sunsynk.sensors import Sensor


def test_int_round() -> None:
    res1 = int_round(1.0)
    assert isinstance(res1, int)
    assert res1 == 1


def test_ensure_tuple() -> None:
    assert ensure_tuple(1) == (1,)
    assert ensure_tuple((1,)) == (1,)
    assert ensure_tuple((1, 5)) == (1, 5)
    assert ensure_tuple("a") == ("a",)


def test_signed() -> None:
    assert signed(0x7FFF) == 0x7FFF
    assert signed(0xFFFF) == 0


def test_signeds() -> None:
    """Signed sensors have a -1 factor"""
    s = Sensor(1, "", "", factor=-1)
    assert s.reg_to_value(1) == 1
    assert s.reg_to_value(0xFFFE) == -1

    s = Sensor(1, "", "", factor=1)
    assert s.reg_to_value(1) == 1
    assert s.reg_to_value(0xFFFE) == 0xFFFE
    assert s.reg_to_value((1, 1)) == 0x10001


def test_time() -> None:
    time = SSTime(10)
    assert time.str_value == "0:10"
    assert time.reg_value == 10
    time.str_value = "0:10"
    assert time.minutes == 10
    time.str_value = "00:10"
    assert time.minutes == 10
    time.reg_value = 10
    assert time.minutes == 10

    time = SSTime(100)
    assert time.str_value == "1:40"
    assert time.reg_value == 140
    time.str_value = "1:40"
    assert time.minutes == 100
    time.str_value = "01:40"
    assert time.minutes == 100
    time.reg_value = 140
    assert time.minutes == 100

    just_before_midnight = 23 * 60 + 59
    time = SSTime(just_before_midnight)
    assert time.str_value == "23:59"
    assert time.reg_value == 2359
    time.str_value = "23:59"
    assert time.minutes == just_before_midnight
    time.reg_value = 2359
    assert time.minutes == just_before_midnight