import pytest

from pyloadover.group import Group, Function
from pyloadover.exceptions import (
    MismatchedIdError, DuplicatedSignatureError, NoMatchFoundError, MultipleMatchesFoundError
)


def test_allow_mismatched_names(foo, use_simple_function_id):
    group = Group("bar", allow_mismatched_ids=True)

    group.register(Function(foo))


def test_not_allow_mismatched_names(foo, use_simple_function_id):
    group = Group("bar", allow_mismatched_ids=False)

    with pytest.raises(MismatchedIdError):
        group.register(Function(foo))


def test_allow_identical_signatures(foo, use_simple_function_id):
    group = Group("foo", allow_duplicated_signatures=True)

    group.register(Function(foo))
    group.register(Function(foo))


def test_not_allow_identical_signatures(foo, use_simple_function_id):
    group = Group("foo", allow_duplicated_signatures=False)

    group.register(Function(foo))
    with pytest.raises(DuplicatedSignatureError):
        group.register(Function(foo))


def test_find_by_arguments(use_simple_function_id):
    registry = Group("foo")

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


def test_find_one_by_arguments(use_simple_function_id):
    registry = Group("foo")

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
    registry = Group("foo")
    registry.register(Function(foo))

    with pytest.raises(NoMatchFoundError):
        registry.find_one_by_arguments()


def test_find_one_by_arguments_multiple_matches():
    registry = Group("foo")

    def foo():
        pass

    registry.register(Function(foo))

    def foo(*a, **b):
        pass

    registry.register(Function(foo))

    with pytest.raises(MultipleMatchesFoundError):
        registry.find_one_by_arguments()
