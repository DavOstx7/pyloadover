import pytest
from unittest.mock import patch, MagicMock

from pyloadover.functions.function import Function, FunctionContext, FunctionIdGenerator


def test_function_id():
    mock_context = MagicMock(spec_set=FunctionContext)
    mock_id_generator = MagicMock(spec_set=FunctionIdGenerator)

    return_value = Function(mock_context, id_generator=mock_id_generator).id

    mock_id_generator.generate_id.asser_called_once_with(mock_context)
    assert return_value == mock_id_generator.generate_id.return_value


@patch('pyloadover.functions.function.CONFIG', autospec=True)
def test_function_reload_from_config(mock_CONFIG):
    mock_context = MagicMock(spec_set=FunctionContext)

    function = Function(mock_context)
    function.reload_from_config()

    assert function.id_generator == mock_CONFIG["function_id_generator"]


def _foo(a: int, b: str, c: bool = True):
    return a, b, c


@pytest.mark.parametrize("_object, args,  kwargs", [
    (_foo, (1, "2"), {"c": True}),
    (_foo, (1, "2"), {})
])
def test_function_arguments_do_match(_object, args, kwargs):
    context = FunctionContext(_object)
    assert Function(context).do_arguments_match(*args, **kwargs)


@pytest.mark.parametrize("_object, args,  kwargs", [
    (_foo, (), {}),
    (_foo, (1,), {}),
    (_foo, (1, 2), {"c": True}),
    (_foo, (1, "2"), {"c": 3}),
    (_foo, (1, "2"), {"c": True, "d": False}),
])
def test_function_arguments_do_not_match(_object, args, kwargs):
    context = FunctionContext(_foo)
    assert not Function(context).do_arguments_match(*args, **kwargs)
