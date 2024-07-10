from typing import Dict
from pyloadover.registry import FunctionRegistry, Function
from pyloadover.exceptions import NameNotFoundError


class FunctionManager:
    def __init__(self):
        self._registry_by_name: Dict[str, FunctionRegistry] = {}

    def add(self, function: Function):
        name = function.name
        if name not in self._registry_by_name:
            self._registry_by_name[name] = FunctionRegistry(name)

        self._registry_by_name[name].register(function)

    def find(self, name: str, *args, **kwargs) -> Function:
        if name not in self._registry_by_name:
            raise NameNotFoundError(f"Name '{name}' has not been added yet")

        return self._registry_by_name[name].find_one_by_arguments(*args, **kwargs)
