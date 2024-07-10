import pytest

from pyloadover.registry import FunctionRegistry, Function
from pyloadover.exceptions import (
    NamespaceMismatchError, SignatureExistsError, NoMatchingSignatureError, MultipleMatchingSignaturesError
)
from pyloadover.utils import get_namespace


def _foo(a: int, b: str, c: bool = True):
    pass


_foo_namespace = get_namespace(_foo)


def test_register():
    registry = FunctionRegistry(_foo_namespace)

    registry.register(Function(_foo))


def test_register_name_mismatch():
    registry = FunctionRegistry("bar")

    with pytest.raises(NamespaceMismatchError):
        registry.register(Function(_foo))


def test_register_signature_already_exists():
    registry = FunctionRegistry(_foo_namespace)
    registry.register(Function(_foo))

    with pytest.raises(SignatureExistsError):
        registry.register(Function(_foo))


def test_find_by_arguments():
    registry = FunctionRegistry(_foo_namespace)

    def _foo():
        pass

    function1 = Function(_foo)
    registry.register(function1)

    def _foo(a: bool):
        pass

    function2 = Function(_foo)
    registry.register(function2)

    def _foo(a: int, b: str, c: bool = True):
        pass

    function3 = Function(_foo)
    registry.register(function3)

    assert registry.find_by_arguments() == [function1]
    assert registry.find_by_arguments(True) == [function2]
    assert registry.find_by_arguments(1, "2", True) == [function3]
    assert registry.find_by_arguments(False, False, False) == []


def test_find_one_by_arguments():
    registry = FunctionRegistry(_foo_namespace)

    def _foo():
        pass

    function1 = Function(_foo)
    registry.register(function1)

    def _foo(a: bool):
        pass

    function2 = Function(_foo)
    registry.register(function2)

    def _foo(a: int, b: str, c: bool = True):
        pass

    function3 = Function(_foo)
    registry.register(function3)

    assert registry.find_one_by_arguments() == function1
    assert registry.find_one_by_arguments(True) == function2
    assert registry.find_one_by_arguments(1, "2", True) == function3


def test_find_one_by_arguments_no_matches():
    registry = FunctionRegistry(_foo_namespace)
    registry.register(Function(_foo))

    with pytest.raises(NoMatchingSignatureError):
        registry.find_one_by_arguments()


def test_find_one_by_arguments_multiple_matches():
    registry = FunctionRegistry(_foo_namespace)

    def _foo():
        pass

    registry.register(Function(_foo))

    def _foo(*a, **b):
        pass

    registry.register(Function(_foo))

    with pytest.raises(MultipleMatchingSignaturesError):
        registry.find_one_by_arguments()
