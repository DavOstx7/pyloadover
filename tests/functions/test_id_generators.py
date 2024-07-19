from pyloadover.functions.id_generators import NameIdGenerator, FullyQualifiedNameIdGenerator


def test_name_id_generator(mock_function_context):
    return_value = NameIdGenerator().generate_id(mock_function_context)

    assert return_value == mock_function_context.name


def test_fully_qualified_name_id_generator(mock_function_context):
    return_value = FullyQualifiedNameIdGenerator().generate_id(mock_function_context)

    assert return_value == f"{mock_function_context.module}.{mock_function_context.qualified_name}"
