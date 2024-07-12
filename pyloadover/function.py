import inspect
from typing import Callable
from pyloadover.config import config
from pyloadover.utils import is_instance


class Function:
    def __init__(self, function: Callable):
        self._object = function
        self._signature = inspect.signature(function)

    @property
    def id(self) -> str:
        if config["use_fully_qualified_function_id"]:
            return f"{self.module}.{self.qualified_name}"
        else:
            return self.name

    @property
    def name(self) -> str:
        return self._object.__name__

    @property
    def qualified_name(self) -> str:
        return self._object.__qualname__

    @property
    def module(self) -> str:
        return self._object.__module__

    @property
    def signature(self) -> inspect.Signature:
        return self._signature

    def do_arguments_match(self, *args, **kwargs) -> bool:
        try:
            bound_args = self._signature.bind(*args, **kwargs)
            bound_args.apply_defaults()

            for name, value in bound_args.arguments.items():
                param = self._signature.parameters[name]

                if param.annotation != inspect.Parameter.empty:
                    if not is_instance(value, param.annotation):
                        return False

            return True
        except (TypeError, ValueError):
            return False

    def __call__(self, *args, **kwargs):
        return self._object(*args, **kwargs)
