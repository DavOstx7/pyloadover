from pyloadover.pyloadover import pyloadover, loadover


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


def test_pyloadover_group(reset_manager):
    @pyloadover("group")
    def foo(x: int):
        return x

    @pyloadover("group")
    def bar(x: int, y: str):
        return x, y

    assert foo(1, "2") == (1, "2")
    assert bar(1) == 1
