# Secrets and dependency security

After this you can keep secrets out of your code and git history, audit a project's dependencies, and explain how a supply-chain attack reaches your app.

Before this: [Secure authentication](05-secure-authentication.md) and [Git basics](../../06-developer-tools-and-workflow/01-editor-and-git/02-git-basics.md).

## The idea

A typical app has 20 direct dependencies and a few hundred indirect ones, and holds a dozen secrets: a database password, a payment API key, a signing key. Two of the most common ways to be breached have nothing to do with your own logic. A key gets pushed to a public repository, or a package you install, directly or three levels down, turns out to be malicious or vulnerable.

You protect secrets by keeping them out of places that copy easily (source code, git history, logs, images) and by making them cheap to replace. You protect against dependencies by knowing what you run, pinning it, and scanning it. In the diagram, an app depends on packages, which depend on others, and one of those has been poisoned.

```mermaid
flowchart TD
    APP["Your app"] --> EXP["express"]
    APP --> LOG["fancy-logger"]
    APP --> UTIL["date-utils"]
    EXP --> BP["body-parser"]
    LOG --> COL["colour-helper"]
    COL --> BAD["left-padd<br/>(typosquat of left-pad,<br/>steals env vars on install)"]
    UTIL --> SMALL["small-helper"]
    style BAD fill:#fdd,stroke:#c00
```

Your code never mentions `left-padd`. It runs on every machine that installs the app, with that machine's environment variables and file access.

## Key terms

A **secret** is a value that grants access and must stay private: passwords, API keys, tokens, private keys. A **secrets manager** (AWS Secrets Manager, HashiCorp Vault, a cloud provider's equivalent) stores them encrypted, controls who can read them and logs access. An **environment variable** is a named value the operating system gives a process at start.

A **lockfile** (`package-lock.json`, `poetry.lock`, `uv.lock`) records the exact version and checksum of every dependency, direct and indirect, so every install gets the same code.

A **software supply-chain attack** compromises something you depend on instead of attacking you directly. **Typosquatting** publishes a package with a name close to a popular one. A **software bill of materials (SBOM)** is a machine-readable inventory of every component in a build, so you can answer "are we affected?" when a new vulnerability is announced.

## How it works

Secrets ([OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)):

1. Read secrets from the environment or a secrets manager at runtime, never from source files. Local development uses a `.env` file listed in `.gitignore`.
2. Commit a `.env.example` with fake values, so others know which variables exist.
3. Turn on secret scanning: GitHub's push protection blocks pushes that contain known key formats, and tools such as gitleaks scan history.
4. Assume a pushed secret is public forever. Deleting the commit does not help, since bots scrape new commits within minutes. Revoke and rotate the key first, then clean up.
5. Rotate regularly and use short-lived credentials (for example, temporary tokens from a cloud role) so a leak expires.
6. Give each key the least privilege: a read-only key for a read-only job.

Dependencies:

1. Commit the lockfile, and install from it in CI (`npm ci`, `pip install -r requirements.txt` with hashes, or `uv sync --locked`).
2. Audit regularly: `npm audit` or `pip-audit`. Add Dependabot or a similar bot to open update pull requests.
3. Be careful adding a package: check its name, download count, maintainers and last release. Prefer fewer dependencies.
4. Treat install scripts as code execution. Do not run `npm install` from untrusted sources on a machine with real credentials.
5. Generate an SBOM (CycloneDX or SPDX format) in CI and keep it with each release.

## Worked examples

<div class="example" markdown>

### Example 1: reading a secret from the environment

The script `sec.py` fails fast when the variable is missing:

```python
import os

API_KEY = os.environ.get("PAYMENTS_API_KEY")
if API_KEY is None:
    raise SystemExit("PAYMENTS_API_KEY is not set")
print("key loaded, length", len(API_KEY))
```

In a shell where the variable is unset, then set for one command:

```bash
python sec.py
PAYMENTS_API_KEY=sk_test_demo python sec.py
```

```text
PAYMENTS_API_KEY is not set
key loaded, length 12
```

The program prints the length and not the value. Logging a secret copies it into log files, which are rarely protected as well as the secret itself. The `PAYMENTS_API_KEY=value command` form is for POSIX shells; in PowerShell set `$env:PAYMENTS_API_KEY = "sk_test_demo"` first.

Check: run it without the variable and confirm the message appears and nothing crashes with a stack trace.

</div>

<div class="example" markdown>

### Example 2: auditing dependencies

We install an old version of `lodash` into a throwaway folder and audit it:

```bash
npm install lodash@4.17.15
npm audit
```

```text
# npm audit report

lodash  <=4.17.23
Severity: high
Command Injection in lodash - https://github.com/advisories/GHSA-35jh-r3h4-6jhm
Prototype Pollution in lodash - https://github.com/advisories/GHSA-p6mc-m468-83gw
...
fix available via `npm audit fix`
node_modules/lodash

1 high severity vulnerability
```

Output is trimmed to the first rows, and the advisory list will differ when you run it, because the data changes. The Python equivalent, with `pip-audit` 2.10.1 and a requirements file containing `requests==2.25.0`:

```bash
pip-audit -r requirements.txt --no-deps --disable-pip
```

```text
Name     Version ID              Fix Versions
-------- ------- --------------- ------------
requests 2.25.0  PYSEC-2023-74   2.31.0
requests 2.25.0  PYSEC-2026-1873 2.32.0
requests 2.25.0  PYSEC-2026-1872 2.32.4
```

(`--no-deps --disable-pip` is for a requirements file with exact versions; normally you run `pip-audit` inside your project's environment.) Each row names the advisory and the first fixed version.

Check: after `npm audit fix` or after raising the version, the same command reports no known vulnerabilities, or lists only those with no fix yet.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: committing `.env` "just this once", or putting keys in front-end code. Anything shipped to a browser is public, and git history is permanent. Rotate the key.

Watch out: ignoring audit output because "it is only a dev dependency" or because there are 40 warnings. Sort by severity and whether the vulnerable code path is reachable, then fix the top items.

Watch out: using a version range like `^1.2.0` with no lockfile in CI. The build on Friday can differ from Thursday's.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: secrets manager, rotation, lockfile, typosquatting, supply chain, `npm audit`, SBOM, least privilege.

Prompts to try:

- "Here is my `docker-compose.yml` and `.github/workflows/ci.yml`. List every secret in them, say which are hard-coded, and show how to read each from environment variables or GitHub Actions secrets."
- "Explain these `pip-audit` results, and tell me which fix versions are safe upgrades with my pinned Django 4.2."

What to check:

- Packages that AI suggests and do not exist, or have names close to real ones (package hallucination is exploitable by typosquatters). Look each one up on npm or PyPI before installing.
- Example code with a key written inline, which you may paste and commit. Search the diff for `KEY`, `SECRET`, `TOKEN` before committing.
- An upgrade that jumps a major version, which can break your code. Read the changelog and run the tests.

</div>

## Quiz

1\. You pushed an AWS key to a public repo and removed it in the next commit. Is it safe?

<details class="solution" markdown>
<summary>Answer</summary>

No. It remains in history and bots find it quickly. Revoke and rotate the key first, then consider cleaning history.

</details>

2\. What does a lockfile give you that `package.json` does not?

<details class="solution" markdown>
<summary>Answer</summary>

Exact versions and checksums of all dependencies, including indirect ones, so installs are reproducible and a tampered package fails the checksum.

</details>

3\. A teammate adds `reqeusts` to `requirements.txt` (a typo). What attack does this resemble?

<details class="solution" markdown>
<summary>Answer</summary>

Typosquatting. An attacker can publish a package under a mistyped name and run code on install. Check the name against the real project.

</details>

4\. Why is "short-lived credentials" a better defence than "never leak the key"?

<details class="solution" markdown>
<summary>Answer</summary>

Leaks happen. A credential that expires in an hour limits what a leak is worth, so the defence does not depend on perfection.

</details>

## Lab

<div class="lab" markdown>

### Lab: scan, audit, fix

Goal: find a planted secret and a vulnerable package in a throwaway project. Time: about 15 minutes. Runs in: any terminal with Node.

1. Create a folder with `npm init -y` and `npm install lodash@4.17.15`.
2. Add a file `config.js` containing `const key = "AKIAIOSFODNN7EXAMPLE";` (AWS's documented fake key).
3. Run `npm audit` and note the severity. Then run a scan for the key with `grep -rnE "AKIA[0-9A-Z]{16}" --include=*.js --exclude-dir=node_modules .`.
4. Move the key to an environment variable, add `.env` to `.gitignore`, and run `npm install lodash@latest`, then `npm audit` again.
5. Cleanup: delete the folder.

Expected result: audit reports a high severity first, then none after upgrading; the grep finds `config.js:1` first and nothing after the fix.

<details class="solution" markdown>
<summary>Solution</summary>

`config.js` becomes `const key = process.env.AWS_KEY_ID;`. A short Python scan of the same pattern (`AKIA[0-9A-Z]{16}`) printed `line 1: possible AWS access key id` for the original text. Real scanners such as gitleaks use many such patterns plus entropy checks.

</details>

</div>

## Where this shows up

- Docker builds and CI pipelines in [DevOps and cloud](../../13-devops-and-cloud/index.md) are where secrets leak into images and logs.
- AI security risks<!-- link: ../../15-ai-and-llms/03-ai-assisted-development/04-ai-security-risks.md --> covers package hallucination and prompt injection.
