# Hardware

A cheat sheet for the chapter. Each lesson link has the explanation; this page only collects the terms, tables and rules.

## Lessons

1. [Transistors and logic gates](01-transistors-and-logic-gates.md)
2. [Boolean algebra and circuits](02-boolean-algebra-and-circuits.md)
3. [The CPU](03-the-cpu.md)
4. [Memory hierarchy and latency numbers](04-memory-hierarchy-and-latency-numbers.md)
5. [Storage, I/O and buses](05-storage-io-and-buses.md)
6. [GPUs and parallel hardware](06-gpus-and-parallel-hardware.md) (optional)

## Key terms

| Term | Meaning |
|---|---|
| Transistor | A voltage-controlled switch; the building block of every chip |
| Logic gate | A small circuit that maps one or two input bits to one output bit |
| NAND | Output 0 only when both inputs are 1; universal, so any gate can be built from it |
| Full adder | Adds two bits and a carry-in; gives a sum bit and a carry-out |
| Latch, flip-flop | A feedback loop that holds one bit; a flip-flop changes only on a clock edge |
| Register | A row of flip-flops inside the CPU; the fastest storage |
| SRAM, DRAM | SRAM: about 6 transistors per bit, fast, used for caches. DRAM: 1 transistor and a capacitor per bit, dense, refreshed, used for main memory |
| Program counter | The register holding the address of the next instruction |
| Cycle, clock speed | One clock tick; ticks per second in GHz |
| Core, logical CPU | A core runs one instruction stream; SMT makes one core look like two logical CPUs |
| Cache hit, miss | Data was, or was not, in the cache |
| Latency, bandwidth | Time to the first byte; bytes per second once flowing |
| Interrupt, polling | The device signals the CPU; or the CPU asks the device repeatedly |
| DMA | A device reads or writes RAM itself, without the CPU copying each byte |
| PCIe lane | One two-way data path; links are x1, x4, x16 |
| SIMD | One instruction applied to several values at once |
| VRAM | A GPU's own memory |

## Truth tables

| Inputs (a b) | AND | OR | NAND | NOR | XOR |
|---|---|---|---|---|---|
| 0 0 | 0 | 0 | 1 | 1 | 0 |
| 0 1 | 0 | 1 | 1 | 0 | 1 |
| 1 0 | 0 | 1 | 1 | 0 | 1 |
| 1 1 | 1 | 1 | 0 | 0 | 0 |

## Formulas

De Morgan's laws:

$$\overline{a \cdot b} = \bar{a} + \bar{b} \qquad \overline{a + b} = \bar{a} \cdot \bar{b}$$

Full adder:

$$s = a \oplus b \oplus c_{in} \qquad c_{out} = ab + c_{in}(a \oplus b)$$

Weights in memory: parameters times bytes per parameter (7 billion parameters at 2 bytes each is 14 GB).

## The instruction cycle

Fetch the instruction at the program counter, decode it, execute it, write the result to a register, repeat. A jump loads a new address into the program counter.

## Numbers to remember (as of 2026)

| Item | Value | Where |
|---|---|---|
| One CPU cycle at 3 to 4 GHz | 0.25 to 0.33 ns | [The CPU](03-the-cpu.md) |
| Branch misprediction | about 10 to 20 cycles | [The CPU](03-the-cpu.md) |
| Random read: RAM, SSD, HDD | about 100 ns, 100 µs, 10 ms | [Latency numbers](04-memory-hierarchy-and-latency-numbers.md) |
| PCIe 3.0, 4.0, 5.0 per lane | 0.985, 1.97, 3.94 GB/s | [Storage, I/O and buses](05-storage-io-and-buses.md) |
| PCIe 4.0 x4, 5.0 x16 | 7.9 GB/s, 63 GB/s per direction | [Storage, I/O and buses](05-storage-io-and-buses.md) |
| Sequential read: HDD, SATA SSD, NVMe PCIe 5.0 | about 100 to 300 MB/s, 500 MB/s, up to 15,000 MB/s | [Storage, I/O and buses](05-storage-io-and-buses.md) |
| RTX 5090 | 32 GB GDDR7, 21,760 CUDA cores | [GPUs](06-gpus-and-parallel-hardware.md) |

## Rules of thumb

- Hardware computes with all gates at once; software runs one step after another.
- Clock speed alone does not rank CPUs. Compare benchmarks for your workload.
- More cores help only with independent work. In CPython, CPU-bound parallelism needs processes.
- Latency dominates many small requests, bandwidth dominates one large one.
- Sequential disk throughput is not what a random read sees.
- The OS caches file contents in RAM, so a second read of a file measures memory.
- A GPU needs large, regular, data-parallel work and data kept in VRAM.

## Code to remember

```python
import os
import tempfile
from multiprocessing import Pool

def square(n):
    return n * n

if __name__ == "__main__":              # required on Windows and macOS
    print(os.cpu_count() > 0)           # logical CPUs, not physical cores
    with Pool(2) as pool:
        print(pool.map(square, [1, 2, 3]))
    with tempfile.TemporaryFile() as f:
        f.write(b"data")
        f.flush()
        os.fsync(f.fileno())            # wait until the data reaches the device
        print("synced")
```

```text
True
[1, 4, 9]
synced
```
