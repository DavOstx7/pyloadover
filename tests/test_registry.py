import pytest

from pyloadover.registry import FunctionRegistry, Function
from pyloadover.exceptions import (
    NamespaceMismatchError, SignatureExistsError, NoMatchingSignatureError, MultipleMatchingSignaturesError
)


def test_register(foo, foo_namespace):
    registry = FunctionRegistry(foo_namespace, True)

    registry.register(Function(foo))


def test_register_name_mismatch(foo, foo_namespace, bar_namespace):
    registry = FunctionRegistry(bar_namespace, True)

    with pytest.raises(NamespaceMismatchError):
        registry.register(Function(foo))


def test_register_no_name_mismatch(foo, foo_namespace, bar_namespace):
    registry = FunctionRegistry(bar_namespace, False)

    registry.register(Function(foo))


def test_register_signature_already_exists(foo, foo_namespace):
    registry = FunctionRegistry(foo_namespace, True)
    registry.register(Function(foo))

    with pytest.raises(SignatureExistsError):
        registry.register(Function(foo))


def test_find_by_arguments():
    registry = FunctionRegistry("", False)

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
    registry = FunctionRegistry("", False)

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
    registry = FunctionRegistry(foo, False)
    registry.register(Function(foo))

    with pytest.raises(NoMatchingSignatureError):
        registry.find_one_by_arguments()


def test_find_one_by_arguments_multiple_matches():
    registry = FunctionRegistry("", False)

    def foo():
        pass

    registry.register(Function(foo))

    def foo(*a, **b):
        pass

    registry.register(Function(foo))

    with pytest.raises(MultipleMatchingSignaturesError):
        registry.find_one_by_arguments()
