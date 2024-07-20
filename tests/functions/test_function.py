import pytest
from unittest.mock import patch

from pyloadover.functions.function import Function, FunctionContext, CONFIG


def test_function_id(mock_function_context, mock_function_id_generator):
    return_value = Function(mock_function_context, id_generator=mock_function_id_generator).id

    mock_function_id_generator.generate_id.assert_called_once_with(mock_function_context)
    assert return_value == mock_function_id_generator.generate_id.return_value


@patch.dict('pyloadover.functions.function.CONFIG', {}, clear=True)
def test_function_reload_from_config(mock_function_context, mock_function_id_generator):
    CONFIG["function_id_generator"] = mock_function_id_generator
    function = Function(mock_function_context)

    function.reload_from_config()

    assert function.id_generator == CONFIG["function_id_generator"]


def _dummy_foo(a: int, b: str, c: bool = True):
    pass


@pytest.mark.parametrize("f, args,  kwargs", [
    (_dummy_foo, (1, "2"), {"c": True}),
    (_dummy_foo, (1, "2"), {})
])
def test_function_arguments_do_match_signature(f, args, kwargs):
    context = FunctionContext(f)
    assert Function(context).do_arguments_match_signature(*args, **kwargs)


@pytest.mark.parametrize("f, args,  kwargs", [
    (_dummy_foo, (), {}),
    (_dummy_foo, (1,), {}),
    (_dummy_foo, (1, 2), {"c": True}),
    (_dummy_foo, (1, "2"), {"c": 3}),
    (_dummy_foo, (1, "2"), {"c": True, "d": False}),
])
def test_function_arguments_do_not_match_signature(f, args, kwargs):
    context = FunctionContext(f)
    assert not Function(context).do_arguments_match_signature(*args, **kwargs)


def test_function_call_underlying_callable_exists(mock_function_context, mock_callable, args, kwargs):
    mock_function_context.underlying_callable = mock_callable

    Function(mock_function_context)(*args, **kwargs)

    mock_callable.assert_called_once_with(*args, **kwargs)


def test_function_call_underlying_callable_not_exists(mock_function_context, args, kwargs):
    mock_function_context.underlying_callable = None

    Function(mock_function_context)(*args, **kwargs)

    mock_function_context.callable.assert_called_once_with(*args, **kwargs)
