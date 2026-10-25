# From code to running program

The path from source text to a running program, and the vocabulary for talking about it. Each section links the lesson that teaches it.

## Machine code and assembly

Lesson: [Machine code and assembly](01-machine-code-and-assembly.md).

| Term | Meaning |
|---|---|
| ISA | The instructions, registers and encodings a CPU family understands (x86-64, ARM64) |
| Machine code | The bytes the CPU executes |
| Assembly | Machine code as text: a mnemonic and operands per line |
| Register | A named storage slot inside the CPU (`rax`, `edi`) |
| Calling convention | Where arguments and the result live; System V x86-64: `rdi`, `rsi`, result in `eax`; Windows: `rcx`, `rdx` |
| `-O0`, `-O2` | Compiler optimization levels: literal translation, or rewritten for speed |

Commands (GCC; Clang takes the same flags):

```bash
gcc -S -O0 -masm=intel -o - add.c
gcc -S -O2 -masm=intel -o - add.c
```

Rules:

- Intel syntax writes the destination first; AT&T writes it last.
- Assembly is tied to one ISA and one operating system.
- `exec format error` on Linux means the binary was built for another ISA.

## Compilers, interpreters and JIT

Lesson: [Compilers, interpreters and JIT](02-compilers-interpreters-and-jit.md).

| Stage or term | Meaning |
|---|---|
| Token | Smallest piece of source text: a name, number or operator |
| AST | Tree of how the tokens nest, built by the parser |
| Bytecode | Compact instructions for a virtual machine, not a real CPU |
| AOT | Compile to machine code before running (C, Rust, Go) |
| JIT | Compile hot code to machine code while running (V8, JVM) |
| Transpiler | Translates one high-level language to another (TypeScript to JavaScript) |

| Language | Typical path |
|---|---|
| C, Rust, Go | Source, tokens, AST, machine code (AOT) |
| Python (CPython) | Source, AST, bytecode, interpreter; experimental JIT off by default |
| JavaScript (V8) | Source, AST, Ignition bytecode, then Sparkplug, Maglev, TurboFan |
| TypeScript | Types removed (`tsc` or Node type stripping), then the JavaScript path |

Commands:

```bash
python -c "import dis; dis.dis(lambda x: x * 2)"
node --print-bytecode --print-bytecode-filter=sumMod7 hot.js
npx tsc --noEmit file.ts
```

Rules:

- "Compiled" and "interpreted" describe an implementation, not a language.
- Python bytecode can change between versions, so run `dis` on your version.
- Benchmark JIT code with several runs and a used result.
- `node file.ts` strips types without checking them; run `tsc --noEmit` for type errors.
