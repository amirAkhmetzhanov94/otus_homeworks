"""
TODO:

The function `add` accepts two arguments and returns a value,
they all have the same type.
"""

from typing import TypeVar

T = TypeVar("T")


def add[T](a: T, b: T) -> T:
    return a
