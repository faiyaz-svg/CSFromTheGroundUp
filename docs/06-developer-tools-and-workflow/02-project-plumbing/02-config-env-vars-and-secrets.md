# Config, environment variables and secrets

After this you can keep settings and passwords out of your code, load them from the environment in Python and Node, and know what to do when a key leaks.

Before this: [Package managers and dependencies](01-package-managers-and-dependencies.md) and Environment variables and path<!-- link: ../../02-operating-systems-and-linux/02-linux-command-line/08-environment-variables-and-path.md -->.

## The idea

Your app connects to a database. On your laptop that is `localhost`; in production it is a different server with a different password. If the address and password are typed into the code, you must edit the code for each place it runs, and the password is now in your Git history for anyone with repository access.

The fix is to treat these values as **config**: everything likely to vary between deploys (developer machine, staging, production). The Twelve-Factor App, a widely used guide to building deployable apps, says to keep config strictly separate from code and store it in environment variables ([12factor.net/config](https://12factor.net/config)). Its test is whether the codebase could be made open source at any moment without leaking a credential.

```mermaid
flowchart LR
    CODE["code<br/>(same everywhere)"] --> APP["running app"]
    ENV1["developer: .env file"] --> APP
    ENV2["production: set by the host"] --> APP
    APP --> DB[("database")]
```

In the diagram, the code is identical in both places; only the environment around it changes.

## Key terms

An **environment variable** is a named string that the operating system gives to every process it starts. A program reads it by name and gets text back, always text, even when it looks like a number.

A **secret** is config that grants access if someone else reads it: passwords, API keys, tokens, private keys. A **`.env` file** is a plain text file of `NAME=value` lines, read by a library or by Node itself, used on developer machines.

**Rotating** a secret means issuing a new one and revoking the old one.

## How it works

A process receives a copy of its parent's environment when it starts. You can add a variable for one command, or for the rest of the shell session:

```bash
PORT=9000 node app.js
export PORT=9000
```

In PowerShell the same two steps are `$env:PORT = "9000"; node app.js`, and the variable lasts for that session.

Python reads the environment through `os.environ`, a dictionary of strings. Node uses `process.env`. Both give you text, so convert numbers and booleans yourself. A missing variable is `None` or `undefined` unless you index with `os.environ["NAME"]`, which raises `KeyError`. For a required secret that failure is what you want: the app stops at start-up with a clear message instead of failing later with a confusing one.

A `.env` file saves you from typing variables on every run:

```text
DATABASE_URL=postgres://app:s3cret@localhost:5432/shop
PORT=3000
DEBUG=false
```

Python needs the `python-dotenv` package (`pip install python-dotenv`) and a call to `load_dotenv()`, which by default does not replace a variable that is already set in the real environment ([python-dotenv reference](https://saurabh-kumar.com/python-dotenv/reference/)). Node 20.6 and later can read the file itself: `node --env-file=.env app.js`. As of 2026, `--env-file` is no longer experimental in Node 24, a missing file is an error, and `--env-file-if-exists` ignores a missing file ([Node.js CLI docs](https://nodejs.org/api/cli.html)). Both tools let the real environment win, which is how production overrides your file.

Secrets need extra care, because a leaked secret is out of your control once it is copied. Three rules:

1. Keep `.env` in `.gitignore` before the first commit, and commit a `.env.example` with the variable names and no real values, so a new teammate knows what to set.
2. Never print secrets in logs or error messages, and never put them in front-end code, which every visitor can read.
3. If a secret is committed or pasted anywhere public, assume it is compromised. Rotate it first. Removing the file from the next commit does not help, because the old commit still contains it.

```mermaid
flowchart TD
    A["Secret leaked"] --> B["1. Revoke it at the provider<br/>and issue a new one"]
    B --> C["2. Put the new one in the secret store<br/>or .env, not in code"]
    C --> D["3. Check the provider's logs<br/>for use you did not make"]
    D --> E["4. Clean the repository history<br/>(optional, after rotating)"]
```

In production, a `.env` file on the server is the weakest option. A **secret manager** (AWS Secrets Manager, or the secrets feature of GitHub Actions and your hosting platform) stores the values encrypted, controls who can read them and injects them as environment variables when the app starts. The security chapter returns to this in secrets and dependency security<!-- link: ../../12-security/01-web-security/06-secrets-and-dependency-security.md -->.

## Worked examples

<div class="example" markdown>

### Example 1: one script, three sources of config

The `.env` file above sits next to `app.py`, which reads three settings.

```python
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env; real environment variables win
port = int(os.environ.get("PORT", "8000"))
debug = os.environ.get("DEBUG", "false").lower() == "true"
db_url = os.environ["DATABASE_URL"]  # KeyError if missing: fail fast
print(port, debug, db_url.split("@")[-1])
```

1. `PORT` has a default of `"8000"`, converted with `int`.
2. `DEBUG` is text, so we compare it to `"true"`. `bool("false")` would be `True`, because any non-empty string is truthy.
3. `DATABASE_URL` has no default. The script prints only the part after `@`, so the password never reaches the log.

```bash
python app.py
PORT=9000 python app.py
```

```text
3000 False localhost:5432/shop
9000 False localhost:5432/shop
```

The first run takes `3000` from the file. The second shows the real environment winning. The Node version (`node --env-file=.env app.js`, reading `process.env.PORT` and so on) printed `3000 false ...` and `9000 false ...`, and without the flag it threw `Error: DATABASE_URL is not set`.

Check: delete `DATABASE_URL` from `.env` and rerun; Python should stop with `KeyError: 'DATABASE_URL'`.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: committing `.env` "just this once". The commit stays in history even after you delete the file. Add `.env` to `.gitignore` first; `git check-ignore -v .env` confirms the rule is working.

Watch out: reading `DEBUG=false` as a boolean. Environment variables are strings, so `if os.environ["DEBUG"]:` is true for `"false"`. Compare the text.

Watch out: putting an API key in browser JavaScript, including variables that a bundler copies into the front-end build. Anything shipped to the browser is public. Keep the key on a server and have the browser call your server.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: environment variable, `.env`, `.env.example`, `.gitignore`, secret manager, rotate a key, fail fast.

Prompts to try:

- "My Node 24 app reads `process.env.PORT` but I get `undefined` when I run `node server.js`. I have a `.env` file in the project root. Explain how to load it without installing a package, and what the precedence is if `PORT` is already set in my shell."
- "Review this Python settings module for secrets handling (paste it). List every place a secret could end up in a log, a traceback or a Git commit."

What to check:

- Example code that hard-codes a placeholder key. Real keys pasted into a prompt also leave your machine; paste variable names, not values.
- Missing `.env` in the `.gitignore` it generates. Run `git status` before your first commit.
- Numbers and booleans used straight from the environment without conversion.
- Advice to "just delete the commit". If the key was pushed, rotating it is the real fix.

</div>

## Quiz

1\. Why does the Twelve-Factor guide say to keep config out of the code?

<details class="solution" markdown>
<summary>Answer</summary>

Config differs between deploys while code stays the same, and credentials in code leak with the repository. Reading config from the environment lets one build run everywhere.

</details>

2\. What does this print if `DEBUG=false` is set?

```python
import os
if os.environ["DEBUG"]:
    print("debug on")
else:
    print("debug off")
```

<details class="solution" markdown>
<summary>Answer</summary>

`debug on`. The value is the string `"false"`, which is non-empty and therefore truthy. Compare with `== "true"` instead.

</details>

3\. You pushed a commit containing a cloud API key, then force-pushed a version without it. Is the key safe?

<details class="solution" markdown>
<summary>Answer</summary>

No. It may already have been copied or scanned, and old commits can stay reachable. Revoke the key at the provider and issue a new one, then check the provider's logs for use you did not make.

</details>

4\. `node --env-file=.env app.js` fails with a "not found" error on a teammate's machine, which has no `.env`. What are two ways to handle it?

<details class="solution" markdown>
<summary>Answer</summary>

They copy `.env.example` to `.env` and fill it in, or you start the app with `--env-file-if-exists=.env` so a missing file is allowed. For required secrets, the first is better, because the app then fails with a clear message about the missing variable.

</details>

## Lab

<div class="lab" markdown>

### Lab: load, override and protect config

Goal: read settings from a `.env` file, override one from the shell and prove Git ignores the file. Time: about 10 minutes. Runs in: any terminal with Node 24 and Git.

1. Make a folder and run `git init`. Create `.env` containing `PORT=3000` and `API_KEY=abc123`.
2. Create `app.js` that prints `process.env.PORT` and the first three characters of `process.env.API_KEY`, and throws if `API_KEY` is missing.
3. Run `node --env-file=.env app.js`, then set `PORT=9000` for one run and compare.
4. Run `git status`. If `.env` is listed, add it to `.gitignore`, then use `git check-ignore -v .env`.
5. Create `.env.example` with the names only, and commit nothing else.
6. Cleanup: delete the folder.

Expected result: `3000 abc`, then `9000 abc`, and `.env` ignored with the rule printed.

<details class="solution" markdown>
<summary>Solution</summary>

```javascript
if (!process.env.API_KEY) throw new Error("API_KEY is not set");
console.log(process.env.PORT, process.env.API_KEY.slice(0, 3));
```

```bash
node --env-file=.env app.js
PORT=9000 node --env-file=.env app.js
printf '.env\n' > .gitignore
git check-ignore -v .env
```

```text
.gitignore:1:.env	.env
```

In PowerShell, set the override with `$env:PORT = "9000"` first.

</details>

</div>

## Where this shows up

- Pipelines pass secrets as protected variables in GitHub Actions<!-- link: ../../13-devops-and-cloud/02-ci-cd/02-github-actions.md -->, and containers receive them through Compose<!-- link: ../../13-devops-and-cloud/01-containers/03-volumes-networks-and-compose.md -->.
- Every back-end project starts with a settings module, as in [what a back end does](../../09-back-end/01-servers-and-apis/01-what-a-back-end-does.md).
