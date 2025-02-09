import pytest
from unittest.mock import MagicMock

import random
import inspect
import string
from typing import List, Callable, Dict
from pyloadover.pyloadover import manager, configure
from pyloadover.functions import Function, FunctionContext, FunctionIdGenerator, NameIdGenerator
from pyloadover.groups import Group, GroupContext, GroupFunctionValidator
from pyloadover.manager import Manager

configure(function_id_generator=NameIdGenerator(), group_function_validators=[])


@pytest.fixture
def foo_callable() -> Callable:
    def foo():
        pass

    return foo


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
def mock_underlying_callable(random_string) -> MagicMock:
    mock = MagicMock()
    mock.__name__ = random_string[:1]
    mock.__qualname__ = random_string[:2]
    mock.__module__ = random_string[:3]

    return mock


@pytest.fixture
def mock_callable(mock_underlying_callable, random_string) -> MagicMock:
    mock = MagicMock()
    mock.__name__ = random_string[:1]
    mock.__qualname__ = random_string[:2]
    mock.__module__ = random_string[:3]

    return mock


@pytest.fixture
def mock_object() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_function_signature() -> MagicMock:
    return MagicMock(spec_set=inspect.Signature)


@pytest.fixture
def mock_function_id_generator() -> MagicMock:
    return MagicMock(spec_set=FunctionIdGenerator)


@pytest.fixture
def mock_function_context() -> MagicMock:
    return MagicMock(spec_set=FunctionContext)


@pytest.fixture
def mock_function() -> MagicMock:
    return MagicMock(spec_set=Function)


@pytest.fixture
def mock_functions(random_int) -> List[MagicMock]:
    return [MagicMock(spec_set=Function) for _ in range(random_int)]


@pytest.fixture
def mock_group_validators(random_int) -> List[MagicMock]:
    return [MagicMock(spec_set=GroupFunctionValidator) for _ in range(random_int)]


@pytest.fixture
def mock_group_context() -> MagicMock:
    return MagicMock(spec_set=GroupContext)


@pytest.fixture
def mock_group() -> MagicMock:
    return MagicMock(spec_set=Group)


@pytest.fixture
def mock_id_to_group(args) -> Dict[str, MagicMock]:
    return {arg: MagicMock(spec_set=Group) for arg in args}


@pytest.fixture
def clear_manager() -> Manager:
    manager.clear()
    return manager
