import functools
from typing import Optional, List, Callable
from pyloadover.functions import Function, FunctionContext, FunctionIdGenerator
from pyloadover.groups import GroupFunctionValidator
from pyloadover.manager import manager
from pyloadover.config import set_if_value_exists


def basic_config(propagate: bool = False, *,
                 function_id_generator: Optional[FunctionIdGenerator] = None,
                 group_validators: Optional[List[GroupFunctionValidator]] = None):
    set_if_value_exists("function_id_generator", function_id_generator)
    set_if_value_exists("group_validators", group_validators)

    if propagate:
        manager.reload_from_config()


def pyoverload(group: str = None):
    def decorator(f: Callable):
        function = Function(FunctionContext(f))
        group_id = group if group is not None else function.id
        manager.register_function_to_group(group_id, function)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            retrieved_function = manager.retrieve_function_from_group(group_id, *args, **kwargs)
            return retrieved_function(*args, **kwargs)

        return wrapper

    return decorator


loadover = pyoverload()
