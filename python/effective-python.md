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

## `yield` over returning a list

- `yield` is more memory efficient than returning a list
- `yield` can be used to create infinite sequences


## what happends when call `for x in foo`?

1. `foo.__iter__()` is called
2. `__iter__` returns an iterator object
3. `iter.__next__()` is called repeatedly until `StopIteration` is raised


Example:
```python
def normalize(nums):
    if iter(nums) is nums:
        raise TypeError("Expected a sequence of numbers")
    s = sum(nums) # call __iter__
    for i in nums: # another call to __iter__
        yield i/s

class Visits:
    def __init__(self, path) -> None:
        self.path = path

    def __iter__(self):
        with open(self.path) as f:
            for line in f:
                yield int(line)

norm_it = normalize(Visits('file.txt'))
print(list(norm_it))
```
## `yield from` for composing/chaining generators

## avoid `send` and `throw` in generators

a better way to provide exceptional behaviour is to use a class that implements `__iter__` along with method to cause exceptional state transision

## itertools

all takes iterators and returns iterators

### combining
- `chain`
- `tee`:  `it1,it2 = itertools.tee(it,2)`
- `zip_longest`
- `cycle`
- `repeat`

### filtering
- `islice`
- `takewhile`
- `dropwhile`
- `filterfalse`

### transforming
- `accumulate`: see also `functools.reduce`

### combinations
- `product`
- `permutations`
- `combinations`
- `combinations_with_replacement`

## implement stateful hooks as callable

Example

```python
class BetterCountMissing:
    def __init__(self) -> None:
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0
current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
]
counter = BetterCountMissing()
result = defaultdict(counter, current)
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
```
## use @classmethod polymorphism to construct objects

- python only support a single constructor `__init__` per class
- use `@classmethod` to define alternative constructors

## use `super().__init__` 

the superclasses in diamond inheritance are called only once. The order of classes in the inheritance list matters.

## compose functionality with mix-in

## use collections.abc for custom container types

https://docs.python.org/3/library/collections.abc.html

to define an abstract base class, use
`from abc import ABC` and decorator `@abstractmethod` for meothod of subclass of `ABC`

https://docs.python.org/3/library/abc.html

## @property caveats

- prefer simple public attributes for  new class interfactes
- use `@property` to define special behaviour if necessary 
- modify related ojects in the setter not the getter, if necessary at all
- avoid computation heavy operations and unexpected side effects
- methods for an attributes can only be shared by subclasses


