import pytest
from unittest.mock import patch, MagicMock

from pyloadover.function import Function


@pytest.mark.parametrize("args,  kwargs", [
    ((1, "2"), {"c": True}),
    ((1, "2"), {})
])
def test_arguments_match_signature(args, kwargs, foo):
    assert Function(foo).do_arguments_match_signature(*args, **kwargs)


@pytest.mark.parametrize("args,  kwargs", [
    ((), {}),
    ((1,), {}),
    ((1, 2), {"c": True}),
    ((1, "2"), {"c": 3}),
    ((1, "2"), {"c": True, "d": False}),
])
def test_arguments_not_match_signature(args, kwargs, foo):
    assert not Function(foo).do_arguments_match_signature(*args, **kwargs)


@patch('pyloadover.function.get_namespace', autospec=True)
def test_function_namespace_property(mock_get_namespace: MagicMock, foo):
    return_value = Function(foo).namespace

    mock_get_namespace.assert_called_once_with(foo)
    assert return_value == mock_get_namespace.return_value
