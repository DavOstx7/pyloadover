from typing import Callable
from .pyloadover import pyloadover, loadover
from .config import set_use_full_path_as_namespace


class _DynamicPyloadover:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, item):
        self.name = f"{self.name}.{item}"
        return self

    def __call__(self, f: Callable):
        return pyloadover(self.name)(f)


def __getattr__(group: str):
    return _DynamicPyloadover(group)
