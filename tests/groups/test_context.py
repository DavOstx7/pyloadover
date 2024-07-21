from pyloadover.groups.context import GroupContext


def test_functions_assigned_to_provided_param(mock_functions, random_string):
    context = GroupContext(random_string, mock_functions)

    assert context._functions == mock_functions


def test_functions_assigned_to_empty_list_when_param_not_provided(random_string):
    context = GroupContext(random_string)

    assert context._functions == []


def test_is_signature_exists_returns_true(mock_functions, mock_function_signature, random_string):
    mock_functions[-1].signature = mock_function_signature
    context = GroupContext(random_string, mock_functions)

    assert context.is_signature_exists(mock_function_signature)


def test_is_signature_exists_returns_false(mock_functions, mock_function_signature, random_string):
    context = GroupContext(random_string, mock_functions)

    assert not context.is_signature_exists(mock_function_signature)
