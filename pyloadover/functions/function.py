import inspect
from typing import Optional
from pyloadover.config import CONFIG, ConfigReloadable
from pyloadover.function.generators import FunctionIdGenerator, FunctionContext
from pyloadover.utils import is_instance


class Function(ConfigReloadable):
    def __init__(self, context: FunctionContext, id_generator: Optional[FunctionIdGenerator] = None):
        self.context = context
        self.id_generator = CONFIG["function_id_generator"] if id_generator is None else id_generator

    @property
    def id(self) -> str:
        return self.id_generator.generate_id(self.context)

    @property
    def name(self) -> str:
        return self.context.name

    @property
    def signature(self) -> inspect.Signature:
        return self.context.signature

    def reload_from_config(self):
        self.id_generator = CONFIG["function_id_generator"]

    def do_arguments_match(self, *args, **kwargs) -> bool:
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
        return self.context.object(*args, **kwargs)