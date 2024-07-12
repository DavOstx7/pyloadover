import pytest
from unittest.mock import patch, MagicMock

from pyloadover.manager import Manager, Group, Function
from pyloadover.exceptions import GroupNotFoundError


@patch('pyloadover.manager.Group', autospec=True)
def test_get_new_group(MockGroup: MagicMock, random_string):
    manager = Manager()

    return_value = manager.get_group(random_string)

    MockGroup.assert_called_once_with(random_string)
    assert return_value == MockGroup.return_value


@patch('pyloadover.manager.Group', autospec=True)
def test_get_existing_group(MockGroup: MagicMock, random_string):
    manager = Manager()
    mock_group = MagicMock(spec_set=Group)
    manager._id_to_group[random_string] = mock_group

    return_value = manager.get_group(random_string)

    MockGroup.assert_not_called()
    assert return_value == mock_group


@patch.object(Manager, 'get_group')
def test_register_to_group(mock_get_group: MagicMock, random_string):
    manager = Manager()
    mock_function = MagicMock(spec_set=Function)

    manager.register_to_group(random_string, mock_function)

    mock_get_group.assert_called_once_with(random_string)
    mock_group = mock_get_group.return_value
    mock_group.register.assert_called_once_with(mock_function)


@patch.object(Manager, 'get_group')
def test_retrieve_from_existing_group(mock_get_group, random_string, args, kwargs):
    manager = Manager()
    manager._id_to_group[random_string] = MagicMock(spec_set=Group)

    return_value = manager.retrieve_from_existing_group(random_string, *args, **kwargs)

    mock_get_group.assert_called_once_with(random_string)
    mock_group = mock_get_group.return_value
    mock_group.find_one_by_arguments.assert_called_once_with(*args, **kwargs)
    assert return_value == mock_group.find_one_by_arguments.return_value


def test_retrieve_from_non_existing_group(random_string):
    manager = Manager()

    with pytest.raises(GroupNotFoundError):
        manager.retrieve_from_existing_group(random_string)
