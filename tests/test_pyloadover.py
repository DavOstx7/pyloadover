from unittest.mock import patch, MagicMock

from pyloadover.pyloadover import pyoverload, loadover


@patch('pyloadover.pyloadover.FunctionContext', spec_set=True)
@patch('pyloadover.pyloadover.Function', spec_set=True)
@patch('pyloadover.pyloadover.manager', spec_set=True)
def test_pyoverload_with_group(mock_manager: MagicMock, MockFunction: MagicMock, MockFunctionContext: MagicMock,
                               random_string, args, kwargs):
    def _foo(*a, **b):
        return a, b

    new_foo = pyoverload(random_string)(_foo)
    MockFunctionContext.assert_called_once_with(_foo)
    MockFunction.assert_called_once_with(MockFunctionContext.return_value)
    mock_manager.register_to_group.assert_called_once_with(random_string, MockFunction.return_value)

    return_value = new_foo(*args, **kwargs)

    mock_manager.retrieve_from_group.assert_called_once_with(random_string, *args, **kwargs)
    mock_manager.retrieve_from_group.return_value.assert_called_once_with(*args, **kwargs)
    assert return_value == mock_manager.retrieve_from_group.return_value.return_value


@patch('pyloadover.pyloadover.FunctionContext', spec_set=True)
@patch('pyloadover.pyloadover.Function', spec_set=True)
@patch('pyloadover.pyloadover.manager', spec_set=True)
def test_pyoverload_without_group(mock_manager: MagicMock, MockFunction: MagicMock, MockFunctionContext: MagicMock,
                                  args, kwargs):
    def _foo(*a, **b):
        return a, b

    new_foo = pyoverload()(_foo)
    MockFunctionContext.assert_called_once_with(_foo)
    MockFunction.assert_called_once_with(MockFunctionContext.return_value)
    mock_manager.register_to_group.assert_called_once_with(MockFunction.return_value.id, MockFunction.return_value)

    return_value = new_foo(*args, **kwargs)

    mock_manager.retrieve_from_group.assert_called_once_with(MockFunction.return_value.id, *args, **kwargs)
    mock_manager.retrieve_from_group.return_value.assert_called_once_with(*args, **kwargs)
    assert return_value == mock_manager.retrieve_from_group.return_value.return_value


def test_loadover_on_function(clear_manager):
    @loadover
    def foo(x: int):
        return x

    @loadover
    def foo(x: int, y: str):
        return x, y

    @loadover
    def bar(x: int):
        return x

    assert foo(1) == 1
    assert foo(1, "2") == (1, "2")
    assert bar(3) == 3


def test_loadover_on_method(clear_manager):
    class Foo:
        @loadover
        def foo(self, x: int):
            return x

        @loadover
        def foo(self, x: int, y: str):
            return x, y

        @loadover
        def bar(self, x: int):
            return x

    instance = Foo()
    assert instance.foo(1) == 1
    assert instance.foo(1, "2") == (1, "2")
    assert instance.bar(3) == 3


def test_loadover_on_static_method(clear_manager):
    class Foo:
        @staticmethod
        @loadover
        def foo(x: int):
            return x

        @staticmethod
        @loadover
        def foo(x: int, y: str):
            return x, y

        @staticmethod
        @loadover
        def bar(x: int):
            return x

    assert Foo.foo(1) == 1
    assert Foo.foo(1, "2") == (1, "2")
    assert Foo.bar(3) == 3


def test_loadover_on_class_method(clear_manager):
    class Foo:
        @classmethod
        @loadover
        def foo(cls, x: int):
            return x

        @classmethod
        @loadover
        def foo(cls, x: int, y: str):
            return x, y

        @classmethod
        @loadover
        def bar(cls, x: int):
            return x

    assert Foo.foo(1) == 1
    assert Foo.foo(1, "2") == (1, "2")
    assert Foo.bar(3) == 3
