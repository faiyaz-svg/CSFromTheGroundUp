# The CPU

After this you can describe what a CPU does with each instruction, and say what clock speed, cores, pipelining and branch prediction do and do not tell you about speed.

Before this: [boolean algebra and circuits](02-boolean-algebra-and-circuits.md).

## The idea

A CPU is a very fast, very literal clerk. It has a small desk (the registers), a pile of numbered instructions in memory, and a finger marking the place in the pile. It repeats one routine forever: read the instruction under the finger, work out what it asks, do it, move the finger. Python, a browser and a database all reduce to this loop running billions of times per second.

```mermaid
flowchart LR
    F["Fetch<br/>read instruction at the program counter"] --> D["Decode<br/>find the operation and its operands"]
    D --> E["Execute<br/>ALU computes, or memory is read or written"]
    E --> W["Write back<br/>result goes to a register"]
    W --> F
```

## Key terms

A **CPU** (central processing unit) is the chip that fetches and runs instructions. An **instruction** is one small operation such as "add these two registers" or "load a value from this address". The set of instructions a CPU understands is its **instruction set**; x86-64 (Intel and AMD) and ARM (phones, Apple silicon) are the two you meet.

A **register** is a storage slot inside the CPU. The **program counter** (PC) is the register holding the address of the next instruction.

The **clock** is a signal that ticks at a fixed rate, and a **cycle** is one tick. **Clock speed** is ticks per second, measured in **GHz** (billions of cycles per second).

A **core** is one complete instruction-running unit, with its own registers and ALU. A chip with several cores runs several instruction streams at the same time. **Simultaneous multithreading** (SMT; Intel calls it Hyper-Threading) lets one core present itself as two **logical CPUs** by sharing its units between two threads.

## How it works

Fetch, decode, execute. The CPU reads the instruction at the address in the PC and increases the PC. The decoder splits it into an operation and operands. The ALU, a memory access or a jump then carries it out, and a result goes into a register. A jump loads a new address into the PC, and that is how `if` and `for` work at this level. [Machine code and assembly](../03-code-to-running-program/01-machine-code-and-assembly.md) shows real instructions.

Clock speed. At 4 GHz a cycle lasts 0.25 ns. Many simple instructions take one cycle once the pipeline is full, and a memory miss can cost hundreds. Clock speed alone does not rank CPUs: a newer design can finish more instructions per cycle, and a faster clock draws more power and makes more heat, so chips raise and lower it constantly (boost clocks). The figure to ask about is work per second for your workload.

Pipelining. A CPU does not finish one instruction before starting the next. As the diagram shows, it works on different stages of different instructions at once. A pipeline does not make one instruction faster; it raises the number finishing per cycle.

```text
cycle:           1    2    3    4    5    6
instruction 1    F    D    E    W
instruction 2         F    D    E    W
instruction 3              F    D    E    W
                 F = fetch, D = decode, E = execute, W = write back
```

Branch prediction. A conditional jump makes the pipeline's next instruction unknown until the condition is computed. Rather than wait, the CPU guesses which way the branch goes and runs ahead. A right guess costs nothing; a wrong guess throws away the work started on the wrong path, which costs roughly 10 to 20 cycles ([Wikipedia: branch predictor](https://en.wikipedia.org/wiki/Branch_predictor)). Predictors are right far more often than not, so a loop's branch is nearly free, while a branch that depends on random data (an `if` on an unsorted list's values) is costly.

Cores. More cores help only when there is independent work to give them. A program with one thread uses one core. Splitting work across cores needs threads or processes, and the parts that must run in order limit the gain. In CPython, threads running Python code share one lock (the GIL), so CPU-bound parallelism in Python usually uses separate processes, as in the lab.

| Item | Typical value (as of 2026) | Source |
|---|---|---|
| Desktop CPU cores | 6 to 16 in a mainstream Ryzen 9000 chip | [Wikipedia: Ryzen](https://en.wikipedia.org/wiki/Ryzen) |
| Example: Ryzen 9 9950X | 16 cores, 32 threads, 4.3 GHz base, up to 5.7 GHz boost | [Best Buy listing](https://www.bestbuy.com/product/amd-ryzen-9-9950x-16-core-32-thread-4-3-ghz-5-7-ghz-max-boost-socket-am5-unlocked-desktop-processor-silver/JXKQHH5XP5) |

The numbers move every year; read the vendor's current specification page before quoting one.

## Worked examples

<div class="example" markdown>

### Example 1: a toy CPU

We want to see fetch, decode and execute in code. The program loads 5 and 3, then adds 3 to the first register until the second counts down to zero: the sum is $5 + 3 + 2 + 1 = 11$.

1. The list `program` is memory. Each instruction is a tuple of an operation and two operands.
2. `pc` starts at 0. The loop fetches `program[pc]` and increases `pc`.
3. The `if` chain decodes the operation and executes it. `JNZ` ("jump if not zero") changes `pc`, which makes a loop.

<details class="code" markdown>
<summary>In code</summary>

```python
program = [
    ("LOAD", 0, 5),     # r0 = 5
    ("LOAD", 1, 3),     # r1 = 3
    ("ADD", 0, 1),      # r0 = r0 + r1
    ("SUB1", 1, None),  # r1 = r1 - 1
    ("JNZ", 1, 2),      # if r1 != 0, jump to instruction 2
    ("HALT", None, None),
]
regs = [0, 0]
pc = 0                              # program counter
while True:
    op, x, y = program[pc]          # fetch (and split into fields: decode)
    pc += 1
    if op == "LOAD":                # execute
        regs[x] = y
    elif op == "ADD":
        regs[x] += regs[y]
    elif op == "SUB1":
        regs[x] -= 1
    elif op == "JNZ":
        if regs[x] != 0:
            pc = y
    elif op == "HALT":
        break
print(regs)
```

```text
[11, 0]
```

</details>

Check: `r0` ends at 5 + 3 + 2 + 1 = 11, and `r1` at 0, which is what the output shows. Real CPUs encode instructions as binary numbers and run the stages in hardware, but the structure is the same.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: comparing CPUs by GHz. A 5 GHz chip of one design can be slower than a 4 GHz chip of another. Compare benchmark results for a workload like yours.

Watch out: assuming more cores make a program faster. A single-threaded program does not change. Even a parallel program gains less than the core count, because of the serial parts and shared memory.

Watch out: counting logical CPUs as cores. `os.cpu_count()` reports logical CPUs, which on a chip with SMT is twice the physical cores.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: instruction set, program counter, cycle, IPC (instructions per cycle), pipeline, branch misprediction, core, logical CPU.

Prompts to try:

- "My Python script processes 5,000 CSV files, takes 20 minutes and uses 8% of my 12-logical-CPU machine. Show how to use `concurrent.futures.ProcessPoolExecutor`, and say what limits the speed-up."
- "Explain why this loop runs faster when the input list is sorted, in terms of branch prediction. Which language and compiler settings would make it matter?"

What to check:

- Advice to use threads for CPU-bound Python code. Time it; the GIL usually means no speed-up.
- A claimed speed-up of N times for N cores. Measure it, as in the lab.
- Specific clock speeds, core counts or branch-penalty cycles with no source or year.

</div>

## Quiz

1\. List the stages of the instruction cycle and say which one changes the program counter on a jump.

<details class="solution" markdown>
<summary>Answer</summary>

Fetch, decode, execute (and write back). The execute stage of a jump instruction loads a new address into the program counter.

</details>

2\. A chip at 4 GHz runs one instruction per cycle on average. About how many instructions is that per second, and how long is one cycle?

<details class="solution" markdown>
<summary>Answer</summary>

4 billion instructions per second ($4 \times 10^9$), and one cycle is $1 / (4 \times 10^9)$ s $= 0.25$ ns.

</details>

3\. You run 8 CPU-heavy tasks one after another and it takes 40 s. On an 8-core machine you start 8 processes and get 7 s. Is that surprising?

<details class="solution" markdown>
<summary>Answer</summary>

No. The speed-up is 5.7 times, not 8. Process start-up, shared memory bandwidth, boost clocks falling when all cores are busy and any serial part all cost time.

</details>

4\. What happens in the pipeline when the branch predictor guesses wrong?

<details class="solution" markdown>
<summary>Answer</summary>

The instructions fetched after the branch on the wrong path are thrown away, and the pipeline restarts from the correct address. That costs roughly 10 to 20 cycles of work.

</details>

## Lab

<div class="lab" markdown>

### Lab: how many cores can you use?

Goal: measure how a CPU-bound task speeds up as you add processes. Time: about 15 minutes. Runs in: any terminal with Python 3.

1. Save the script below as `cores.py`. It runs 8 equal jobs, first one after another, then with 2, 4 and 8 worker processes.
2. Run `python cores.py` (or `python3`). It takes about 10 seconds.
3. Write down the speed-up for each count and compare with `os.cpu_count()`.
4. Change the job count to 2 and run again. Predict first: what is the best speed-up 8 workers can give?
5. Cleanup: nothing to remove.

```python
import os
import time
from multiprocessing import Pool

def work(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

if __name__ == "__main__":
    print("logical CPUs:", os.cpu_count())
    jobs = [10_000_000] * 8
    start = time.perf_counter()
    for n in jobs:
        work(n)
    one = time.perf_counter() - start
    print(f"1 process : {one:.2f} s")
    for workers in (2, 4, 8):
        start = time.perf_counter()
        with Pool(workers) as pool:
            pool.map(work, jobs)
        t = time.perf_counter() - start
        print(f"{workers} processes: {t:.2f} s   speedup {one / t:.1f}x")
```

Expected result: the speed-up grows with the worker count but stays below it. The output below is from the author's Windows 11 PC (AMD Ryzen 5 5600G: 6 cores, 12 logical CPUs, Python 3.14). Yours will differ.

```text
logical CPUs: 12
1 process : 3.55 s
2 processes: 2.15 s   speedup 1.7x
4 processes: 1.06 s   speedup 3.4x
8 processes: 0.87 s   speedup 4.1x
```

<details class="solution" markdown>
<summary>Solution</summary>

The `if __name__ == "__main__"` guard is required on Windows and macOS, where child processes re-import the script. Without it each worker would start more workers.

The 8-worker run gets 4.1 times, not 8, because this chip has 6 physical cores. With 8 workers and 8 jobs on 6 physical cores, some cores run two workers each through SMT, and a core shared by two threads does less than two full cores. The clock also drops a little when all cores are busy. With 2 jobs, extra workers cannot help: only 2 jobs exist, so the best case is 2 times. On the author's PC the 2-job run gave about 1.4 times for every worker count, because process start-up is a large share of a 0.9 s task.

</details>

</div>

## Where this shows up

- [Machine code and assembly](../03-code-to-running-program/01-machine-code-and-assembly.md) shows the instructions this lesson describes.
- [Processes, threads and scheduling](../../02-operating-systems-and-linux/01-os-concepts/02-processes-threads-and-scheduling.md) covers how the operating system shares cores among programs.
- [GPUs and parallel hardware](06-gpus-and-parallel-hardware.md) takes the "many cores" idea much further.
