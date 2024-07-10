import inspect
from typing import Callable


class Function:
    def __init__(self, function: Callable):
        self._obj = function
        self._sig = inspect.signature(function)

    @property
    def name(self) -> str:
        return self._obj.__name__

    @property
    def signature(self) -> inspect.Signature:
        return self._sig

    def do_arguments_match_signature(self, *args, **kwargs) -> bool:
        try:
            bound_args = self._sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            for name, value in bound_args.arguments.items():
                param = self._sig.parameters[name]

                if param.annotation != inspect.Parameter.empty:
                    if not isinstance(value, param.annotation):
                        return False

            return True
        except (TypeError, ValueError):
            return False

    def __call__(self, *args, **kwargs):
        return self._obj(*args, **kwargs)
