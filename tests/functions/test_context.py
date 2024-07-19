from unittest.mock import patch, MagicMock

from pyloadover.functions.context import FunctionContext


@patch('inspect.signature', autospec=True)
def test_function_context_properties(mock_signature: MagicMock, mock_object):
    mock_object.__name__ = "a"
    mock_object.__qualname__ = "b"
    mock_object.__module__ = "c"

    context = FunctionContext(mock_object)

    mock_signature.assert_called_once_with(mock_object)
    assert context.object == mock_object
    assert context.name == mock_object.__name__
    assert context.qualified_name == mock_object.__qualname__
    assert context.module == mock_object.__module__
    assert context.signature == mock_signature.return_value
