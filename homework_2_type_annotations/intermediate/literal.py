"""
TODO:

foo only accepts literal 'left' and 'right' as its argument.
"""

from typing import Literal


def foo[Literals: Literal["left", "right"]](direction: Literals): ...
