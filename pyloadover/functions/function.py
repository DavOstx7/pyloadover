import inspect
from typing import Optional, Callable, Any
from pyloadover.config import CONFIG, ConfigReloadable
from pyloadover.functions.id_generators import FunctionIdGenerator, FunctionContext
from pyloadover.utils import is_instance


class Function(ConfigReloadable):
    def __init__(self, context: FunctionContext, id_generator: Optional[FunctionIdGenerator] = None):
        self._context = context
        self.id_generator = CONFIG["function_id_generator"] if id_generator is None else id_generator

    @classmethod
    def from_callable(cls, f: Callable[[...], Any], id_generator: Optional[FunctionIdGenerator] = None):
        return cls(FunctionContext(f), id_generator=id_generator)

    @property
    def id(self) -> str:
        return self.id_generator.generate_id(self._context)

    @property
    def context(self) -> FunctionContext:
        return self._context

    @property
    def object(self) -> Callable[[...], Any]:
        return self._context.object

    @property
    def name(self) -> str:
        return self._context.name

    @property
    def signature(self) -> inspect.Signature:
        return self._context.signature

    def reload_from_config(self):
        self.id_generator = CONFIG["function_id_generator"]

    def do_arguments_match_signature(self, *args, **kwargs) -> bool:
        try:
            bound_args = self.signature.bind(*args, **kwargs)
            bound_args.apply_defaults()

            for name, value in bound_args.arguments.items():
                param = self.signature.parameters[name]

                if param.annotation != inspect.Parameter.empty:
                    if not is_instance(value, param.annotation):
                        return False

            return True
        except (TypeError, ValueError):
            return False

    def __call__(self, *args, **kwargs):
        return self.object(*args, **kwargs)
