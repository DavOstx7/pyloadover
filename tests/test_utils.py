import pytest

import functools
from typing import List, Dict
from pyloadover.utils import is_instance, get_underlying_callable


@pytest.mark.parametrize("value, annotation", [
    (1, int),
    ("2", str),
    ([1, 2, 3], list),
    (["1", "2", "3"], List[str]),
    ({1: 1, 2: 2}, dict),
    ({"1": "2", "2": "2"}, Dict[str, str])
])
def test_is_instance(value, annotation):
    assert is_instance(value, annotation)


@pytest.mark.parametrize("value, annotation", [
    (1, bool),
    ("2", bool),
    ([1, 2, 3], dict),
    (["1", "2", "3"], Dict[str, str]),
    ({1: 1, 2: 2}, list),
    ({"1": "2", "2": "2"}, List[str])
])
def test_is_not_instance(value, annotation):
    assert not is_instance(value, annotation)


def _dummy_decorator(func):
    @functools.wraps(func)
    def _dummy_wrapper(*args, **kwargs):
        pass

    return _dummy_wrapper


def test_get_underlying_callable():
    def _foo():
        pass

    class _Foo:
        def _foo(self):
            pass

    assert _foo == get_underlying_callable(classmethod(staticmethod(_dummy_decorator(_foo))))
    assert _foo == get_underlying_callable(_dummy_decorator(staticmethod(classmethod(_foo))))

    assert _Foo._foo == get_underlying_callable(classmethod(staticmethod(_dummy_decorator(_Foo._foo))))
    assert _Foo._foo == get_underlying_callable(_dummy_decorator(staticmethod(classmethod(_Foo._foo))))


def test_get_underlying_callable_returns_none(foo_callable):
    def _foo():
        pass

    class _Foo:
        def _foo(self):
            pass

    assert get_underlying_callable(_foo) is None
    assert get_underlying_callable(_Foo._foo) is None
