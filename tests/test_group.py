import pytest

from pyloadover.group import Group, Function
from pyloadover.exceptions import (
    NameMismatchError, IdenticalSignatureError, NoMatchesFoundError, MultipleMatchesFoundError
)


def test_register(foo, foo_namespace):
    registry = Group(foo_namespace, True)

    registry.register(Function(foo))


def test_register_name_mismatch(foo, foo_namespace, bar_namespace):
    registry = Group(bar_namespace, True)

    with pytest.raises(NameMismatchError):
        registry.register(Function(foo))


def test_register_no_name_mismatch(foo, foo_namespace, bar_namespace):
    registry = Group(bar_namespace, False)

    registry.register(Function(foo))


def test_register_signature_already_exists(foo, foo_namespace):
    registry = Group(foo_namespace, True)
    registry.register(Function(foo))

    with pytest.raises(IdenticalSignatureError):
        registry.register(Function(foo))


def test_find_by_arguments():
    registry = Group("", False)

    def foo():
        pass

    function1 = Function(foo)
    registry.register(function1)

    def foo(a: bool):
        pass

    function2 = Function(foo)
    registry.register(function2)

    def foo(a: int, b: str, c: bool = True):
        pass

    function3 = Function(foo)
    registry.register(function3)

    assert registry.find_by_arguments() == [function1]
    assert registry.find_by_arguments(True) == [function2]
    assert registry.find_by_arguments(1, "2", True) == [function3]
    assert registry.find_by_arguments(False, False, False) == []


def test_find_one_by_arguments():
    registry = Group("", False)

    def foo():
        pass

    function1 = Function(foo)
    registry.register(function1)

    def foo(a: bool):
        pass

    function2 = Function(foo)
    registry.register(function2)

    def foo(a: int, b: str, c: bool = True):
        pass

    function3 = Function(foo)
    registry.register(function3)

    assert registry.find_one_by_arguments() == function1
    assert registry.find_one_by_arguments(True) == function2
    assert registry.find_one_by_arguments(1, "2", True) == function3


def test_find_one_by_arguments_no_matches(foo):
    registry = Group(foo, False)
    registry.register(Function(foo))

    with pytest.raises(NoMatchesFoundError):
        registry.find_one_by_arguments()


def test_find_one_by_arguments_multiple_matches():
    registry = Group("", False)

    def foo():
        pass

    registry.register(Function(foo))

    def foo(*a, **b):
        pass

    registry.register(Function(foo))

    with pytest.raises(MultipleMatchesFoundError):
        registry.find_one_by_arguments()
