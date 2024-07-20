import inspect
import typeguard
from typing import Optional, Callable, Any


def is_instance(value, annotation) -> bool:
    try:
        typeguard.check_type(value, annotation)
    except typeguard.TypeCheckError:
        return False
    else:
        return True


def is_wrapped(obj: object) -> bool:
    return hasattr(obj, '__wrapped__')


def is_bound(obj: object) -> bool:
    return hasattr(obj, '__func__')


def unbind(obj: object) -> object:
    return getattr(obj, '__func__')


def get_underlying_callable(f: Callable[[...], Any]) -> Optional[Callable[[...], Any]]:
    obj = f
    while is_wrapped(obj) or is_bound(obj):
        # Unwrapping before unbinding would always result in the shortest chain (even though it might skip some objects)
        if is_wrapped(obj):
            obj = inspect.unwrap(obj)
        if is_bound(obj):
            obj = unbind(obj)

    if obj == f:
        return None

    return obj
