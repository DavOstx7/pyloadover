from unittest.mock import patch

from pyloadover.config import CONFIG, set_if_value_exists


@patch.dict('pyloadover.config.CONFIG', {}, clear=True)
def test_config_set_value_if_exists():
    set_if_value_exists("key", "value")

    assert CONFIG["key"] == "value"


@patch.dict('pyloadover.config.CONFIG', {}, clear=True)
def test_config_not_set_value_if_not_exists():
    set_if_value_exists("key", None)

    assert "key" not in CONFIG
