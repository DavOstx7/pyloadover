import functools
from typing import Callable
from pyloadover.manager import FunctionManager, AddOptions, Function

_manager = FunctionManager()


def pyloadover(group: str = None):
    def decorator(f: Callable):
        function = Function(f)
        if group is None:
            options = AddOptions(namespace=function.namespace, should_namespace_match=True)
        else:
            options = AddOptions(namespace=group, should_namespace_match=False)

        _manager.add(function, options)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return _manager.find(options.namespace, *args, **kwargs)(*args, **kwargs)

        return wrapper

    return decorator


loadover = pyloadover()
