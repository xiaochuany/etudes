#  effective python

## dict

- use `dict.get` to provide default values
- use `collections.defaultdict` to provide default values
- overwirte `__missing__` method of `dict` to provide key-dependent default values

## scope

when referencing a variable, python will search for the variable in the following order:

1. local scope
2. enclosing scopes
3. global scope i.e. scope of the module
4. built-in scope

Assigning a variable will create a local variable in the local scope, if the variable is not already defined in the local scope.

`nonlocal` keyword can be used to assign a variable in the enclosing scope. However, its side effects can be hard to follow. It's better to wrap the variable in a helper class.

## default arguments

- default arguments are evaluated only once at the module load time, not at the time of function call

## positional-only and keyword-only arguments

- arguments before `/` positional-only
- arguments after  `*` are keyword-only
- everything in between can be positional or keyword

## use `functools.wraps` in decorators to preserve metadata of the original function


## comprehensions

- both `for` and `if` can be used in comprehensions. Evaluation order: `for` followed by `if`. 
- Better only use walrus assignment expressions in `if` part. 