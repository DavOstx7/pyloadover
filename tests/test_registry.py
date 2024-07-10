import pytest

from pyloadover.registry import FunctionRegistry, Function
from pyloadover.exceptions import (
    NameMismatchError, SignatureExistsError, NoMatchingSignatureError, MultipleMatchingSignaturesError
)


def _foo(a: int, b: str, c: bool = True):
    pass


def test_register():
    registry = FunctionRegistry("_foo")

    registry.register(Function(_foo))


def test_register_name_mismatch():
    registry = FunctionRegistry("bar")

    with pytest.raises(NameMismatchError):
        registry.register(Function(_foo))


def test_register_signature_already_exists():
    registry = FunctionRegistry("_foo")
    registry.register(Function(_foo))

    with pytest.raises(SignatureExistsError):
        registry.register(Function(_foo))


def test_find_by_arguments():
    registry = FunctionRegistry("bar")

    def bar():
        pass

    function1 = Function(bar)
    registry.register(function1)

    def bar(a: bool):
        pass

    function2 = Function(bar)
    registry.register(function2)

    def bar(a: int, b: str, c: bool = True):
        pass

    function3 = Function(bar)
    registry.register(function3)

    assert registry.find_by_arguments() == [function1]
    assert registry.find_by_arguments(True) == [function2]
    assert registry.find_by_arguments(1, "2", True) == [function3]
    assert registry.find_by_arguments(False, False, False) == []


def test_find_one_by_arguments():
    registry = FunctionRegistry("bar")

    def bar():
        pass

    function1 = Function(bar)
    registry.register(function1)

    def bar(a: bool):
        pass

    function2 = Function(bar)
    registry.register(function2)

    def bar(a: int, b: str, c: bool = True):
        pass

    function3 = Function(bar)
    registry.register(function3)

    assert registry.find_one_by_arguments() == function1
    assert registry.find_one_by_arguments(True) == function2
    assert registry.find_one_by_arguments(1, "2", True) == function3


def test_find_one_by_arguments_no_matches():
    registry = FunctionRegistry("_foo")
    registry.register(Function(_foo))

    with pytest.raises(NoMatchingSignatureError):
        registry.find_one_by_arguments()


def test_find_one_by_arguments_multiple_matches():
    registry = FunctionRegistry("bar")

    def bar():
        pass

    registry.register(Function(bar))

    def bar(*a, **b):
        pass

    registry.register(Function(bar))

    with pytest.raises(MultipleMatchingSignaturesError):
        registry.find_one_by_arguments()
