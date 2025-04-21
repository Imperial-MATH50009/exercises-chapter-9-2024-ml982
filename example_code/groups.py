"""A module implementing the basic functionality of mathematical groups.

This version of the module uses inheritance.
"""

from numbers import Integral # noqa F401
import numpy as np # noqa F401


class Element:
    """An element of the specified group.

    Parameters
    ----------
    group: Group
        The group of which this is an element.
    value:
        The value of this entity. Valid values depend on the group.
    """

    def __init__(self, group, value):
        group._validate(value)
        self.group = group
        self.value = value

    def __mul__(self, other):
        """Use * to represent the group operation."""
        return Element(self.group,
                       self.group.operation(self.value,
                                            other.value))

    def __str__(self):
        """Return a string of the form value_group."""
        return f"{self.value}_{self.group}"

    def __repr__(self):
        """Return the canonical string representation of the element."""
        return f"{type(self).__name__}{self.group, self.value!r}"


class Group:
    """A base class containing methods common to many groups.

    Each subclass represents a family of parametrised groups.

    Parameters
    ----------
    n: int
        The primary group parameter, such as order or degree. The
        precise meaning of n changes from subclass to subclass.
    """

    def __init__(self, n):
        self.n = n

    def __call__(self, value):
        """Create an element of this group."""
        return Element(self, value)

    def __str__(self):
        """Return a string in the form symbol then group parameter."""
        return f"{self.symbol}{self.n}"

    def __repr__(self):
        """Return the canonical string representation of the element."""
        return f"{type(self).__name__}({self.n!r})"
