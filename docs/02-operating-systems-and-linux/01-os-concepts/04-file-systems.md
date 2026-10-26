# File systems

After this you can explain what an inode is, tell a hard link from a soft link, read a path and a mount point, and say why Linux treats devices and processes as files.

Before this: [Memory and virtual memory](03-memory-and-virtual-memory.md) and [storage, I/O and buses](../../01-how-computers-work/02-hardware/05-storage-io-and-buses.md).

## The idea

A disk is a long run of numbered blocks that knows nothing about files or folders. Something has to turn "bytes at block 8,412,907" into "the file `report.txt` in `/home/you/docs`".

That something is a **file system**: a set of data structures on the disk, plus kernel code that reads them. It keeps the file's contents in blocks, keeps the file's facts (size, owner, permissions, times, where its blocks are) in a record, and keeps a directory structure that maps names to records.

```mermaid
flowchart LR
    D["Directory /docs<br/>report.txt -> inode 4821<br/>old.txt -> inode 4821"] --> I["Inode 4821<br/>size, owner, mode,<br/>link count 2, block list"]
    I --> B["Data blocks"]
```

The diagram holds the lesson's main surprise: a file's name is not stored with the file. It is an entry in a directory that points at an inode, and one inode can have many names.

## Key terms

An **inode** is the record the file system keeps for one file: its type, size, owner, permission bits, timestamps and the location of its data blocks. It is identified by a number (the inode number). It does not hold the file's name.

A **directory** is a special file that maps names to inode numbers. A **path** is a chain of directory names that leads to an inode: `/home/you/report.txt` starts at the root `/` and follows each name.

A **hard link** is an extra directory entry that points to an existing inode. All names for the inode are equal, and the inode keeps a **link count**. The data is freed only when the count reaches zero and no process still has the file open.

A **soft link** (symbolic link) is a small file whose contents are a path. The kernel follows that path when you open the link. If the target is removed, the link is left **dangling**.

To **mount** a file system is to attach it to a directory in the tree, called the mount point. Linux has one tree rooted at `/`; every disk, USB stick and network share appears somewhere under it. Windows instead gives each volume a drive letter such as `C:`.

## How it works

**ext4** is the default on many Linux distributions, including Ubuntu. **NTFS** is the Windows default, and APFS is the macOS default. They differ in details, but a few differences show up in everyday work:

| | ext4 (Linux) | NTFS (Windows) |
|---|---|---|
| Path separator | `/` | `\` (and `/` often works) |
| Top of the tree | one root `/` | one tree per drive letter |
| Case in names | `a.txt` and `A.txt` are different | same file by default (case-preserving) |
| Symbolic links | any user can make one | need a privilege or Developer Mode |

The case rule is a classic source of bugs: code written on a Mac or Windows laptop that opens `Config.json` works there and fails on a Linux server where the file is `config.json`.

### Everything is a file

Unix-style systems expose many things through the file interface: you open them, read, write and close them. Ordinary files and directories are the obvious case. Devices appear under `/dev` (`/dev/null` throws away what you write to it). Pipes and sockets are files too, which is why a shell can connect programs with `|`.

The **proc file system**, mounted at `/proc` on Linux, is the clearest case. It is a pseudo-file-system that provides an interface to kernel data structures ([proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html)). Nothing in it is stored on a disk. When you read `/proc/cpuinfo` the kernel generates the text on the spot, and `/proc/self` is a link to the directory of the process that reads it. The Linux tools `ps` and `top` get their data by reading `/proc`. macOS and Windows have no `/proc`.

<details class="code" markdown>
<summary>In code</summary>

Python reads inode numbers and link counts through `os.stat`. This runs on any OS; the script looks at its own file.

```python
import os

info = os.stat(__file__)
print("inode:", info.st_ino)
print("links:", info.st_nlink)
print("size: ", info.st_size, "bytes")
```

```text
inode: 1125899908118581
links: 1
size:  135 bytes
```

Windows reports a very large file ID where Linux reports a smaller number. Your values will differ.

</details>

## Worked examples

<div class="example" markdown>

### Example 1: one inode, two names

We make a file, add a second name for it with `os.link`, delete the first name, and check that the data survives. A soft link is attempted too; on Windows it can fail without a privilege.

```python
import os, tempfile

with tempfile.TemporaryDirectory() as d:
    a = os.path.join(d, "report.txt")
    b = os.path.join(d, "hard.txt")
    c = os.path.join(d, "soft.txt")
    with open(a, "w") as f:
        f.write("quarterly numbers\n")

    os.link(a, b)
    print("same inode:", os.stat(a).st_ino == os.stat(b).st_ino)
    print("link count:", os.stat(a).st_nlink)

    try:
        os.symlink(a, c)
        symlinks = True
    except OSError:
        symlinks = False
        print("symlink not allowed on this account")

    os.remove(a)
    print("hard link still reads:", open(b).read().strip())
    print("link count now:", os.stat(b).st_nlink)
    if symlinks:
        print("soft link target exists:", os.path.exists(c))
```

```text
same inode: True
link count: 2
symlink not allowed on this account
hard link still reads: quarterly numbers
link count now: 1
```

1. `os.link(a, b)` adds a second directory entry for the same inode. Both names report the same inode number and a link count of 2.
2. `os.remove(a)` removes one name and lowers the count to 1. The inode and its data stay, so reading through `hard.txt` still works.
3. A soft link behaves differently. On Linux the last line prints `soft link target exists: False`, because the name it points at is gone.

Check: on this Windows run the symlink step was refused. Run the same script in WSL to see the soft-link line (unverified here).

</div>

<div class="example" markdown>

### Example 2: following the mounts in WSL

In WSL (Ubuntu), unverified:

```bash
df -h /
findmnt /mnt/c
ls -li /etc/hostname
```

`df -h /` ([df(1)](https://manpages.ubuntu.com/manpages/noble/man1/df.1.html)) shows the file system holding `/` with its size and use. `findmnt /mnt/c` ([findmnt(8)](https://manpages.ubuntu.com/manpages/noble/man8/findmnt.8.html)) shows that your Windows `C:` drive is mounted at `/mnt/c`, with a different file system type from the root. `ls -li` puts the inode number in the first column, so you can compare names that share one.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: thinking `rm` erases a file. It removes one name and lowers the link count. The data is freed when no name and no open file remains. The same fact explains why a deleted log file can keep eating disk space while a process still holds it open.

Watch out: using a hard link where you need a soft link. Hard links cannot point to directories, and cannot cross file systems, because inode numbers are only unique inside one file system. Use a soft link for those.

Watch out: relative soft links. `ln -s ../data/file.txt link` stores that text, which is resolved from the link's own folder. Moving the link breaks it.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: inode, hard link, symbolic link, mount point, file system type, `/proc`, case sensitivity, link count. They make questions about disk space and "file not found" precise.

Prompts to try:

- "On Ubuntu 24.04, `df -h` says the disk is full but `du -sh /*` adds up to much less. Explain how deleted-but-open files and inode exhaustion cause this, and give the commands to check both."
- "My Next.js app works on macOS and fails on Linux with `Cannot find module './Header'` while the file is `header.js`. Explain what is happening."

What to check:

- Suggested `ln` arguments in the wrong order. The order is `ln -s TARGET LINK_NAME`; check with `man ln`.
- Advice that deletes a file as a way to free space while a process holds it open. Check with `lsof` that nothing has it open, or restart the process.
- Examples that assume `/proc` exists on macOS or inside a Windows terminal.

</div>

## Quiz

1\. What does a directory contain?

<details class="solution" markdown>
<summary>Answer</summary>

A table of names mapped to inode numbers. The file's size, permissions and data location are in the inode, not in the directory.

</details>

2\. A file has link count 3. You run `rm` on one of its names. What happens to the data?

<details class="solution" markdown>
<summary>Answer</summary>

Nothing is freed. The count drops to 2, and the other two names still reach the same inode and data.

</details>

3\. `ln -s notes.txt shortcut` is run in `/tmp`, but `notes.txt` is in `/home/you`. What happens when you `cat /tmp/shortcut`?

<details class="solution" markdown>
<summary>Answer</summary>

"No such file or directory". The soft link stores the text `notes.txt`, which is resolved from the link's own folder (`/tmp`), where no such file exists. Use `ln -s /home/you/notes.txt /tmp/shortcut`.

</details>

4\. Your Python script reads `/proc/cpuinfo` on Linux and works. Why would the same script fail on a Mac?

<details class="solution" markdown>
<summary>Answer</summary>

`/proc` is a Linux kernel feature. macOS has no such file system, so the path does not exist. Use a portable call such as `os.cpu_count()` or `platform`.

</details>

## Lab

<div class="lab" markdown>

### Lab: hard links, soft links and a mount

Goal: see an inode shared by two names, see a soft link dangle, and see what is mounted. Time: about 15 minutes. Runs in: Python on any OS; steps 3 to 5 use WSL (Ubuntu) and are unverified.

1. Run the script from Example 1. Confirm the inode check prints `True` and the link count goes from 2 to 1.
2. Change the script to write `"v2"` through the hard-link name with `open(b, "a")` before removing `a`, then read it back through `a`. Predict the result first.
3. In WSL, in `/tmp`: `echo hello > a.txt`, `ln a.txt hard.txt`, `ln -s a.txt soft.txt`, then `ls -li`. Find the two entries with the same inode number and the `->` on the soft link.
4. Run `rm a.txt`, then `cat hard.txt` and `cat soft.txt`. The first prints `hello`; the second reports that the file does not exist ([ln(1)](https://manpages.ubuntu.com/manpages/noble/man1/ln.1.html)).
5. Cleanup: `rm hard.txt soft.txt`. Then run `df -h` and `cat /proc/self/status | head -3` and find the mount for `/` and the process name.

Expected result: the hard link keeps working after step 4, and the soft link dangles.

<details class="solution" markdown>
<summary>Solution</summary>

Step 2: both names point at one inode, so a write through either shows up through the other. Steps 3 and 4 are the same demonstration with shell commands. `ls -li` shows the same inode on `a.txt` and `hard.txt`, with link count 2. `soft.txt` has its own inode, because it is a separate small file holding the text `a.txt`.

</details>

</div>

## Where this shows up

- The permission bits in the inode are the subject of [users, groups and permissions](../02-linux-command-line/03-users-groups-and-permissions.md); paths and `ls` are in [files and navigation](../02-linux-command-line/02-files-and-navigation.md).
- Docker images are stacks of file-system layers, which later lessons build on.
