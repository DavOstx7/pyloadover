from unittest.mock import patch, call, MagicMock

from pyloadover.pyloadover import basic_config, get_group, resolve_group_id, pyoverload, overload
from pyloadover.pyloadover import Function


@patch('pyloadover.pyloadover.set_if_value_exists')
def test_basic_config(mock_set_if_value_exists: MagicMock, mock_function_id_generator, mock_group_validators):
    expected_call_count = 2

    basic_config(
        function_id_generator=mock_function_id_generator,
        group_function_validators=mock_group_validators
    )

    assert mock_set_if_value_exists.call_count == expected_call_count
    mock_set_if_value_exists.assert_has_calls(
        [
            call("function_id_generator", mock_function_id_generator),
            call("group_function_validators", mock_group_validators)
        ]
    )


@patch('pyloadover.pyloadover.manager', spec_set=True)
def test_basic_config_propagate(mock_manager: MagicMock):
    basic_config(propagate=True)
    mock_manager.reload_from_config.assert_called_once_with()


@patch('pyloadover.pyloadover.manager', spec_set=True)
def test_basic_config_not_propagate(mock_manager: MagicMock):
    basic_config(propagate=False)
    mock_manager.reload_from_config.assert_not_called()


@patch('pyloadover.pyloadover.manager', spec_set=True)
def test_get_group(mock_manager: MagicMock, random_string):
    return_value = get_group(random_string)

    mock_manager.get_group.assert_called_once_with(random_string)
    assert return_value == mock_manager.get_group.return_value


def test_resolve_group_id_returns_group_id_if_provided(foo_callable, random_string):
    group_id = random_string
    function = Function.from_callable(foo_callable)

    assert group_id == resolve_group_id(group_id, function)


def test_resolve_group_id_returns_function_id_if_group_id_not_provided(foo_callable):
    group_id = None
    function = Function.from_callable(foo_callable)

    assert function.id == resolve_group_id(group_id, function)


@patch('pyloadover.pyloadover.resolve_group_id', spec_set=True)
@patch('pyloadover.pyloadover.Function', spec_set=True)
@patch('pyloadover.pyloadover.manager', spec_set=True)
def test_pyoverload(mock_manager: MagicMock, MockFunction: MagicMock, mock_resolve_group_id: MagicMock,
                    random_string, foo_callable, args, kwargs):
    return_value = pyoverload(random_string)(foo_callable)

    MockFunction.from_callable.assert_called_once_with(foo_callable)
    mock_resolve_group_id.assert_called_once_with(random_string, MockFunction.from_callable.return_value)
    mock_manager.get_group.assert_called_once_with(mock_resolve_group_id.return_value)
    mock_manager.get_group.return_value.wraps.assert_called_once_with(MockFunction.from_callable.return_value)
    assert return_value == mock_manager.get_group.return_value.wraps.return_value


def test_group_decorator_on_function(clear_manager, random_string):
    random_group = get_group(random_string)

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
