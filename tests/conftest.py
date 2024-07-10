import pytest

import random
import string
import pyloadover.pyloadover
from typing import Callable
from pyloadover.utils import get_namespace


@pytest.fixture
def foo() -> Callable:
    def foo(a: int, b: str, c: bool = True):
        return a, b, c

    return foo


@pytest.fixture
def foo_namespace(foo) -> str:
    return get_namespace(foo)


@pytest.fixture
def bar() -> Callable:
    def bar(*args, **kwargs):
        return args, kwargs

    return bar


@pytest.fixture
def bar_namespace(bar) -> Callable:
    return get_namespace(bar)


@pytest.fixture
def args() -> tuple:
    return tuple(random.choices(list(string.digits) + list(range(0, 10)) + [True, False], k=random.randint(1, 3)))


@pytest.fixture
def kwargs(args) -> dict:
    names = tuple(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=len(args)))
    return {name: arg for name, arg in zip(names, args)}


@pytest.fixture
def reset_manager():
    pyloadover.pyloadover._manager.reset()
