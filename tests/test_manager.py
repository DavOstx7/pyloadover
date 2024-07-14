import pytest
from unittest.mock import patch, MagicMock

from pyloadover.manager import Manager, Group, Function
from pyloadover.exceptions import GroupNotFoundError


def test_manager_reload_from_config(args):
    mock_id_to_group = {str(arg): MagicMock(spec_set=Group) for arg in args}

    manager = Manager()
    manager._id_to_group = mock_id_to_group
    manager.reload_from_config()

    for mock_group in mock_id_to_group.values():
        mock_group.reload_from_config.assert_called_once_with()


def test_get_existing_group(random_string):
    manager = Manager()
    mock_group = MagicMock(spec_set=Group)
    manager._id_to_group[random_string] = mock_group

    return_value = manager.get_group(random_string)

    assert return_value == mock_group


@patch('pyloadover.manager.GroupContext')
@patch('pyloadover.manager.Group')
def test_get_non_existing_group(MockGroup: MagicMock, MockGroupContext: MagicMock, random_string):
    manager = Manager()

    return_value = manager.get_group(random_string)

    MockGroupContext.assert_called_once_with(random_string)
    MockGroup.assert_called_once_with(MockGroupContext.return_value)
    assert manager._id_to_group[random_string] == MockGroup.return_value
    assert return_value == MockGroup.return_value


@patch.object(Manager, 'get_group')
def test_register_function_to_group(mock_get_group: MagicMock, random_string):
    manager = Manager()
    mock_function = MagicMock(spec_set=Function)

    manager.register_function_to_group(random_string, mock_function)

    mock_get_group.assert_called_once_with(random_string)
    mock_group = mock_get_group.return_value
    mock_group.register_function.assert_called_once_with(mock_function)


def test_retrieve_function_from_existing_group(random_string, args, kwargs):
    manager = Manager()
    mock_group = MagicMock(spec_set=Group)
    manager._id_to_group[random_string] = mock_group

    return_value = manager.retrieve_function_from_group(random_string, *args, **kwargs)

    mock_group.find_one_function_by_arguments.assert_called_once_with(*args, **kwargs)
    assert return_value == mock_group.find_one_function_by_arguments.return_value


def test_retrieve_function_from_non_existing_group(random_string):
    manager = Manager()

    with pytest.raises(GroupNotFoundError):
        manager.retrieve_function_from_group(random_string)
