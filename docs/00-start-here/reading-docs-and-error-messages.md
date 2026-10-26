# Reading docs and error messages

After this you can find the right kind of documentation for a question, read a Python or Node.js stack trace to the line that matters, recognize five common error shapes, and turn an error into a prompt an AI can answer.

Most of what you do as a developer is read: docs, code, and error output. An assistant can summarize all three, but it can also misread them, so you need to read them yourself first.

## The kinds of documentation

Documentation comes in several types, and the same project often has all of them. Picking the right type saves time.

A **reference** lists every function, flag and option, exactly and completely. It is for looking things up, not for learning. Examples: the [Python standard library reference](https://docs.python.org/3/library/), [MDN Web Docs](https://developer.mozilla.org/) for JavaScript and the web, and `man` pages.

A **tutorial** walks a beginner through one complete task, step by step. Use it when the topic is new. Its examples are chosen to teach, so they leave out error handling and edge cases.

A **guide** (also called a how-to or an explanation) covers one goal or concept in between: "how to deploy with X", "how caching works". Use it when you know the basics and need the approach.

When you have a specific question, start with the reference. When you have no map, start with the tutorial.

### Documentation built into your tools

Every command-line tool should explain itself:

```bash
ls --help
```

```text
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
```

That output is trimmed; the real list of options is long. Run `man ls` for the full manual page: press `/` to search, `n` for the next match and `q` to quit. In Python, `help(str.split)` prints the documentation of a function, and in a REPL `dir(obj)` lists its attributes. A flag your AI assistant suggests that appears in neither `--help` nor `man` is a reason to doubt it.

When you open a reference page, look for four things: the signature (what goes in), the return value, the exceptions or errors it can raise, and the version where it was added or changed. Version notes such as "Changed in version 3.x" tell you whether an answer written for an older version still applies.

## Reading a stack trace

A **stack trace** (a traceback in Python) is the list of function calls that were active when an error happened, from the program's entry point down to the line that failed. It answers "how did we get here?".

The error is the message plus the type: `ZeroDivisionError`, `TypeError`. The frames are the calls. Your job is to find the frame in your own code that is closest to the failure, because that is where you can fix something. Frames inside libraries are usually correct; the bug is more often in the arguments you passed.

### Python: read from the bottom

Python prints frames oldest first, so the last line is the error and the frame right above it is the failing line. Here is a small script, `parse_user.py`:

```python
import json

def read_name(text):
    user = json.loads(text)
    return user["name"]

print(read_name('{"name": "Ada"'))
```

Running `python3 parse_user.py` gives (paths shortened, and the `~~^^` marker lines removed):

```text
Traceback (most recent call last):
  File "/home/you/parse_user.py", line 7, in <module>
    print(read_name('{"name": "Ada"'))
  File "/home/you/parse_user.py", line 4, in read_name
    user = json.loads(text)
  File "/usr/lib/python3/json/__init__.py", line 352, in loads
    return _default_decoder.decode(s)
  File "/usr/lib/python3/json/decoder.py", line 345, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/usr/lib/python3/json/decoder.py", line 361, in raw_decode
    obj, end = self.scan_once(s, idx)
json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 15 (char 14)
```

1. Read the last line first: `JSONDecodeError`, with "line 1 column 15". The JSON text is malformed at its end.
2. Scan upward for the last frame in your own file: `parse_user.py`, line 4, `json.loads(text)`. The three `json/` frames below it are library internals.
3. Ask what you passed in. Line 7 passes a string with a missing closing brace. That is the bug.

Check: add the missing `}` to the string and run it; the script prints `Ada`.

### Node.js: the message first, then the newest frame

Node prints the error message first, then frames with the newest call at the top. For this `app.js`:

```javascript
function parse(text) {
  return JSON.parse(text);
}

function main() {
  const user = parse('{"name": "Ada"');
  console.log(user.name);
}

main();
```

Node v24 prints (paths shortened, later `node:internal` frames cut):

```text
SyntaxError: Expected ',' or '}' after property value in JSON at position 14 (line 1 column 15)
    at JSON.parse (<anonymous>)
    at parse (/home/you/app.js:2:15)
    at main (/home/you/app.js:6:16)
    at Object.<anonymous> (/home/you/app.js:10:1)
    at Module._compile (node:internal/modules/cjs/loader:1830:14)
```

Read it top-down. `JSON.parse (<anonymous>)` is built in. The first frame with your file name is `parse` at `app.js:2:15` (line 2, column 15); the next, `main` at line 6, shows who called it with the bad text. Frames starting `node:internal` are Node itself.

## Five common error shapes

These messages look different on each system, but each one has a short list of causes.

| Message | What it means | First thing to check |
|---|---|---|
| `bash: foo: command not found` | The shell found no program named `foo` on `PATH` | Typo? Installed? Right shell (PowerShell vs Ubuntu)? New terminal after install? |
| `Permission denied` | The operating system refused the action for your user | `ls -l` on the file; are you allowed to read or run it? Is a script missing execute permission? |
| `ModuleNotFoundError: No module named 'x'` | Python cannot import `x` | Is the virtual environment active? Was it `pip install`ed into that environment? Is the name spelled right? |
| `EADDRINUSE` or "address already in use" | Another process already listens on that port | Which process? Close it or choose another port |
| `ECONNREFUSED` or "connection refused" | Nothing is listening at that address and port | Is the server running? Right host and port? Inside Docker, is the port published? |

The last two are demonstrated by real runs. In Node:

```text
listen EADDRINUSE: address already in use :::3000
connect ECONNREFUSED 127.0.0.1:3999
```

In Python, a missing module:

```text
ModuleNotFoundError: No module named 'requests_nope'
```

Python's port errors are `OSError` subclasses; connecting to a closed port raises `ConnectionRefusedError`. The wording of the operating-system message differs (Windows prints `WinError 10061`; Linux prints `[Errno 111] Connection refused`). The Linux wording here is from standard behaviour, not from a run inside WSL.

Watch out: "command not found" and "No module named" often mean the right tool is installed in a different place than the one you are running. Check which one runs with `which python3` or `command -v node`.

## Searching for an error well

1. Copy the error line itself, without your file paths, usernames and numbers. Put it in quotes in the search box.
2. Add the tool and version (`python 3.12`, `node 24`, `postgres 16`), because answers from five years ago may no longer apply.
3. Prefer official docs, the project's issue tracker and answers that quote the same error text. A forum answer for a similar but different message is a common trap.
4. Read the date. An old answer that works may still give you a deprecated approach.

## Turning an error into a prompt

A good prompt has five parts: what you are trying to do, your environment, the exact error, the smallest code that causes it, and what you already tried.

```text
Goal: read scores.json and print the average score.
Environment: Ubuntu 24.04 on WSL2, Python 3.12.
Error (full traceback below):
  ZeroDivisionError: division by zero, at average() line 4.
Code: (paste the 10 lines)
Tried: printed `scores`; it is an empty list.
Question: why is the list empty, and how should average() handle that case?
Please explain the cause first, then show the fix.
```

Remove secrets and real data before you paste. Then check the answer as in [Learning tech with AI](learning-tech-with-ai.md): does the explanation match the traceback, and does the fix pass when you run it?

## Try it

<div class="lab" markdown>

### Lab: fix a broken script

Goal: find and fix the bug using only the traceback. Time: about 10 minutes. Runs in: Ubuntu.

1. Save this as `broken.py` in a folder under `~/projects`:

    ```python
    import json

    def average(scores):
        return sum(scores) / len(scores)

    def load(text):
        return json.loads(text)

    data = load('{"scores": []}')
    print(average(data["scores"]))
    ```

2. Run `python3 broken.py`.
3. Write down: the error type, the last frame in your own code, and which line called it.
4. Decide what `average` should do for an empty list, and change it.
5. Run it again. Then change the data to `{"scores": [80, 90]}` and confirm that it prints `85.0`.

Expected result: before the fix, the last lines are as shown below.

```text
  File "/home/you/broken.py", line 10, in <module>
    print(average(data["scores"]))
  File "/home/you/broken.py", line 4, in average
    return sum(scores) / len(scores)
ZeroDivisionError: division by zero
```

<details class="solution" markdown>
<summary>Solution</summary>

The error is `ZeroDivisionError`. The last frame in your code is `average`, line 4, called from line 10. The list is empty, so `len(scores)` is 0. The program cannot compute an average of nothing, so decide what to return. One choice is `None`:

```python
import json

def average(scores):
    if not scores:
        return None
    return sum(scores) / len(scores)

def load(text):
    return json.loads(text)

data = load('{"scores": []}')
print(average(data["scores"]))
```

```text
None
```

With `{"scores": [80, 90]}` it prints `85.0`. Raising a `ValueError` with a clear message is also fine, and better if callers must not carry on without a result.

</details>

</div>

## Working with AI

<div class="ai" markdown>

### Working with AI

Words to use: stack trace, traceback, frame, exception, exit code, `PATH`, reproducible example, regression.

Prompts to try:

- "Here is a Python traceback. Which frame is in my code, and which are library frames? Tell me the line to look at first: (paste)."
- "Explain what `EADDRINUSE` means in Node.js, then give me the Ubuntu command to find which process uses port 3000."

What to check:

- The explanation refers to a line that exists in your trace. If it names a function you do not have, it is guessing.
- Commands it gives exist: run `--help` first.
- A fix that only hides the error (a bare `except:` that ignores everything) is not a fix. Ask what the underlying cause is.

</div>

## Where this shows up

- Python errors in depth: [errors and exceptions](../03-programming-fundamentals/01-python-basics/06-errors-and-exceptions.md) and [reading code and debugging](../03-programming-fundamentals/02-thinking-like-a-programmer/04-reading-code-and-debugging.md).
- Ports and connection errors: [ports and sockets](../07-networking/01-how-the-internet-works/04-ports-and-sockets.md).
