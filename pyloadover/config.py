from abc import ABC, abstractmethod
from typing import Optional, Any

# TODO: better config management (via a class for the config or consts/enums for the keys)
CONFIG = {
    "function_id_generator": None,
    "group_function_validators": None
}


def update_config_if_value_exists(key: str, value: Optional[Any]):
    if value is None:
        return

    CONFIG[key] = value


class ConfigReloadable(ABC):
    @abstractmethod
    def reload_from_config(self):
        raise NotImplementedError
