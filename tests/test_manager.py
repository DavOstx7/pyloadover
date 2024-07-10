import pytest
from unittest.mock import patch, MagicMock

from pyloadover.manager import FunctionManager, FunctionRegistry, Function
from pyloadover.exceptions import NamespaceNotFoundError


@patch('pyloadover.manager.FunctionRegistry', autospec=True)
def test_add_function_on_new_namespace(MockFunctionRegistry: MagicMock, foo, foo_namespace):
    manager = FunctionManager()
    function = Function(foo)

    manager.add(function)

    assert foo_namespace in manager._registry_by_namespace
    MockFunctionRegistry.assert_called_once_with(foo_namespace)
    assert manager._registry_by_namespace[foo_namespace] == MockFunctionRegistry.return_value
    manager._registry_by_namespace[foo_namespace].register.assert_called_once_with(function)


@patch('pyloadover.manager.FunctionRegistry', autospec=True)
def test_add_function_on_existing_namespace(MockFunctionRegistry: MagicMock, foo, foo_namespace):
    manager = FunctionManager()
    mock_registry = MagicMock(spec_set=FunctionRegistry)
    manager._registry_by_namespace[foo_namespace] = mock_registry
    function = Function(foo)

    manager.add(function)

    MockFunctionRegistry.assert_not_called()
    mock_registry.register.assert_called_once_with(function)


def test_find_function_on_existing_namespace(args, kwargs, foo, foo_namespace):
    manager = FunctionManager()
    mock_registry = MagicMock(spec_set=FunctionRegistry)
    manager._registry_by_namespace[foo_namespace] = mock_registry

    return_value = manager.find(foo_namespace, *args, **kwargs)

    mock_registry.find_one_by_arguments.assert_called_once_with(*args, **kwargs)
    assert return_value == mock_registry.find_one_by_arguments.return_value


def test_find_function_on_non_existing_namespace(args, kwargs, foo_namespace, bar_namespace):
    manager = FunctionManager()
    mock_registry = MagicMock(spec_set=FunctionRegistry)
    manager._registry_by_namespace[foo_namespace] = mock_registry

    with pytest.raises(NamespaceNotFoundError):
        manager.find(bar_namespace, *args, **kwargs)
