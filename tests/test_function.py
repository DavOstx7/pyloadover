import pytest
from unittest.mock import patch, MagicMock

from pyloadover.function import Function


def _foo(a: int, b: str, c: bool = True):
    pass


@pytest.mark.parametrize("f, args,  kwargs", [
    (_foo, (1, "2"), {"c": True}),
    (_foo, (1, "2"), {})
])
def test_arguments_match_signature(f, args, kwargs):
    assert Function(f).do_arguments_match_signature(*args, **kwargs)


@pytest.mark.parametrize("f, args,  kwargs", [
    (_foo, (), {}),
    (_foo, (1,), {}),
    (_foo, (1, 2), {"c": True}),
    (_foo, (1, "2"), {"c": 3}),
    (_foo, (1, "2"), {"c": True, "d": False}),
])
def test_arguments_not_match_signature(f, args, kwargs):
    assert not Function(f).do_arguments_match_signature(*args, **kwargs)


@patch('pyloadover.function.get_namespace', autospec=True)
def test_function_namespace(mock_get_namespace: MagicMock):
    return_value = Function(_foo).namespace

    mock_get_namespace.assert_called_once_with(_foo)
    assert return_value == mock_get_namespace.return_value
