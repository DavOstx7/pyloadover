import pytest
from unittest.mock import patch, call, MagicMock

from pyloadover.groups.group import Group, CONFIG
from pyloadover.functions.function import Function
from pyloadover.exceptions import NoMatchFoundError, MultipleMatchesFoundError


def test_validators_attribute(mock_group_context, mock_group_validators):
    group = Group(mock_group_context, mock_group_validators)

    assert group.validators == mock_group_validators


@patch.dict('pyloadover.groups.group.CONFIG', {}, clear=True)
def test_validators_attribute_default_value(mock_group_context, mock_group_validators):
    CONFIG["group_function_validators"] = mock_group_validators

    group = Group(mock_group_context)

    assert group.validators == CONFIG["group_function_validators"]


@patch.dict('pyloadover.groups.group.CONFIG', {}, clear=True)
def test_reload_from_config(mock_group_context, mock_group_validators, mock_functions):
    CONFIG["group_function_validators"] = mock_group_validators
    mock_group_context.functions = mock_functions
    group = Group(mock_group_context)

    group.reload_from_config()

    assert group.validators == CONFIG["group_function_validators"]
    for mock_function in mock_functions:
        mock_function.reload_from_config.assert_called_once_with()


def test_clear(random_int, mock_group_context, mock_group_validators, mock_functions):
    mock_group_context.functions = mock_functions
    group = Group(mock_group_context, mock_group_validators)

    group.clear()

    assert not mock_functions
    assert not mock_group_validators


@patch.object(Group, 'validate_function')
def test_register_function(mock_validate_function: MagicMock, mock_group_context, mock_function):
    mock_group_context.functions = []
    group = Group(mock_group_context)

    group.register_function(mock_function)

    mock_validate_function.assert_called_once_with(mock_function)
    assert mock_group_context.functions == [mock_function]


@patch.object(Group, 'validate_function')
def test_validate(mock_validate_function: MagicMock, mock_group_context, mock_functions):
    mock_group_context.functions = mock_functions
    group = Group(mock_group_context)
    expected_call_count = len(mock_functions)

    group.validate()

    assert mock_validate_function.call_count == expected_call_count
    mock_validate_function.assert_has_calls([call(mock_function) for mock_function in mock_functions])


def test_validate_function(mock_group_context, mock_group_validators, mock_function):
    group = Group(mock_group_context, mock_group_validators)

    group.validate_function(mock_function)

    for mock_validator in mock_group_validators:
        mock_validator.validate_function.assert_called_once_with(mock_group_context, mock_function)


def test_find_functions_by_arguments():
    group = Group.from_id("_foo")

    def _foo():
        pass

    function1 = Function.from_callable(_foo)
    group.register_function(function1)

    def _foo(a: bool):
        pass

    function2 = Function.from_callable(_foo)
    group.register_function(function2)

    def _foo(a: int, b: str, c: bool = True):
        pass

    function3 = Function.from_callable(_foo)
    group.register_function(function3)

    assert group.find_functions_by_arguments() == [function1]
    assert group.find_functions_by_arguments(True) == [function2]
    assert group.find_functions_by_arguments(1, "2", True) == [function3]
    assert group.find_functions_by_arguments(False, False, False) == []


def test_find_single_function_by_arguments():
    group = Group.from_id("_foo")

    def _foo():
        pass

    function1 = Function.from_callable(_foo)
    group.register_function(function1)

    def _foo(a: bool):
        pass

    function2 = Function.from_callable(_foo)
    group.register_function(function2)

    def _foo(a: int, b: str, c: bool = True):
        pass

    function3 = Function.from_callable(_foo)
    group.register_function(function3)

    assert group.find_single_function_by_arguments() == function1
    assert group.find_single_function_by_arguments(True) == function2
    assert group.find_single_function_by_arguments(1, "2", True) == function3


def test_find_single_function_by_arguments_raises_no_match():
    group = Group.from_id("_foo")

    def _foo(a: int, b: str, c: bool = True):
        pass

    function = Function.from_callable(_foo)
    group.register_function(function)

    with pytest.raises(NoMatchFoundError):
        group.find_single_function_by_arguments()


def test_find_single_function_by_arguments_raises_multiple_matches():
    group = Group.from_id("_foo")

    def _foo():
        pass

    function = Function.from_callable(_foo)
    group.register_function(function)

    def _foo(*a, **b):
        pass

    function = Function.from_callable(_foo)
    group.register_function(function)

    with pytest.raises(MultipleMatchesFoundError):
        group.find_single_function_by_arguments()


@patch.object(Group, 'find_single_function_by_arguments')
def test_call_function_by_arguments(
        mock_find_single_function_by_arguments: MagicMock,
        mock_group_context, args, kwargs
):
    group = Group(mock_group_context)

    return_value = group.call_function_by_arguments(*args, **kwargs)

    mock_find_single_function_by_arguments.assert_called_once_with(*args, **kwargs)
    mock_found_function = mock_find_single_function_by_arguments.return_value
    mock_found_function.assert_called_once_with(*args, **kwargs)
    assert return_value == mock_found_function.return_value


@patch.object(Group, 'call_function_by_arguments')
@patch.object(Group, 'register_function')
def test_wraps(
        mock_register_function: MagicMock, mock_call_function_by_arguments: MagicMock,
        mock_group_context, mock_function, args, kwargs
):
    group = Group(mock_group_context)

    wrapped_function = group.wraps(mock_function)

    mock_register_function.assert_called_once_with(mock_function)

    return_value = wrapped_function(*args, **kwargs)

    mock_call_function_by_arguments.assert_called_once_with(*args, **kwargs)
    assert return_value == mock_call_function_by_arguments.return_value


@patch('pyloadover.groups.group.Function', autospec=True)
@patch.object(Group, 'wraps')
def test_as_decorator(mock_wraps: MagicMock, MockFunction: MagicMock, mock_group_context):
    group = Group(mock_group_context)

    def _foo():
        pass

    return_value = group(_foo)

    MockFunction.from_callable.assert_called_once_with(_foo)
    mock_wraps.assert_called_once_with(MockFunction.from_callable.return_value)
    assert return_value == mock_wraps.return_value
