from unittest.mock import patch, MagicMock

from pyloadover.functions.context import FunctionContext


@patch('inspect.signature', autospec=True)
def test_function_context_properties(mock_signature: MagicMock, mock_callable):
    context = FunctionContext(mock_callable)

    mock_signature.assert_called_once_with(mock_callable)
    assert context.callable == mock_callable
    assert context.name == mock_callable.__name__
    assert context.qualified_name == mock_callable.__qualname__
    assert context.module == mock_callable.__module__
    assert context.signature == mock_signature.return_value
