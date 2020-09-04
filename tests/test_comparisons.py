from random import random

import pytest

from uncertain_math import GivenValue


overlapping_values = (
    (GivenValue(-3, 2), GivenValue(-1, 1)),
    (GivenValue(+1, 2), GivenValue(-1, 1)),
    (GivenValue(+0, 2), GivenValue(+0, 4)),
    (GivenValue(+0, 4), GivenValue(+0, 2)),
)


@pytest.mark.parametrize(['a', 'b'], overlapping_values)
def test_equals(a, b):
    assert a == b
    assert a <= b
    assert a >= b
    assert not a < b
    assert not a > b
    assert not a != b


def test_less_than():
    a = GivenValue(random() * 10, random())
    b = GivenValue(a.max + 10, random())
    assert a < b
    assert a <= b
    assert a != b


def test_greater_than():
    a = GivenValue(random() * 10, random())
    b = GivenValue(a.max + 10, random())
    assert b > a
    assert b >= a
    assert b != a
