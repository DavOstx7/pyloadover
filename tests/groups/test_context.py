from pyloadover.groups.context import GroupContext


def test_functions_attribute_assigned_to_param(mock_functions, random_string):
    context = GroupContext(random_string, mock_functions)

    assert context._functions == mock_functions


def test_functions_attribute_assigned_to_empty_list(random_string):
    context = GroupContext(random_string)

    assert context._functions == []


def test_is_signature_exists(mock_functions, mock_function_signature, random_string):
    mock_functions[-1].signature = mock_function_signature
    context = GroupContext(random_string, mock_functions)

    assert context.is_signature_exists(mock_function_signature)


def test_is_signature_not_exists(mock_functions, mock_function_signature, random_string):
    context = GroupContext(random_string, mock_functions)

    assert not context.is_signature_exists(mock_function_signature)
