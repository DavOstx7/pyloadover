import pytest
from unittest.mock import patch, call, MagicMock

from pyloadover.groups.model import Group, GroupContext, CONFIG
from pyloadover.functions.model import Function, FunctionContext
from pyloadover.exceptions import NoMatchFoundError, MultipleMatchesFoundError


@patch.dict('pyloadover.groups.model.CONFIG', {}, clear=True)
def test_group_reload_from_config(mock_group_context, mock_group_validators, mock_functions):
    CONFIG["group_function_validators"] = mock_group_validators
    mock_group_context.functions = mock_functions
    group = Group(mock_group_context)

    group.reload_from_config()

    assert group.validators == CONFIG["group_function_validators"]
    for mock_function in mock_functions:
        mock_function.reload_from_config.assert_called_once_with()


def test_group_clear(random_int, mock_group_context, mock_group_validators, mock_functions):
    mock_group_context.functions = mock_functions
    group = Group(mock_group_context, mock_group_validators)

    group.clear()

    assert not mock_functions
    assert not mock_group_validators


@patch.object(Group, 'validate_function')
def test_group_register_function(mock_validate_function: MagicMock, mock_group_context, mock_function):
    mock_group_context.functions = []
    group = Group(mock_group_context)

    group.register_function(mock_function)

    mock_validate_function.assert_called_once_with(mock_function)
    assert mock_group_context.functions == [mock_function]


@patch.object(Group, 'validate_function')
def test_group_validate(mock_validate_function: MagicMock, mock_group_context, mock_functions):
    mock_group_context.functions = mock_functions
    expected_calls = len(mock_functions)
    group = Group(mock_group_context)

    group.validate()

    assert mock_validate_function.call_count == expected_calls
    mock_validate_function.assert_has_calls([call(mock_function) for mock_function in mock_functions])


def test_group_validate_function(mock_group_context, mock_group_validators, mock_function):
    group = Group(mock_group_context, mock_group_validators)

    group.validate_function(mock_function)

    for mock_validator in mock_group_validators:
        mock_validator.validate.assert_called_once_with(mock_group_context, mock_function)


def test_group_retrieve_matching_functions():
    group = Group(GroupContext("_foo"))

    def _foo():
        pass

    function1 = Function(FunctionContext(_foo))
    group.register_function(function1)

    def _foo(a: bool):
        pass

    function2 = Function(FunctionContext(_foo))
    group.register_function(function2)

    def _foo(a: int, b: str, c: bool = True):
        pass

    function3 = Function(FunctionContext(_foo))
    group.register_function(function3)

    assert group.retrieve_matching_functions() == [function1]
    assert group.retrieve_matching_functions(True) == [function2]
    assert group.retrieve_matching_functions(1, "2", True) == [function3]
    assert group.retrieve_matching_functions(False, False, False) == []


def test_group_retrieve_single_matching_function():
    group = Group(GroupContext("_foo"))

    def _foo():
        pass

    function1 = Function(FunctionContext(_foo))
    group.register_function(function1)

    def _foo(a: bool):
        pass

    function2 = Function(FunctionContext(_foo))
    group.register_function(function2)

    def _foo(a: int, b: str, c: bool = True):
        pass

    function3 = Function(FunctionContext(_foo))
    group.register_function(function3)

    assert group.retrieve_single_matching_function() == function1
    assert group.retrieve_single_matching_function(True) == function2
    assert group.retrieve_single_matching_function(1, "2", True) == function3


def test_group_retrieve_single_matching_function_no_matches():
    group = Group(GroupContext("_foo"))

    def _foo(a: int, b: str, c: bool = True):
        pass

    function = Function(FunctionContext(_foo))
    group.register_function(function)

    with pytest.raises(NoMatchFoundError):
        group.retrieve_single_matching_function()


def test_group_retrieve_single_matching_function_multiple_matches():
    group = Group(GroupContext("_foo"))

    def _foo():
        pass

    function = Function(FunctionContext(_foo))
    group.register_function(function)

    def _foo(*a, **b):
        pass

    function = Function(FunctionContext(_foo))
    group.register_function(function)

    with pytest.raises(MultipleMatchesFoundError):
        group.retrieve_single_matching_function()


@patch.object(Group, 'retrieve_single_matching_function')
def test_group_call_matching_function(mock_retrieve_single_matching_function: MagicMock, mock_group_context, args,
                                      kwargs):
    group = Group(mock_group_context)

    return_value = group.call_matching_function(*args, **kwargs)

    mock_retrieve_single_matching_function.assert_called_once_with(*args, **kwargs)
    mock_retrieve_single_matching_function.return_value.assert_called_once_with(*args, **kwargs)
    assert return_value == mock_retrieve_single_matching_function.return_value.return_value


@patch('pyloadover.groups.model.Function', autospec=True)
@patch.object(Group, 'wraps')
def test_group_as_decorator(mock_wraps: MagicMock, MockFunction: MagicMock, mock_group_context):
    group = Group(mock_group_context)

    def _foo():
        pass

    return_value = group(_foo)

    MockFunction.from_callable.assert_called_once_with(_foo)
    mock_wraps.assert_called_once_with(MockFunction.from_callable.return_value)
    assert return_value == mock_wraps.return_value
