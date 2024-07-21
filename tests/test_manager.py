from unittest.mock import patch, MagicMock

from pyloadover.manager import Manager


def test_reload_from_config(mock_id_to_group):
    manager = Manager()
    manager._id_to_group = mock_id_to_group

    manager.reload_from_config()

    for mock_group in mock_id_to_group.values():
        mock_group.reload_from_config.assert_called_once_with()


def test_get_group_when_group_exists(mock_group, random_string):
    manager = Manager()
    manager._id_to_group[random_string] = mock_group

    return_value = manager.get_group(random_string)

    assert return_value == mock_group


@patch('pyloadover.manager.Group')
def test_get_group_when_group_not_exists(MockGroup: MagicMock, random_string):
    manager = Manager()

    return_value = manager.get_group(random_string)

    MockGroup.from_id.assert_called_once_with(random_string)
    assert manager._id_to_group[random_string] == MockGroup.from_id.return_value
    assert return_value == MockGroup.from_id.return_value
