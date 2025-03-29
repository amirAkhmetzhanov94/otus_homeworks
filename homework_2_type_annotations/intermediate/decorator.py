"""
TODO:

Define a decorator that wraps a function and returns a function with the same signature.
"""

from typing import Callable


def decorator(func: Callable):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return wrapper


@decorator
def foo(a: int, *, b: str) -> None: ...


@decorator
def bar(c: int, d: str) -> None: ...
