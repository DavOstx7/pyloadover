from pyloadover.groups.context import GroupContext


def test_group_context_properties(random_string):
    context = GroupContext(random_string)

    assert context.id == random_string
    assert context.functions == []


def test_group_context_signature_exists(mock_functions,  mock_function_signature, random_string):
    mock_functions[-1].signature = mock_function_signature
    context = GroupContext(random_string, mock_functions)

    assert context.is_signature_exists(mock_function_signature)


def test_group_context_signature_not_exists(mock_functions,  mock_function_signature, random_string):
    context = GroupContext(random_string, mock_functions)

    assert not context.is_signature_exists(mock_function_signature)
