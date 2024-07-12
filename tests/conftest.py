import pytest

import random
import string
from typing import Callable
from pyloadover.pyloadover import _manager
from pyloadover.config import basic_config


@pytest.fixture
def use_simple_function_id():
    basic_config(use_fully_qualified_function_id=False)


@pytest.fixture
def foo() -> Callable:
    def foo(a: int, b: str, c: bool = True):
        return a, b, c

    return foo


@pytest.fixture
def random_string() -> tuple:
    return ''.join(random.choices(string.printable, k=random.randint(1, 5)))


@pytest.fixture
def args() -> tuple:
    return tuple(random.choices(list(string.digits) + list(range(0, 10)) + [True, False], k=random.randint(1, 3)))


@pytest.fixture
def kwargs(args) -> dict:
    names = tuple(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=len(args)))
    return {name: arg for name, arg in zip(names, args)}


@pytest.fixture
def clear_manager():
    _manager.clear()
