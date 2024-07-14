import pytest

from pyloadover.group import Group
from pyloadover.function import Function
from pyloadover.exceptions import (
    IdMismatchError, SignatureDuplicationError, NoMatchFoundError, MultipleMatchesFoundError
)


def test_allow_mismatched_names(foo, use_name_as_function_id):
    group = Group("bar")

    group.register_function(Function(foo))


def test_not_allow_mismatched_names(foo, use_name_as_function_id):
    group = Group("bar")

    with pytest.raises(IdMismatchError):
        group.register_function(Function(foo))


def test_allow_identical_signatures(foo, use_name_as_function_id):
    group = Group("foo")

    group.register_function(Function(foo))
    group.register_function(Function(foo))


def test_not_allow_identical_signatures(foo, use_name_as_function_id):
    group = Group("foo")

    group.register_function(Function(foo))
    with pytest.raises(SignatureDuplicationError):
        group.register_function(Function(foo))


def test_find_by_arguments(use_name_as_function_id):
    registry = Group("foo")

    def foo():
        pass

    function1 = Function(foo)
    registry.register_function(function1)

    def foo(a: bool):
        pass

    function2 = Function(foo)
    registry.register_function(function2)

    def foo(a: int, b: str, c: bool = True):
        pass

    function3 = Function(foo)
    registry.register_function(function3)

    assert registry.find_functions_by_arguments() == [function1]
    assert registry.find_functions_by_arguments(True) == [function2]
    assert registry.find_functions_by_arguments(1, "2", True) == [function3]
    assert registry.find_functions_by_arguments(False, False, False) == []


def test_find_one_by_arguments(use_name_as_function_id):
    registry = Group("foo")

    def foo():
        pass

    function1 = Function(foo)
    registry.register_function(function1)

    def foo(a: bool):
        pass

    function2 = Function(foo)
    registry.register_function(function2)

    def foo(a: int, b: str, c: bool = True):
        pass

    function3 = Function(foo)
    registry.register_function(function3)

    assert registry.find_one_function_by_arguments() == function1
    assert registry.find_one_function_by_arguments(True) == function2
    assert registry.find_one_function_by_arguments(1, "2", True) == function3


def test_find_one_by_arguments_no_matches(foo):
    registry = Group("foo")
    registry.register_function(Function(foo))

    with pytest.raises(NoMatchFoundError):
        registry.find_one_function_by_arguments()


def test_find_one_by_arguments_multiple_matches():
    registry = Group("foo")

    def foo():
        pass

    registry.register_function(Function(foo))

    def foo(*a, **b):
        pass

    registry.register_function(Function(foo))

    with pytest.raises(MultipleMatchesFoundError):
        registry.find_one_function_by_arguments()
