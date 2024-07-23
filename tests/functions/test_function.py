import pytest
from unittest.mock import patch

from typing import List, Dict, Optional, Any
from pyloadover.functions.function import Function, FunctionContext, CONFIG


def test_id_generator_attr(mock_function_context, mock_function_id_generator):
    function = Function(mock_function_context, mock_function_id_generator)

    assert function.id_generator == mock_function_id_generator


@patch.dict('pyloadover.functions.function.CONFIG', {}, clear=True)
def test_id_generator_attr_default_value_from_config(mock_function_context, mock_function_id_generator):
    CONFIG["function_id_generator"] = mock_function_id_generator

    function = Function(mock_function_context)

    assert function.id_generator == mock_function_id_generator


def test_id_property(mock_function_context, mock_function_id_generator):
    function = Function(mock_function_context, id_generator=mock_function_id_generator)

    return_value = function.id

    mock_function_id_generator.generate_id.assert_called_once_with(mock_function_context)
    assert return_value == mock_function_id_generator.generate_id.return_value


@patch.dict('pyloadover.functions.function.CONFIG', {}, clear=True)
def test_reload_from_config(mock_function_context, mock_function_id_generator):
    CONFIG["function_id_generator"] = mock_function_id_generator
    function = Function(mock_function_context)

    function.reload_from_config()

    assert function.id_generator == CONFIG["function_id_generator"]


def _dummy_foo(a: int, b: str, c: bool = True):
    pass


def _dummy_typed_foo(a: List[int], b: Dict[str, Any], c: Optional[bool]):
    pass


@pytest.mark.parametrize("f, args,  kwargs", [
    (_dummy_foo, (1, "2"), {"c": True}),
    (_dummy_foo, (1, "2"), {}),
    (_dummy_typed_foo, ([], {}, True), {}),
    (_dummy_typed_foo, ([1, 2], {"1": 1, "2": 2, "3": bool}), {"c": None})
])
def test_do_arguments_match_signature(f, args, kwargs):
    context = FunctionContext(f)

    assert Function(context).do_arguments_match_signature(*args, **kwargs)


@pytest.mark.parametrize("f, args,  kwargs", [
    (_dummy_foo, (), {}),
    (_dummy_foo, (1,), {}),
    (_dummy_foo, (1, 2), {"c": True}),
    (_dummy_foo, (1, "2"), {"c": 3}),
    (_dummy_foo, (1, "2"), {"c": True, "d": False}),
    (_dummy_typed_foo, (["1", "2"], {}, False), {}),
    (_dummy_typed_foo, ([], {1: 1}), {"c": True}),
    (_dummy_typed_foo, (["1", "2"], {}, False), {}),
    (_dummy_typed_foo, ([], {}, 1), {})
])
def test_do_arguments_not_match_signature(f, args, kwargs):
    context = FunctionContext(f)

    assert not Function(context).do_arguments_match_signature(*args, **kwargs)


def test_as_callable(mock_function_context, mock_callable, args, kwargs):
    mock_function_context.callable = mock_callable
    mock_function_context.underlying_callable = None

    return_value = Function(mock_function_context)(*args, **kwargs)

    mock_callable.assert_called_once_with(*args, **kwargs)
    assert return_value == mock_callable.return_value


def test_as_callable_calls_underlying_callable(mock_function_context, mock_callable, mock_underlying_callable,
                                               args, kwargs):
    mock_function_context.callable = mock_callable
    mock_function_context.underlying_callable = mock_underlying_callable

    return_value = Function(mock_function_context)(*args, **kwargs)

    mock_callable.assert_not_called()
    mock_underlying_callable.assert_called_once_with(*args, **kwargs)
    assert return_value == mock_underlying_callable.return_value
