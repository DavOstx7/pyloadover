import pytest

import random
import string
import pyloadover.pyloadover


@pytest.fixture
def args() -> tuple:
    return tuple(random.choices(list(string.digits) + list(range(0, 10)) + [True, False], k=random.randint(1, 3)))


@pytest.fixture
def kwargs(args) -> dict:
    names = tuple(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=len(args)))
    return {name: arg for name, arg in zip(names, args)}


@pytest.fixture
def reset_manager():
    pyloadover.pyloadover._manager = pyloadover.pyloadover.FunctionManager()
