from typing import Optional, List, Callable, Any
from pyloadover.functions import Function, FunctionIdGenerator
from pyloadover.groups import Group, GroupFunctionValidator
from pyloadover.manager import manager
from pyloadover.config import set_if_value_exists


def basic_config(propagate: bool = False, *,
                 function_id_generator: Optional[FunctionIdGenerator] = None,
                 group_function_validators: Optional[List[GroupFunctionValidator]] = None):
    set_if_value_exists("function_id_generator", function_id_generator)
    set_if_value_exists("group_function_validators", group_function_validators)

    if propagate:
        manager.reload_from_config()


def get_group(group_id: str) -> Group:
    return manager.get_group(group_id)


def resolve_group_id(group_id: Optional[str], function: Function):
    return function.id if group_id is None else group_id


def pyoverload(group_id: str = None):
    def decorator(f: Callable[[...], Any]):
        function = Function.from_callable(f)
        group = manager.get_group(resolve_group_id(group_id, function))
        return group.wraps(function)

    return decorator


overload = pyoverload()
