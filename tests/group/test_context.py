from unittest.mock import MagicMock

import inspect
from pyloadover.groups.context import GroupContext
from pyloadover.functions.function import Function


def test_context_properties(random_string):
    context = GroupContext(random_string)

    assert context.id == random_string
    assert context.functions == []


def test_context_signature_exists(random_int, random_string):
    mock_functions = [MagicMock(spec_set=Function) for _ in range(random_int)]
    mock_signature = MagicMock(spec_set=inspect.Signature)
    mock_functions[-1].signature = mock_signature

    context = GroupContext(random_string, mock_functions)

    assert context.is_signature_exists(mock_signature)


def test_context_signature_not_exists(random_int, random_string):
    mock_functions = [MagicMock(spec_set=Function) for _ in range(random_int)]
    mock_signature = MagicMock(spec_set=inspect.Signature)

    context = GroupContext(random_string, mock_functions)

    assert not context.is_signature_exists(mock_signature)
