from typing import Optional, Any

config = {
    "use_fully_qualified_function_id": True
}


def _set_key_if_value_exists(key: str, value: Optional[Any]):
    if value is None:
        return
    config[key] = value


def basic_config(use_fully_qualified_function_id: bool = None):
    _set_key_if_value_exists("use_fully_qualified_function_id", use_fully_qualified_function_id)
