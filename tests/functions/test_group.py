import pytest
from unittest.mock import patch

from pyloadover.functions.function import Function, FunctionContext, CONFIG


def test_function_id(mock_function_context, mock_function_id_generator):
    return_value = Function(mock_function_context, id_generator=mock_function_id_generator).id

    mock_function_id_generator.generate_id.asser_called_once_with(mock_function_context)
    assert return_value == mock_function_id_generator.generate_id.return_value


@patch.dict('pyloadover.functions.function.CONFIG', {}, clear=True)
def test_function_reload_from_config(mock_function_context, mock_function_id_generator):
    CONFIG["function_id_generator"] = mock_function_id_generator
    function = Function(mock_function_context)

    function.reload_from_config()

    assert function.id_generator == CONFIG["function_id_generator"]


def _foo(a: int, b: str, c: bool = True):
    return a, b, c


@pytest.mark.parametrize("f, args,  kwargs", [
    (_foo, (1, "2"), {"c": True}),
    (_foo, (1, "2"), {})
])
def test_function_arguments_do_match_signature(f, args, kwargs):
    context = FunctionContext(f)
    assert Function(context).do_arguments_match_signature(*args, **kwargs)


@pytest.mark.parametrize("f, args,  kwargs", [
    (_foo, (), {}),
    (_foo, (1,), {}),
    (_foo, (1, 2), {"c": True}),
    (_foo, (1, "2"), {"c": 3}),
    (_foo, (1, "2"), {"c": True, "d": False}),
])
def test_function_arguments_do_not_match_signature(f, args, kwargs):
    context = FunctionContext(f)
    assert not Function(context).do_arguments_match_signature(*args, **kwargs)
