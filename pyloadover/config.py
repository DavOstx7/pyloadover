from typing import Optional, Any

CONFIG = {
    "function_id_generator": None,
    "group_validators": None
}


def set_if_value_exists(key: str, value: Optional[Any]):
    if value is None:
        return
    CONFIG[key] = value
