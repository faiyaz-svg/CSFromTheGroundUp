# Performance

A cheat sheet for the chapter. Each lesson link has the explanation; this page only collects the commands, tables and rules.

## Lessons

1. [Profiling and benchmarking](01-profiling-and-benchmarking.md)
2. [How CPUs go fast](02-how-cpus-go-fast.md)

## The method

1. Measure the current time on a fixed input.
2. Profile to find the hotspot.
3. Change one thing in the hotspot.
4. Measure again the same way. Check the output is unchanged.
5. Stop when it is fast enough.

A part that takes a fraction $f$ of the run saves at most that fraction, even if you make it free.

## Commands

| Need | Use |
|---|---|
| Time a short expression | `python -m timeit -s "setup" "expression"` |
| Time code in a script | `min(timeit.repeat(stmt, setup, number=N, repeat=5)) / N` |
| Profile a script | `python -m cProfile -s cumtime script.py` |
| Save and read a profile | `python -m cProfile -o out.prof script.py`, then `pstats.Stats("out.prof").sort_stats("cumtime").print_stats(10)` |
| Flame graph of a running program | `py-spy record -o profile.svg -- python script.py` (awareness only) |

## Reading a profile

| Term | Meaning |
|---|---|
| `tottime` | Time in the function's own code |
| `cumtime` | Time including everything it calls |
| Hotspot | The function with the largest `tottime`, or one wide box at the top of a flame graph |
| Deterministic profiler | `cProfile`: counts every call, adds overhead per call |
| Sampling profiler | py-spy: looks at the stack many times a second, low overhead |

## Benchmark traps

| Trap | Fix |
|---|---|
| Timing a function that changes its input (`sort()`, `pop`) | Copy the input inside the timed code |
| One run | Repeat 5 or more times, take the minimum, note the spread |
| Warm-up | Run once before timing, or ignore the first result |
| Tiny inputs | Measure at the real size |
| Setup or printing inside the timer | Move it to `setup` |
| Profiler overhead | Rank with `cProfile`, confirm with `timeit` |

## Hardware effects

| Trick | Rewards | Seen in Python |
|---|---|---|
| Pipelining | Few stalls | No |
| Branch prediction | Predictable branches (sorted data) | About 10 to 20% |
| Caches | Locality: small strides, data that fits | About 1.2 to 1.4 times on a large grid |
| SIMD | One operation over a contiguous array | Only via libraries such as NumPy |
| False sharing | Per-thread data in separate cache lines | Hidden by the GIL |

## Rules of thumb

- Profile before changing code. The slow line is often a hidden $O(n)$ call in a loop.
- Algorithm first, then built-ins, then hardware tuning.
- Report timings as "about" with a range from at least 3 runs.
- A change that alters the output is not an optimisation.
