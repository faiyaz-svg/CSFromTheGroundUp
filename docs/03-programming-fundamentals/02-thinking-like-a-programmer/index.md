# Thinking like a programmer

Cheat sheet for the chapter. Snippets were run on Python 3.14.4, mypy 2.4.0 and TypeScript 7.0.2 (as of 2026).

## Lessons

1. [Recursion](01-recursion.md)
2. [References, mutability and copying](02-references-mutability-and-copying.md)
3. [Type systems](03-type-systems.md)
4. [Reading code and debugging](04-reading-code-and-debugging.md)

## Key terms

| Term | Meaning | Lesson |
|---|---|---|
| Base case | The input a recursive function answers without recursing | [1](01-recursion.md) |
| Call stack | One frame per active call; a call pushes, a return pops | [1](01-recursion.md) |
| Memoization | Store results by arguments so a call is never repeated | [1](01-recursion.md) |
| Aliasing | Two names (or slots) refer to one object | [2](02-references-mutability-and-copying.md) |
| Mutable, immutable | Contents can, or cannot, change after creation | [2](02-references-mutability-and-copying.md) |
| Shallow, deep copy | New container with shared contents; new container with copied contents | [2](02-references-mutability-and-copying.md) |
| Static, dynamic typing | Types checked before running; checked while running | [3](03-type-systems.md) |
| Strong, weak typing | Mismatches are refused; mismatches are converted silently | [3](03-type-systems.md) |
| Duck typing | Any object with the needed methods works | [3](03-type-systems.md) |
| Reproduction | Small, reliable way to trigger the bug | [4](04-reading-code-and-debugging.md) |
| Bisecting | Halving the range of commits or lines that may hold the bug | [4](04-reading-code-and-debugging.md) |

## Recursion

```python
from functools import cache
import sys

@cache                      # memoize; arguments must be hashable
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)   # base case n < 2

print(sys.getrecursionlimit())   # 1000 by default; RecursionError past it
```

| Rule | Why |
|---|---|
| Base case first, and every call moves toward it | No base case or no progress means `RecursionError` |
| Depth grows with input size: use a loop or an explicit stack | Python does not optimize tail calls |
| Two recursive calls per level: add `@cache` | Subproblems repeat exponentially often |

## References and copying

| Code | Effect |
|---|---|
| `b = a` | Another name for the same object |
| `a.copy()`, `list(a)`, `a[:]`, `dict(a)` | Shallow copy |
| `copy.deepcopy(a)` | Deep copy |
| `[[0] * 2] * 3` | Three references to one row; use `[[0] * 2 for _ in range(3)]` |
| `def f(x, bucket=[])` | One shared default; use `None` and create inside |
| `x += y` on a list | Mutates in place; on a `str` or `int` it rebinds |

Immutable: `int`, `float`, `bool`, `str`, `bytes`, `tuple`, `frozenset`, `None`. A tuple holding a list can still change through that list. A function can mutate what it is passed; it cannot rebind your variable.

## Types

| Language | Checked | Conversions |
|---|---|---|
| Python | Dynamic | Strong |
| JavaScript | Dynamic | Weak |
| Java, Go | Static | Strong |
| C | Static | Weak |
| TypeScript | Static (build time, erased) | Inherits JavaScript's |

```python
def first(items: list[str]) -> str | None: ...   # 3.10+ for X | None
```

```bash
mypy file.py          # reports mismatches; Python itself ignores hints
```

## Debugging

| Tool | Use |
|---|---|
| `print` | Quick look; delete after |
| `logging.debug("x=%s", x)` | Kept in code; levels switch it on and off |
| `breakpoint()` | Stops in pdb: `p expr`, `n`, `s`, `c`, `l`, `w`, `b N`, `q` |
| VS Code | F9 breakpoint, F5 run, F10 over, F11 into, Shift+F11 out |
| `git bisect start BAD GOOD`, `git bisect run CMD`, `git bisect reset` | Find the first bad commit |

Order of work: reproduce, hypothesize, observe, fix one thing, rerun the reproduction and the tests. Read a traceback from the bottom.
