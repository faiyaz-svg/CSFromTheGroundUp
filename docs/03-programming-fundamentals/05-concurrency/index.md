# Concurrency

Cheat sheet for the chapter. Snippets were run on Python 3.14.4. Timings are approximate and vary by machine. Free-threaded Python status is as of 2026 ([Python docs](https://docs.python.org/3/howto/free-threading-python.html)).

## Lessons

1. [Concurrency, parallelism and race conditions](01-concurrency-parallelism-and-race-conditions.md)
2. [Locks, deadlocks and thread safety](02-locks-deadlocks-and-thread-safety.md)
3. [Threads, processes and asyncio](03-threads-processes-and-asyncio.md)

## Key terms

| Term | Meaning | Lesson |
|---|---|---|
| Concurrency | Tasks in progress with interleaved steps, possibly on one core | [1](01-concurrency-parallelism-and-race-conditions.md) |
| Parallelism | Tasks running at the same instant on different cores | [1](01-concurrency-parallelism-and-race-conditions.md) |
| Shared state | Data that several threads can read and change | [1](01-concurrency-parallelism-and-race-conditions.md) |
| Race condition, data race | Result depends on timing, and two threads touch the same memory with a write | [1](01-concurrency-parallelism-and-race-conditions.md) |
| Critical section | Code that must not run in two threads at once | [1](01-concurrency-parallelism-and-race-conditions.md) |
| Read-modify-write | The three steps inside `x += 1` | [1](01-concurrency-parallelism-and-race-conditions.md) |
| GIL | CPython lock: one thread runs Python bytecode at a time (absent in free-threaded builds) | [1](01-concurrency-parallelism-and-race-conditions.md) |
| Mutex, semaphore | One holder at a time; up to $n$ holders at a time | [2](02-locks-deadlocks-and-thread-safety.md) |
| Deadlock | A cycle of threads each waiting for a resource another holds | [2](02-locks-deadlocks-and-thread-safety.md) |
| Thread-safe | Correct when called from several threads, without caller locking | [2](02-locks-deadlocks-and-thread-safety.md) |
| I/O-bound, CPU-bound | Mostly waiting on the outside world; mostly computing | [3](03-threads-processes-and-asyncio.md) |
| Coroutine, event loop | An `async def` function; the scheduler that runs tasks at each `await` | [3](03-threads-processes-and-asyncio.md) |

## Syntax

```python
import threading, queue, asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

lock = threading.Lock()
with lock:                                  # acquire, then always release
    ...
lock.acquire(timeout=1)                     # False if not obtained in time
threading.Semaphore(2)                      # at most 2 holders
q = queue.Queue(maxsize=10)                 # q.put(x), q.get()

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(func, items))   # same API for ProcessPoolExecutor

async def task():
    await asyncio.sleep(1)                  # never time.sleep here

async def main():
    return await asyncio.gather(task(), task())

asyncio.run(main())
```

## Choosing a tool

| Work | Use | Why |
|---|---|---|
| A few to tens of blocking I/O waits | Threads | Waits overlap, GIL released while waiting |
| Thousands of I/O waits | asyncio | A coroutine costs far less than a thread |
| CPU-bound Python code | Processes | Own interpreter and GIL per process |
| Blocking call inside `async def` | `asyncio.to_thread` | Keeps the event loop free |

## Deadlock conditions

| Condition | Remove it by |
|---|---|
| Mutual exclusion | Not sharing the resource (queues, copies) |
| Hold and wait | Taking all locks at once, or holding fewer |
| No preemption | Timeouts that release and retry |
| Circular wait | A global lock order |

## Rules

1. Any read-modify-write on shared data needs a lock or a queue.
2. Every access to the data uses the same lock.
3. Keep critical sections small, with no slow calls inside.
4. Take locks in one global order.
5. Never block inside a coroutine.
