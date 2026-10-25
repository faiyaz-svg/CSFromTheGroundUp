# OOP and paradigms

Cheat sheet for the chapter. Python snippets were run on Python 3.14.4, JavaScript and TypeScript on Node 24, and the Protocol check on mypy.

## Lessons

1. [Classes and objects](01-classes-and-objects.md)
2. [Encapsulation, inheritance and polymorphism](02-encapsulation-inheritance-and-polymorphism.md)
3. [Composition and interfaces](03-composition-and-interfaces.md)
4. [Functional programming ideas](04-functional-programming-ideas.md)

## Key terms

| Term | Meaning | Lesson |
|---|---|---|
| Class, object | The blueprint; one instance built from it with its own attributes | [1](01-classes-and-objects.md) |
| `self` | The object a method was called on, passed as the first argument | [1](01-classes-and-objects.md) |
| Dataclass | `@dataclass` writes `__init__`, `__repr__` and `__eq__` from annotated fields | [1](01-classes-and-objects.md) |
| Encapsulation | Keep internal state behind a small public interface | [2](02-encapsulation-inheritance-and-polymorphism.md) |
| Property | A method read like an attribute, with an optional validating setter | [2](02-encapsulation-inheritance-and-polymorphism.md) |
| Override, `super()` | Redefine a parent's method; call the parent's version | [2](02-encapsulation-inheritance-and-polymorphism.md) |
| MRO | The order of classes searched for an attribute: `Cls.__mro__` | [2](02-encapsulation-inheritance-and-polymorphism.md) |
| Polymorphism | One call, different behaviour depending on the object's class | [2](02-encapsulation-inheritance-and-polymorphism.md) |
| Composition | An object holds other objects and delegates to them (has-a) | [3](03-composition-and-interfaces.md) |
| ABC, Protocol | Interface enforced when an object is created; interface checked by a type checker | [3](03-composition-and-interfaces.md) |
| Dependency injection | Pass collaborators into a class instead of creating them inside | [3](03-composition-and-interfaces.md) |
| Pure function | Same arguments, same result, no side effects | [4](04-functional-programming-ideas.md) |
| Closure | A function plus the outer variables it uses | [4](04-functional-programming-ideas.md) |
| Higher-order function | Takes or returns a function (`map`, `filter`, `sorted(key=...)`) | [4](04-functional-programming-ideas.md) |

## Classes in Python and JavaScript

| | Python | JavaScript |
|---|---|---|
| Define | `class A:` | `class A {}` |
| Initializer | `def __init__(self, x):` | `constructor(x) {}` |
| Current object | `self` (explicit parameter) | `this` (implicit) |
| Create | `A(1)` | `new A(1)` |
| Inherit, call parent | `class B(A):`, `super().__init__(x)` | `class B extends A {}`, `super(x)` |
| Internal member | `_name` (convention only) | `#name` (enforced) |
| Read-only attribute | `@property` | `get name() {}` |
| Printable form | `__repr__` | `toString()` |

## Rules and snippets

```python
from dataclasses import dataclass, field, replace

@dataclass(frozen=True)              # frozen: fields cannot be assigned
class Item:
    name: str
    tags: list = field(default_factory=list)   # never `= []`

b = replace(Item("pen"), name="ink")   # a new object with one field changed
```

- Put per-object state in `__init__`. A mutable class attribute is shared by every instance, and `obj.x = ...` creates an instance attribute that hides the class one.
- A subclass `__init__` calls `super().__init__(...)`, or the parent's attributes are never set.
- Say the sentence: "X is a Y" in every use means inheritance can work; "X has a Y" or "X uses a Y" means composition. Prefer one parent and shallow hierarchies.
- A class that defines `__eq__` and not `__hash__` is unhashable, so it cannot be a dict key or set member.

```python
from abc import ABC, abstractmethod
from typing import Protocol

class Base(ABC):                      # TypeError on Base() or an incomplete subclass
    @abstractmethod
    def send(self, message: str) -> None: ...

class Notifier(Protocol):             # any class with this method matches; mypy checks it
    def send(self, message: str) -> None: ...
```

| Use | When |
|---|---|
| ABC | You control the implementations, want an error at creation, or share code in the base |
| Protocol | Implementations come from elsewhere, or you only describe what one function needs |
| Plain function | The "class" has only `__init__` and one method |

Dependency injection: `OrderService(notifier)` stores what it is given. Production passes a real object and tests pass a fake that records calls.

## Functional style

| Mutates in place (returns `None` in Python) | Returns a new value |
|---|---|
| `xs.sort()`, `xs.reverse()`, `xs.append(x)` | `sorted(xs)`, `list(reversed(xs))`, `[*xs, x]` |
| `d.update(e)` | `{**d, **e}` or `d \| e` |
| JavaScript: `arr.push(x)`, `arr.sort()` | `[...arr, x]`, `arr.toSorted()`, `arr.map(f)`, `arr.filter(f)` |

```python
[f(x) for x in xs if keep(x)]        # comprehension: filter and map
sorted(users, key=lambda u: u["age"])
lambda i=i: i                        # bind a loop variable's current value
```

- Side effects: printing, files, network, clock, random, changing an argument or global. Keep them at the edges and the middle pure.
- A closure captures variables, not values.
- `{**o}`, `[...a]` and `list(x)` are shallow copies; nested objects are still shared.
- React compares state by identity: use `setItems([...items, x])`, never `items.push(x)`.
- Node 24 runs `.ts` files by erasing types and accepts only erasable syntax (no constructor parameter properties).
