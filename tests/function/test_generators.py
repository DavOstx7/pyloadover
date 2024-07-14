from unittest.mock import MagicMock

from pyloadover.functions.generators import FunctionContext, NameIdGenerator, FullyQualifiedNameIdGenerator


def test_name_id_generator():
    mock_context = MagicMock(spec_set=FunctionContext)

    return_value = NameIdGenerator().generate_id(mock_context)

    assert return_value == mock_context.name


def test_fully_qualified_name_id_generator():
    mock_context = MagicMock(spec_set=FunctionContext)

    return_value = FullyQualifiedNameIdGenerator().generate_id(mock_context)

    assert return_value == f"{mock_context.module}.{mock_context.qualified_name}"
