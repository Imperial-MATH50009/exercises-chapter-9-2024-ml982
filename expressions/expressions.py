from functools import singledispatch
import numbers


class Expression:
    """An expression in a mathematical expression tree."""

    def __init__(self, *operands):
        """Create an expression with the given operands."""
        self.operands = operands

    def __add__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Add(self, other)

    def __radd__(self, other):
        if isinstance(other, numbers.Number):
            return Add(Number(other), self)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Sub(self, other)

    def __rsub__(self, other):
        if isinstance(other, numbers.Number):
            return Sub(Number(other), self)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Mul(self, other)

    def __rmul__(self, other):
        if isinstance(other, numbers.Number):
            return Mul(Number(other), self)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Div(self, other)

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Number):
            return Div(Number(other), self)
        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Pow(self, other)

    def __rpow__(self, other):
        if isinstance(other, numbers.Number):
            return Pow(Number(other), self)
        return NotImplemented


class Terminal(Expression):
    """A terminal in an expression."""

    precedence = 3

    def __init__(self, value):
        self.value = value
        super().__init__()

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)  # finished all code in terminal


class Number(Terminal):
    """A number in an expression."""

    def __init__(self, value):
        if not isinstance(value, numbers.Number):
            raise TypeError("Number must be a number")
        super().__init__(value)  # should be done


class Symbol(Terminal):
    """A symbol in an expression."""

    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError("Symbol must be a string")
        super().__init__(value)  # should be done


class Operator(Expression):
    """An operator in an expression."""

    def __repr__(self):
        """Return the canonical string representation of the operator."""
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        def brackets(expr):
            if expr.precedence < self.precedence:
                return f"({expr})"
            else:
                return str(expr)

        return " ".join((brackets(self.operands[0]),
                        self.symbol, brackets(self.operands[1])))
        # need to implement this


class Add(Operator):
    """Addition operator."""

    precedence = 0
    symbol = "+"


class Sub(Operator):
    """Subtraction operator."""

    precedence = 0
    symbol = "-"


class Mul(Operator):
    """Multiplication operator."""

    precedence = 1
    symbol = "*"


class Div(Operator):
    """Division operator."""

    precedence = 1
    symbol = "/"


class Pow(Operator):
    """Exponentiation operator."""

    precedence = 2
    symbol = "^"


# Exercise 9.7
def postvisitor(expr, fn, **kwargs):
    """
    Visit an Expression in postorder applying a function to every node.

     Parameters
     ----------
     expr: Expression - The expression to be visited.
     fn: function(node, *o, **kwargs)
        A function to be applied at each node. The function should take
        the node to be visited as its first argument, and the results of
        visiting its operands as any further positional arguments. Any
        additional information that the visitor requires can be passed in
        as keyword arguments.
     **kwargs: Any additional keyword arguments to be passed to fn.
    """
    stack = []  # use pseudocode in book to implement this
    visited = {}
    stack.append(expr)
    while stack:
        e = stack.pop()
        unvisited_children = []
        for o in e.operands:
            if o not in visited:
                unvisited_children.append(o)

        if unvisited_children:
            stack.append(e)
            for uc in unvisited_children:
                stack.append(uc)

        else:
            visited[e] = fn(e, *[visited[o] for o in e.operands], **kwargs)

    return visited[expr]

# Exercise 9.8

@singledispatch
def differentiate(expr, *o, **kwargs):
    """Differentiate an expression with respect to a symbol."""
    raise NotImplementedError(f"Cannot differentiate  a {type(expr)}.__name__")

@differentiate.register(Symbol)
def _(expr, *o, **kwargs):
    """Differentiate a symbol with respect to itself."""
    if kwargs['var'] == expr.value:
        return 1.0
    else:
        return 0.0

@differentiate.register(Number)
def _(expr, *o, **kwargs):
    """Differentiate a number with respect to anything."""
    return 0.0

@differentiate.register(Add)
def _(expr, *o, **kwargs):
    """Differentiate an addition operator."""
    return o[0] + o[1]

@differentiate.register(Sub)
def _(expr, *o, **kwargs):
    """Differentiate a subtraction operator."""
    return o[0] - o[1]

@differentiate.register(Mul)
def _(expr, *o, **kwargs):
    """Differentiate a multiplication operator."""
    return o[0] * expr.operands[1] + o[0] * expr.operands[1]  # product rule

@differentiate.register(Div)
def _(expr, *o, **kwargs):
    """Differentiate a division operator."""
    return (o[0] * expr.operands[1] - expr.operands[0] * o[1]) / \
           (expr.operands[1] ** 2)  # quotient rule

@differentiate.register(Pow)
def _(expr, *o, **kwargs):
    """Differentiate an exponentiation operator."""
    return expr.operands[1] * \
           (expr.operands[0] ** (expr.operands[1] - 1)) * o[0]  # chain rule
