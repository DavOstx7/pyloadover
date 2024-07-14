import pytest

import random
import string
from pyloadover.pyloadover import manager, basic_config
from pyloadover.functions import NameIdGenerator

basic_config(function_id_generator=NameIdGenerator(), group_validators=[])


@pytest.fixture
def random_int() -> int:
    return random.randint(1, 7)


@pytest.fixture
def random_string(random_int) -> tuple:
    return ''.join(random.choices(string.printable, k=random_int))


@pytest.fixture
def args(random_int) -> tuple:
    return tuple(random.choices(list(string.digits) + list(range(0, 10)) + [True, False], k=random_int))


@pytest.fixture
def kwargs(args) -> dict:
    names = tuple(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=len(args)))
    return {name: arg for name, arg in zip(names, args)}


@pytest.fixture
def clear_manager():
    manager.clear()
