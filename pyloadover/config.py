from abc import ABC, abstractmethod
from typing import Optional, Any

CONFIG = {
    "function_id_generator": None,
    "group_function_validators": None
}


def set_if_value_exists(key: str, value: Optional[Any]):
    if value is None:
        return
    CONFIG[key] = value


class ConfigReloadable(ABC):
    @abstractmethod
    def reload_from_config(self):
        pass
