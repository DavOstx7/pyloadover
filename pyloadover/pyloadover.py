import functools
from typing import Callable
from pyloadover.manager import FunctionManager, Function

_manager = FunctionManager()


def loadover(f: Callable):
    function = Function(f)
    namespace = function.namespace
    _manager.add(function)

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return _manager.find(namespace, *args, **kwargs)(*args, **kwargs)

    return wrapper
