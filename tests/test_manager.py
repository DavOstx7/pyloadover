import pytest
from unittest.mock import patch, MagicMock

from pyloadover.manager import FunctionManager, FunctionRegistry, Function
from pyloadover.exceptions import NameNotFoundError


def _foo(a: int, b: str, c: bool = True):
    pass


@patch('pyloadover.manager.FunctionRegistry', autospec=True)
def test_add_on_new_function_name(MockFunctionRegistry: MagicMock):
    manager = FunctionManager()
    function = Function(_foo)

    manager.add(function)

    assert "_foo" in manager._registry_by_name
    MockFunctionRegistry.assert_called_once_with("_foo")
    assert manager._registry_by_name["_foo"] == MockFunctionRegistry.return_value
    manager._registry_by_name["_foo"].register.assert_called_once_with(function)


@patch('pyloadover.manager.FunctionRegistry', autospec=True)
def test_add_on_existing_function_name(MockFunctionRegistry: MagicMock):
    manager = FunctionManager()
    mock_registry = MagicMock(spec_set=FunctionRegistry)
    manager._registry_by_name["_foo"] = mock_registry
    function = Function(_foo)

    manager.add(function)

    MockFunctionRegistry.assert_not_called()
    mock_registry.register.assert_called_once_with(function)


def test_find_on_existing_function_name(args, kwargs):
    manager = FunctionManager()
    mock_registry = MagicMock(spec_set=FunctionRegistry)
    manager._registry_by_name["_foo"] = mock_registry

    return_value = manager.find("_foo", *args, **kwargs)

    mock_registry.find_one_by_arguments.assert_called_once_with(*args, **kwargs)
    assert return_value == mock_registry.find_one_by_arguments.return_value


def test_find_on_non_existing_function_name(args, kwargs):
    manager = FunctionManager()
    mock_registry = MagicMock(spec_set=FunctionRegistry)
    manager._registry_by_name["_foo"] = mock_registry

    with pytest.raises(NameNotFoundError):
        manager.find("bar", *args, **kwargs)
