from typing import Optional, List, Callable, Any
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


def pyoverload(group_id: str = None):
    def decorator(_object: Callable[[...], Any]):
        function = Function(FunctionContext(_object))
        group = manager.get_group(group_id if group_id is not None else function.id)

        return group(_object)

    return decorator


loadover = pyoverload()
