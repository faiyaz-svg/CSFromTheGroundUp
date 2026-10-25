# Python basics

Cheat sheet for the chapter. Snippets were run on Python 3.14.4; features newer than 3.10 are marked with the version that added them.

## Lessons

1. [Values, types and variables](01-values-types-and-variables.md)
2. [Control flow](02-control-flow.md)
3. [Functions and scope](03-functions-and-scope.md)
4. [Lists, dicts, sets and tuples](04-lists-dicts-sets-and-tuples.md)
5. [Strings and formatting](05-strings-and-formatting.md)
6. [Errors and exceptions](06-errors-and-exceptions.md)
7. [Files and I/O](07-files-and-io.md)
8. [Modules, packages, pip and venv](08-modules-packages-pip-and-venv.md)

## Key terms

| Term | Meaning | Lesson |
|---|---|---|
| Name binding | A variable is a name pointing at an object; assignment copies nothing | [1](01-values-types-and-variables.md) |
| Truthiness | Falsy: `False`, `None`, numeric zero, empty containers and strings; all else truthy | [2](02-control-flow.md) |
| Iterable, iterator | Anything a `for` loop can walk; the object that yields items and is used up once | [2](02-control-flow.md) |
| LEGB | Name lookup order: Local, Enclosing, Global, Built-in | [3](03-functions-and-scope.md) |
| Closure | A function that keeps variables from its enclosing function | [3](03-functions-and-scope.md) |
| Hashable | Has a fixed hash and `==`; needed for dict keys and set members | [4](04-lists-dicts-sets-and-tuples.md) |
| Code point, encoding | A Unicode number; the rule that turns text into bytes | [5](05-strings-and-formatting.md) |
| EAFP, LBYL | Try and handle failure; check first | [6](06-errors-and-exceptions.md) |
| Context manager | Object used by `with` that cleans up on exit, even after an exception | [7](07-files-and-io.md) |
| venv | A per-project folder with its own interpreter link and packages | [8](08-modules-packages-pip-and-venv.md) |

## Numbers and comparison

| Expression | Result | Note |
|---|---|---|
| `7 / 2` | `3.5` | `/` always returns a float |
| `7 // 2`, `-7 // 2` | `3`, `-4` | `//` floors toward negative infinity |
| `-7 % 2` | `1` | `a == (a // b) * b + a % b` always holds |
| `0.1 + 0.2 == 0.3` | `False` | Use `math.isclose`, integers or `Decimal("0.1")` |
| `round(2.5)` | `2` | Rounds half to even |
| `a == b` / `a is b` | value / identity | Use `is` only for `None` |

## Control flow and functions

```python
for i, x in enumerate(xs, start=1): ...      # index and item
for a, b in zip(xs, ys, strict=True): ...    # strict: 3.10
for n in range(2, 10, 3): ...                # stop is excluded
for x in xs: ...                            # add an else: block, runs if no break
match cmd.split():                           # 3.10
    case ["go", d] if d in DIRS: ...
    case _: ...
if (n := len(data)) > 2: ...                 # walrus: 3.8
def f(a, b=None, /, c=1, *args, key, **kw): ...   # / is 3.8
```

Default values are evaluated once, so use `None` for a mutable default:

```python
def add(item, bucket=None):
    if bucket is None:
        bucket = []
```

Closures capture variables, not values: write `lambda i=i: i` inside a loop. `global` and `nonlocal` are needed only to assign to an outer name.

## Collections

| | `list` | `tuple` | `dict` | `set` |
|---|---|---|---|---|
| Literal | `[1, 2]` | `(1, 2)` | `{"a": 1}` | `{1, 2}`, empty is `set()` |
| Mutable | yes | no | yes | yes |
| `x in c` | $O(n)$ | $O(n)$ | $O(1)$ average | $O(1)$ average |
| Order | position | position | insertion | none |

Rules: `xs.sort()` returns `None` and `sorted(xs)` returns a new list. `[[0] * 3] * 3` shares one row; use a comprehension. Merge dicts with `a | b` (3.9). `Counter` counts, `defaultdict(list)` groups, `deque` is a queue.

## Strings and formatting

| Spec | Example | Output |
|---|---|---|
| Thousands and decimals | `f"{1234.5:,.2f}"` | `1,234.50` |
| Width and alignment | `f"{'ab':>6}"`, `<`, `^` | right, left, centre |
| Zero pad | `f"{3:03d}"` | `003` |
| Percent | `f"{0.256:.1%}"` | `25.6%` |
| Binary, hex | `f"{255:08b}"`, `f"{255:#x}"` | `11111111`, `0xff` |
| Debug | `f"{x=}"` | `x=7` |

A `str` is code points and `bytes` is raw data: `s.encode("utf-8")` and `b.decode("utf-8")`. Join with `"".join(parts)`, not `+=` in a loop. Never build SQL with an f-string; pass parameters. Quote reuse inside an f-string is 3.12 (PEP 701); `t"..."` template strings are 3.14.

## Errors and files

```python
try:
    risky()
except (KeyError, ValueError) as e:     # specific classes only
    raise ConfigError("bad config") from e
else:
    ...                                  # ran with no exception
finally:
    ...                                  # always runs
```

- Never use a bare `except:`. Use `assert` for internal checks only, because `-O` removes it.
- `except*` and `ExceptionGroup`, and `e.add_note()`, are 3.11. `except A, B:` without parentheses (no `as`) is 3.14.
- `with open(path, encoding="utf-8") as f:` always names the encoding. Add `newline=""` for `csv` and `newline="\n"` to stop `\r\n` on Windows.
- `Path("data") / "in.csv"` instead of string paths; `.read_text(encoding="utf-8")`, `.glob("*.csv")`, `.mkdir(parents=True, exist_ok=True)`.
- Modes: `r`, `w` (truncates), `a`, `x`, plus `b` for binary.

## Modules and environments

| Task | Windows PowerShell | Linux and macOS |
|---|---|---|
| Create venv | `python -m venv .venv` | `python3 -m venv .venv` |
| Activate | `.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| Install | `python -m pip install NAME` | same |
| Save | `python -m pip freeze > requirements.txt` | same |
| Recreate | `python -m pip install -r requirements.txt` | same |
| Run a package module | `python -m pkg.mod` | same |

Guard scripts with `if __name__ == "__main__":`. Do not name a file after a standard library module (`random.py`, `json.py`). Do not commit `.venv`.
