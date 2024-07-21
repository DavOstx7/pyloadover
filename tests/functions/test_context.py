from unittest.mock import patch, MagicMock

from pyloadover.functions.context import FunctionContext


@patch('pyloadover.functions.context.get_underlying_callable', autospec=True)
def test_underlying_callable_assignment(mock_get_underlying_callable: MagicMock, mock_callable):
    context = FunctionContext(mock_callable)

    mock_get_underlying_callable.assert_called_once_with(mock_callable)
    assert context._underlying_callable == mock_get_underlying_callable.return_value


@patch('inspect.signature', autospec=True)
@patch('pyloadover.functions.context.get_underlying_callable', autospec=True)
def test_signature_assignment_uses_underlying_callable_if_exists(mock_get_underlying_callable: MagicMock,
                                                                 mock_signature: MagicMock,
                                                                 mock_callable, mock_underlying_callable):
    mock_get_underlying_callable.return_value = mock_underlying_callable
    context = FunctionContext(mock_callable)

    mock_signature.assert_called_once_with(mock_underlying_callable)
    assert context._signature == mock_signature.return_value


@patch('inspect.signature', autospec=True)
@patch('pyloadover.functions.context.get_underlying_callable', autospec=True)
def test_signature_assignment_uses_callable_if_underlying_callable_not_exists(mock_get_underlying_callable: MagicMock,
                                                                              mock_signature: MagicMock,
                                                                              mock_callable):
    mock_get_underlying_callable.return_value = None

    context = FunctionContext(mock_callable)

    mock_signature.assert_called_once_with(mock_callable)
    assert context._signature == mock_signature.return_value
