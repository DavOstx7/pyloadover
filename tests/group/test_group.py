import pytest
from unittest.mock import patch, MagicMock, call

from pyloadover.groups.group import Group, GroupContext, GroupFunctionValidator
from pyloadover.functions.function import Function, FunctionContext
from pyloadover.exceptions import NoMatchFoundError, MultipleMatchesFoundError


@patch('pyloadover.groups.group.CONFIG', autospec=True)
def test_group_reload_from_config(mock_CONFIG, random_int):
    mock_context = MagicMock(spec_set=GroupContext)
    mock_functions = [MagicMock(spec_set=Function) for _ in range(random_int)]
    mock_context.functions = mock_functions

    group = Group(mock_context)
    group.reload_from_config()

    assert group.validators == mock_CONFIG["group_validators"]
    for mock_function in mock_functions:
        mock_function.reload_from_config.assert_called_once_with()


def test_group_clear(random_int, random_string):
    mock_context = MagicMock(spec_set=GroupContext)
    mock_functions = [MagicMock(spec_set=Function) for _ in range(random_int)]
    mock_context.functions = mock_functions
    mock_validators = [MagicMock(spec_set=GroupFunctionValidator) for _ in range(random_int)]

    group = Group(mock_context, mock_validators)
    group.clear()

    assert not mock_functions
    assert not mock_validators


@patch.object(Group, 'validate_function')
def test_group_register_function(mock_validate_function: MagicMock):
    mock_context = MagicMock(spec_set=GroupContext)
    mock_context.functions = []
    mock_function = MagicMock(spec_set=Function)

    group = Group(mock_context)
    group.register_function(mock_function)

    mock_validate_function.assert_called_once_with(mock_function)
    assert mock_context.functions == [mock_function]


@patch.object(Group, 'validate_function')
def test_group_validate_group(mock_validate_function: MagicMock, random_int):
    mock_context = MagicMock(spec_set=GroupContext)
    mock_functions = [MagicMock(spec_set=Function) for _ in range(random_int)]
    mock_context.functions = mock_functions

    group = Group(mock_context)
    group.validate()

    mock_validate_function.assert_has_calls([call(mock_function) for mock_function in mock_functions])


def test_group_validate_function(random_int):
    mock_context = MagicMock(spec_set=GroupContext)
    mock_validators = [MagicMock(spec_set=GroupFunctionValidator) for _ in range(random_int)]
    mock_function = MagicMock(spec_set=Function)

    group = Group(mock_context, mock_validators)
    group.validate_function(mock_function)

    for mock_validator in mock_validators:
        mock_validator.validate.assert_called_once_with(mock_context, mock_function)


def test_find_by_arguments():
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

    assert group.find_functions_by_arguments() == [function1]
    assert group.find_functions_by_arguments(True) == [function2]
    assert group.find_functions_by_arguments(1, "2", True) == [function3]
    assert group.find_functions_by_arguments(False, False, False) == []


def test_find_one_by_arguments():
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

    assert group.retrieve_function_by_arguments() == function1
    assert group.retrieve_function_by_arguments(True) == function2
    assert group.retrieve_function_by_arguments(1, "2", True) == function3


def test_find_one_by_arguments_no_matches():
    group = Group(GroupContext("_foo"))

    def _foo(a: int, b: str, c: bool = True):
        pass

    function = Function(FunctionContext(_foo))
    group.register_function(function)

    with pytest.raises(NoMatchFoundError):
        group.retrieve_function_by_arguments()


def test_find_one_by_arguments_multiple_matches():
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
        group.retrieve_function_by_arguments()
