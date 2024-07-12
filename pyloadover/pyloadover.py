import functools
from typing import Callable
from pyloadover.manager import Manager, Function

_manager = Manager()


def pyloadover(group: str = None):
    def decorator(f: Callable):
        function = Function(f)
        group_id = group if group is not None else function.id
        _manager.register_to_group(group_id, function)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            retrieved_function = _manager.retrieve_from_existing_group(group_id, *args, **kwargs)
            return retrieved_function(*args, **kwargs)

        return wrapper

    return decorator


loadover = pyloadover()
