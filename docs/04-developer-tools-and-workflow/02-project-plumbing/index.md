# Project plumbing

A cheat sheet for the files and formats that every project depends on. Each lesson has the explanations.

## Lessons

1. [Package managers and dependencies](01-package-managers-and-dependencies.md)
2. [Config, environment variables and secrets](02-config-env-vars-and-secrets.md)
3. [Data formats: JSON, YAML and CSV](03-data-formats-json-yaml-csv.md)
4. [Regular expressions](04-regular-expressions.md)

## Key terms

| Term | Meaning |
|---|---|
| direct / transitive dependency | a package you list / a package pulled in by another package |
| lockfile | exact versions of the whole tree (`package-lock.json`, `uv.lock`) |
| semver | `MAJOR.MINOR.PATCH`; major may break, minor adds, patch fixes |
| environment variable | named string a process inherits from its parent |
| secret | config that grants access if read by someone else |
| rotate | issue a new secret and revoke the old one |
| schema | description of the shape and types data must have |
| capture group | `( ... )` part of a regex whose matched text you can reuse |
| greedy / lazy | takes as much / as little text as possible |

## Dependencies

| Task | npm | Python (uv) | Python (pip) |
|---|---|---|---|
| Add a package | `npm install pkg` | `uv add pkg` | `python -m pip install pkg` |
| Add a dev tool | `npm install --save-dev pkg` | `uv add --dev pkg` | a separate requirements file |
| Rebuild exactly | `npm ci` | `uv sync` | `python -m pip install -r requirements.txt` |
| Show the tree | `npm ls --all` | `uv tree` | `python -m pip freeze` (flat list) |
| Run a tool | `npx tool` | `uv run tool` | `python -m tool` |

| Range | Allows |
|---|---|
| `1.2.3` | that version only |
| `~1.2.3` | `1.2.x`, from `1.2.3` up |
| `^1.2.3` | `1.x.y`, from `1.2.3` up |
| `^0.2.3` | `0.2.x`, from `0.2.3` up |

Commit the manifest (`package.json`, `pyproject.toml`) and the lockfile. Never commit `node_modules` or `.venv`.

## Config and secrets

```bash
PORT=9000 node app.js
node --env-file=.env app.js
node --env-file-if-exists=.env app.js
```

```python
import os
os.environ["DATABASE_URL"]            # KeyError if missing
int(os.environ.get("PORT", "8000"))   # values are strings first
```

Rules: `.env` goes in `.gitignore`; `.env.example` is committed with no values; compare booleans as text; if a secret leaks, revoke and replace it before anything else.

## Formats

| | JSON | YAML | CSV |
|---|---|---|---|
| Comments | no | `#` | no |
| Types | string, number, boolean, null | guessed | all text |
| Python | `json.loads`, `json.dumps` | `yaml.safe_load` (PyYAML) | `csv.DictReader` |
| JavaScript | `JSON.parse`, `JSON.stringify` | `YAML.parse` (`yaml` package) | PapaParse |

YAML 1.1 turns `NO` into `False` and `01234` into 668, so quote ambiguous values. CSV quotes fields that hold commas, quotes or line breaks, and doubles inner quotes. Open CSV files with `newline=""` and the right encoding (`utf-8-sig` for an Excel BOM).

## Regex

| Syntax | Meaning |
|---|---|
| `\d` `\w` `\s` | digit, word character, whitespace |
| `[abc]` `[^abc]` | one of / none of |
| `*` `+` `?` `{n,m}` | repeat counts; add `?` for lazy |
| `^` `$` `\b` | start, end, word boundary |
| `(x)` `(?:x)` | capture, no capture |
| `x\|y` | alternation |

| Task | Python | JavaScript |
|---|---|---|
| First match | `re.search(p, s)` | `s.match(/p/)` |
| Whole string | `re.fullmatch(p, s)` | `/^p$/.test(s)` |
| All matches | `re.findall(p, s)` | `s.matchAll(/p/g)` |
| Replace | `re.sub(p, r"\1", s)` | `s.replace(/p/g, "$1")` |

On the command line, `grep -E "pattern" file` searches with a regex, and `-o` prints only the match. Do not use a regex for HTML or full email validation, and avoid nested quantifiers.
