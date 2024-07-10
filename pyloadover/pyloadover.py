import functools
from typing import Callable
from pyloadover.manager import FunctionManager, Function

_manager = FunctionManager()


def loadover(f: Callable):
    name = f.__name__
    _manager.add(Function(f))

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        function = _manager.find(name, *args, **kwargs)
        return function(*args, **kwargs)

    return wrapper
