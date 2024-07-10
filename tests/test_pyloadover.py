from unittest.mock import patch, MagicMock

from pyloadover.pyloadover import loadover


@patch('pyloadover.pyloadover.Function', autospec=True)
@patch('pyloadover.pyloadover._manager', autospec=True)
def test_loadover_flow(mock_manager: MagicMock, MockFunction: MagicMock, args, kwargs, bar):

    new_bar = loadover(bar)

    MockFunction.assert_called_once_with(bar)
    mock_manager.add.assert_called_once_with(MockFunction.return_value)

    return_value = new_bar(*args, **kwargs)

    mock_manager.find.assert_called_once_with(MockFunction.return_value.namespace, *args, **kwargs)
    mock_function = mock_manager.find.return_value
    mock_function.assert_called_once_with(*args, **kwargs)
    assert mock_function.return_value == return_value


def test_loadover_on_func(reset_manager):
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


def test_loadoer_on_method(reset_manager):
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


def test_loadover_on_static_method(reset_manager):
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


def test_loadover_on_class_method(reset_manager):
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
