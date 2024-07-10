import pytest

from typing import List, Dict
from pyloadover.utils import is_instance, get_namespace


def _foo(a: int, b: str, c: bool = True):
    pass


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


def test_get_namespace():
    assert get_namespace(_foo) == "test_utils._foo"
