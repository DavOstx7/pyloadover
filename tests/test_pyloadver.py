from unittest.mock import patch, call, MagicMock

import pyloadover
from pyloadover.pyloadover import configure, get_or_create_group, resolve_group_id, overloader, overload
from pyloadover.pyloadover import Function


@patch('pyloadover.pyloadover.update_config_if_value_exists')
def test_configure(
        mock_update_config_if_value_exists: MagicMock,
        mock_function_id_generator, mock_group_validators
):
    expected_call_count = 2

    configure(
        function_id_generator=mock_function_id_generator,
        group_function_validators=mock_group_validators
    )

    assert mock_update_config_if_value_exists.call_count == expected_call_count
    mock_update_config_if_value_exists.assert_has_calls(
        [
            call("function_id_generator", mock_function_id_generator),
            call("group_function_validators", mock_group_validators)
        ]
    )


@patch('pyloadover.pyloadover.manager', spec_set=True)
def test_configure_with_propagate(mock_manager: MagicMock):
    configure(propagate=True)

    mock_manager.reload_from_config.assert_called_once_with()


@patch('pyloadover.pyloadover.manager', spec_set=True)
def test_configure_without_propagate(mock_manager: MagicMock):
    configure(propagate=False)

    mock_manager.reload_from_config.assert_not_called()


@patch('pyloadover.pyloadover.manager', spec_set=True)
def test_get_or_create_group(mock_manager: MagicMock, random_string):
    return_value = get_or_create_group(random_string)

    mock_manager.get_or_create_group.assert_called_once_with(random_string)
    assert return_value == mock_manager.get_or_create_group.return_value


def test_resolve_group_id(foo_callable, random_string):
    function = Function.from_callable(foo_callable)

    assert random_string == resolve_group_id(random_string, function)


def test_resolve_group_id_without_group_id(foo_callable):
    function = Function.from_callable(foo_callable)

    assert function.id == resolve_group_id(None, function)


@patch('pyloadover.pyloadover.resolve_group_id', spec_set=True)
@patch('pyloadover.pyloadover.Function', spec_set=True)
@patch('pyloadover.pyloadover.manager', spec_set=True)
def test_overloader(
        mock_manager: MagicMock, MockFunction: MagicMock, mock_resolve_group_id: MagicMock,
        random_string, foo_callable, args, kwargs
):
    return_value = overloader(random_string)(foo_callable)

    MockFunction.from_callable.assert_called_once_with(foo_callable)
    mock_resolve_group_id.assert_called_once_with(random_string, MockFunction.from_callable.return_value)
    mock_manager.get_or_create_group.assert_called_once_with(mock_resolve_group_id.return_value)
    mock_gotten_group = mock_manager.get_or_create_group.return_value
    mock_gotten_group.wraps.assert_called_once_with(MockFunction.from_callable.return_value)
    assert return_value == mock_gotten_group.wraps.return_value


def test_group_decorator_on_function(clear_manager, random_string):
    random_group = get_or_create_group(random_string)

    @random_group
    def foo(x: int):
        return x

    @random_group
    def bar(x: int, y: str):
        return x, y

    assert random_group.call_function_by_arguments(1) == 1
    assert random_group.call_function_by_arguments(1, "2") == (1, "2")


def test_overload_decorator_on_function(clear_manager):
    @overload
    def foo(x: int):
        return x

    @overload
    def foo(x: int, y: str):
        return x, y

    @overload
    def bar(x: int):
        return x

    assert foo(1) == 1
    assert foo(1, "2") == (1, "2")
    assert bar(3) == 3


def test_overload_decorator_on_method(clear_manager):
    class Foo:
        @overload
        def foo(self, x: int):
            return x

        @overload
        def foo(self, x: int, y: str):
            return x, y

        @overload
        def bar(self, x: int):
            return x

    instance = Foo()
    assert instance.foo(1) == 1
    assert instance.foo(1, "2") == (1, "2")
    assert instance.bar(3) == 3


def test_overload_decorator_on_static_method(clear_manager):
    class Foo:
        @overload
        @staticmethod
        def foo(x: int):
            return x

        @staticmethod
        @overload
        def foo(x: int, y: str):
            return x, y

        @staticmethod
        @overload
        def bar(x: int):
            return x

    assert Foo.foo(1) == 1
    assert Foo.foo(1, "2") == (1, "2")
    assert Foo.bar(3) == 3


def test_overload_decorator_on_class_method(clear_manager):
    class Foo:
        @overload
        @classmethod
        def foo(cls, x: int):
            return x

        @classmethod
        @overload
        def foo(cls, x: int, y: str):
            return x, y

        @classmethod
        @overload
        def bar(cls, x: int):
            return x

    assert Foo.foo(1) == 1
    assert Foo.foo(1, "2") == (1, "2")
    assert Foo.bar(3) == 3


def test_dynamic_overload_builder_usage(clear_manager):
    dynamic_overload_builder = pyloadover.my.custom.group

    assert dynamic_overload_builder.name == "my.custom.group"


def test_dynamic_overload_builder_usage_as_decorator(clear_manager):
    @pyloadover.my.custom.group
    def foo(x: int):
        return x

    assert "my.custom.group" in clear_manager.id_to_group
