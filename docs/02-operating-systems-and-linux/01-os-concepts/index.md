# Operating system concepts

A compact reference for the chapter. The lessons teach the ideas; this page is for looking things up.

## Lessons

1. [What an OS and kernel do](01-what-an-os-and-kernel-do.md)
2. [Processes, threads and scheduling](02-processes-threads-and-scheduling.md)
3. [Memory and virtual memory](03-memory-and-virtual-memory.md)
4. [File systems](04-file-systems.md)
5. [System calls and kernel mode](05-system-calls-and-kernel-mode.md)

## Key terms

| Term | Meaning |
|---|---|
| Kernel | Core of the OS; the only code with full hardware access |
| User space / kernel space | Restricted mode for programs / privileged mode for the kernel |
| Driver | Kernel code that talks to one kind of device |
| Distribution | Linux kernel plus tools, libraries and a package manager (Ubuntu, Debian, Fedora) |
| Process | A running program with its own address space; named by a PID |
| Thread | A line of execution inside a process; shares the process's memory |
| Context switch | The kernel pausing one thread and starting another |
| Concurrency / parallelism | Tasks in progress together / tasks running at the same instant |
| Virtual memory | Per-process addresses translated to RAM by the MMU |
| Page / page fault | 4 KiB chunk of memory (usual size) / first touch of a page with no RAM behind it |
| Swap | Disk space used as overflow for unused pages |
| OOM killer | Linux ends a process when RAM and swap run out (often exit code 137) |
| Stack / heap | Per-call locals, small and automatic / long-lived data, large and managed |
| Inode | File-system record: size, owner, mode, times, block locations (no name) |
| Hard link / soft link | Another name for the same inode / a small file holding a path |
| Mount | Attaching a file system to a directory in the tree |
| System call | A request from a program to the kernel through a mode-switching instruction |
| File descriptor | Small integer naming an open file, socket or pipe (0, 1, 2 are stdin, stdout, stderr) |

## The layers

```text
programs  ->  libraries / runtimes  ->  system calls  ->  kernel  ->  hardware
```

## Process, thread, or neither

| Task type | Python tool | Why |
|---|---|---|
| CPU-bound (computing) | processes (`multiprocessing`, `ProcessPoolExecutor`) | Each process has its own GIL |
| I/O-bound (waiting) | threads (`ThreadPoolExecutor`) or `asyncio` | The GIL is released while waiting |

Wrap multiprocessing start-up code in `if __name__ == "__main__":`.

## Thread states

Ready (can run), running (on a core), blocked (waiting for I/O). The scheduler moves threads between them; a blocked thread uses no CPU.

## Memory rules of thumb

- Virtual size is address space reserved; RSS is RAM in use. Read `available`, not `free`.
- `RecursionError` is the stack limit; a growing heap ends in the OOM killer.
- Exit code 137 means `SIGKILL` (128 + 9), often the OOM killer.

## Files and links

| Command (Linux) | What it does |
|---|---|
| `ls -li` | Show inode numbers and link counts |
| `ln TARGET NAME` | Hard link |
| `ln -s TARGET NAME` | Soft link; a relative TARGET is read from the link's folder |
| `df -h` | Space used per mounted file system |
| `findmnt` | Show mounts |
| `cat /proc/self/status` | Process facts straight from the kernel |

Case: ext4 treats `a.txt` and `A.txt` as different files; NTFS and the default macOS volume do not.

## System-call tools

| Command | What it does |
|---|---|
| `strace CMD` | Print each system call CMD makes |
| `strace -e trace=openat,read,write CMD` | Only those calls |
| `strace -c CMD` | Summary of calls, errors and time |
| `strace -f CMD` | Follow child processes |
| `strace -p PID` | Attach to a running process |

Common errors in a trace: `ENOENT` (no such path), `EACCES` (permission denied). `strace` is Linux-only.

## Python on any OS

`platform.system()`, `os.cpu_count()`, `os.getpid()`, `os.stat(path).st_ino`, `os.link`, `mmap.PAGESIZE`, `sys.getrecursionlimit()`.
