from unittest.mock import patch

from pyloadover.config import CONFIG, update_config_if_value_exists


@patch.dict('pyloadover.config.CONFIG', {}, clear=True)
def test_update_config_if_value_exists():
    update_config_if_value_exists("key", "value")

    assert CONFIG["key"] == "value"


@patch.dict('pyloadover.config.CONFIG', {}, clear=True)
def test_update_config_if_value_exists_not_update():
    update_config_if_value_exists("key", None)

    assert "key" not in CONFIG
