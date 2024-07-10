from dataclasses import dataclass
from typing import Dict
from pyloadover.registry import FunctionRegistry, Function
from pyloadover.exceptions import NamespaceNotFoundError


@dataclass
class AddOptions:
    namespace: str
    should_namespace_match: bool


class FunctionManager:
    def __init__(self):
        self._registry_by_namespace: Dict[str, FunctionRegistry] = {}

    def reset(self):
        self._registry_by_namespace = {}

    def add(self, function: Function, options: AddOptions):
        if options.namespace not in self._registry_by_namespace:
            registry = FunctionRegistry(options.namespace, options.should_namespace_match)
            self._registry_by_namespace[options.namespace] = registry

        self._registry_by_namespace[options.namespace].register(function)

    def find(self, namespace: str, *args, **kwargs) -> Function:
        if namespace not in self._registry_by_namespace:
            raise NamespaceNotFoundError(f"Namespace '{namespace}' does not exist")

        return self._registry_by_namespace[namespace].find_one_by_arguments(*args, **kwargs)
