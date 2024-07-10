from unittest.mock import patch, MagicMock

from pyloadover.pyloadover import loadover


@patch('pyloadover.pyloadover.Function', autospec=True)
@patch('pyloadover.pyloadover._manager', autospec=True)
def test_loadover_flow(mock_manager: MagicMock, MockFunction: MagicMock, args, kwargs):
    def bar(*a, **b):
        return a, b

    original_bar = bar
    decorated_bar = loadover(bar)

    MockFunction.assert_called_once_with(original_bar)
    mock_manager.add.assert_called_once_with(MockFunction.return_value)

    return_value = decorated_bar(*args, **kwargs)

    mock_manager.find.assert_called_once_with("bar", *args, **kwargs)
    mock_function = mock_manager.find.return_value
    mock_function.assert_called_once_with(*args, **kwargs)
    assert mock_function.return_value == return_value


def test_loadover_on_func(reset_manager):
    @loadover
    def foo(x: int):
        return "one param"

    @loadover
    def foo(x: int, y: str):
        return "two param"

    @loadover
    def bar(x: int):
        return "unique"

    assert foo(1) == "one param"
    assert foo(1, "2") == "two param"
    assert bar(1) == "unique"


def test_loadoer_on_method(reset_manager):
    class Foo:
        @loadover
        def foo(self, x: int):
            return "one param"

        @loadover
        def foo(self, x: int, y: str):
            return "two param"

        @loadover
        def bar(self, x: int):
            return "unique"

    instance = Foo()
    assert instance.foo(1) == "one param"
    assert instance.foo(1, "2") == "two param"
    assert instance.bar(1) == "unique"


def test_loadover_on_static_method(reset_manager):
    class Foo:
        @staticmethod
        @loadover
        def foo(x: int):
            return "one param"

        @staticmethod
        @loadover
        def foo(x: int, y: str):
            return "two param"

        @staticmethod
        @loadover
        def bar(x: int):
            return "unique"

    assert Foo.foo(1) == "one param"
    assert Foo.foo(1, "2") == "two param"
    assert Foo.bar(1) == "unique"


def test_loadover_on_class_method(reset_manager):
    class Foo:
        @classmethod
        @loadover
        def foo(cls, x: int):
            return "one param"

        @classmethod
        @loadover
        def foo(cls, x: int, y: str):
            return "two param"

        @classmethod
        @loadover
        def bar(cls, x: int):
            return "unique"

    assert Foo.foo(1) == "one param"
    assert Foo.foo(1, "2") == "two param"
    assert Foo.bar(1) == "unique"
