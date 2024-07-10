from typing import Dict
from pyloadover.registry import FunctionRegistry, Function
from pyloadover.exceptions import NamespaceNotFoundError


class FunctionManager:
    def __init__(self):
        self._registry_by_namespace: Dict[str, FunctionRegistry] = {}

    def reset(self):
        self._registry_by_namespace = {}

    def add(self, function: Function):
        namespace = function.namespace
        if namespace not in self._registry_by_namespace:
            self._registry_by_namespace[namespace] = FunctionRegistry(namespace)

        self._registry_by_namespace[namespace].register(function)

    def find(self, namespace: str, *args, **kwargs) -> Function:
        if namespace not in self._registry_by_namespace:
            raise NamespaceNotFoundError(f"Namespace '{namespace}' does not exist")

        return self._registry_by_namespace[namespace].find_one_by_arguments(*args, **kwargs)
