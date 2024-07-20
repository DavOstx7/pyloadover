from unittest.mock import patch, MagicMock

from pyloadover.functions.context import FunctionContext


def test_function_context_properties(mock_callable):
    context = FunctionContext(mock_callable)

    assert context.callable == mock_callable
    assert context.name == mock_callable.__name__
    assert context.qualified_name == mock_callable.__qualname__
    assert context.module == mock_callable.__module__


@patch('inspect.signature', autospec=True)
@patch('pyloadover.functions.context.get_underlying_callable', autospec=True)
def test_function_context_properties_underlying_callable_exists(mock_get_underlying_callable: MagicMock,
                                                                mock_signature: MagicMock, mock_callable):
    mock_get_underlying_callable.return_value = MagicMock()

    context = FunctionContext(mock_callable)

    mock_get_underlying_callable.assert_called_once_with(mock_callable)
    mock_signature.assert_called_once_with(mock_get_underlying_callable.return_value)
    assert context.underlying_callable == mock_get_underlying_callable.return_value
    assert context.signature == mock_signature.return_value


@patch('inspect.signature', autospec=True)
@patch('pyloadover.functions.context.get_underlying_callable', autospec=True)
def test_function_context_properties_underlying_callable_not_exists(mock_get_underlying_callable: MagicMock,
                                                                    mock_signature: MagicMock, mock_callable):
    mock_get_underlying_callable.return_value = None

    context = FunctionContext(mock_callable)

    mock_get_underlying_callable.assert_called_once_with(mock_callable)
    mock_signature.assert_called_once_with(mock_callable)
    assert context.underlying_callable is None
    assert context.signature == mock_signature.return_value
