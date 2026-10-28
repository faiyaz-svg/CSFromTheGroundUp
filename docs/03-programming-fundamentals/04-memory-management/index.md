# Memory management

Cheat sheet for the chapter. Python snippets were run on Python 3.14.4. The C and Rust snippets were not compiled on this machine.

## Lessons

1. [Pointers and manual memory](01-pointers-and-manual-memory.md)
2. [Garbage collection and reference counting](02-garbage-collection-and-reference-counting.md)
3. [Ownership and borrowing in Rust](03-ownership-and-borrowing-in-rust.md)

## Key terms

| Term | Meaning | Lesson |
|---|---|---|
| Address, pointer | A byte's number in memory; a variable that holds one | [1](01-pointers-and-manual-memory.md) |
| `malloc`, `free` | Ask the C allocator for heap bytes; give them back | [1](01-pointers-and-manual-memory.md) |
| Memory leak | Memory never given back (C) or still reachable but useless (GC languages) | [1](01-pointers-and-manual-memory.md), [2](02-garbage-collection-and-reference-counting.md) |
| Use-after-free, double free | Touching a freed block; freeing a block twice | [1](01-pointers-and-manual-memory.md) |
| Buffer overflow | Writing past the end of a block, into its neighbour | [1](01-pointers-and-manual-memory.md) |
| Undefined behaviour | The language places no rules on what happens | [1](01-pointers-and-manual-memory.md) |
| Reference count | Number of references to an object; free at 0 | [2](02-garbage-collection-and-reference-counting.md) |
| Reference cycle | Objects that refer to each other, so counts never reach 0 | [2](02-garbage-collection-and-reference-counting.md) |
| Mark-and-sweep | Mark what is reachable from the roots, free the rest | [2](02-garbage-collection-and-reference-counting.md) |
| Generational GC | Collect young objects often, old ones rarely | [2](02-garbage-collection-and-reference-counting.md) |
| GC pause | Time the program is stopped while the collector runs | [2](02-garbage-collection-and-reference-counting.md) |
| Ownership, move | One owner per value, freed when it leaves scope; transfer of the owner | [3](03-ownership-and-borrowing-in-rust.md) |
| Borrow, `&`, `&mut` | Temporary shared read access; temporary exclusive write access | [3](03-ownership-and-borrowing-in-rust.md) |
| Lifetime | How long a reference stays valid | [3](03-ownership-and-borrowing-in-rust.md) |

## Three ways to manage memory

| | C | Python, Java, JavaScript | Rust |
|---|---|---|---|
| Who frees | You, with `free` | The runtime | The compiler inserts the cleanup |
| Cost | None at run time | Memory overhead, possible pauses | Rules at compile time |
| Typical bug | Leak, use-after-free, double free, overflow | Leak through a cache or listener | Compile errors until the rules are met |

## Python tools

| Task | Code |
|---|---|
| Reference count (one extra for the call) | `sys.getrefcount(obj)` |
| Run the cycle collector | `gc.collect()` |
| Reference that does not keep an object alive | `weakref.ref(obj)` |
| Find what allocates | `tracemalloc.start()`, `take_snapshot()`, `after.compare_to(before, "lineno")` |
| Bounded history | `collections.deque(maxlen=n)` |

## Rules of thumb

- Every `malloc` has exactly one `free` on every path. Set the pointer to `NULL` after.
- Check every length before writing to a buffer.
- GC languages leak through collections that only grow. Give caches a size limit.
- Release files and locks with `with`, not with `__del__`.
- Rust: one owner, many `&` or one `&mut`. Treat `.clone()` and `unsafe` as things to review.
