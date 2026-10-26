# Code quality

Cheat sheet for the chapter. Lessons: [Unit testing](01-unit-testing.md), [Integration tests, mocks and end-to-end tests](02-integration-tests-mocks-and-e2e.md), [Linters, formatters and type checkers](03-linters-formatters-and-type-checkers.md), [Documentation and readmes](04-documentation-and-readmes.md).

## Key terms

| Term | Meaning |
|---|---|
| Unit test | Runs one function in isolation and checks its result |
| Arrange, act, assert | Set up input, call the code, compare the result |
| Fixture | Reusable test setup that a test receives by name |
| Parametrize | Run one test over a table of inputs |
| TDD | Red (failing test), green (least code to pass), refactor |
| Integration test | Real parts working together, such as code and a database |
| End-to-end test | Drives the whole app from outside, such as with a browser |
| Test double | Stand-in for a dependency: dummy, stub, fake, spy, mock |
| Flaky test | Passes and fails on the same code |
| Coverage | Share of lines or branches the tests executed |
| Linter | Static analysis for likely bugs and style problems |
| Formatter | Rewrites code into one fixed layout |
| Type checker | Checks values against annotations before running |
| Pre-commit hook | Script Git runs before a commit; failure refuses the commit |
| README, docstring, ADR, changelog | Front door, function docs, decision record, per-release changes |
| CLAUDE.md, AGENTS.md | Instruction files an AI agent loads at session start |

## Commands

| Task | Command |
|---|---|
| Run Python tests | `pytest -v` |
| Run one test | `pytest test_pricing.py::test_edges` |
| Coverage with missing lines | `pytest --cov=calc --cov-report=term-missing` |
| Run JavaScript tests | `npx vitest run` |
| Run an e2e test | `npx playwright test` |
| Python lint, with fixes | `ruff check --fix .` |
| Python format, or check only | `ruff format .`, `ruff format --check .` |
| Python types | `mypy .` |
| JavaScript lint, format check | `npx eslint .`, `npx prettier --check .` |
| TypeScript types | `npx tsc --noEmit` |
| Install the Git hook | `pre-commit install` |
| Run doctest examples | `python -m doctest pricing.py` |

## Rules

- Test typical input, edges (zero, one, empty, each side of a boundary) and errors.
- Assert on results, not on which helper was called.
- Patch a name where it is looked up (`rates.requests.get`), not where it is defined.
- Many unit tests, fewer integration tests, a handful of e2e tests.
- Coverage shows what was not tested, not what was tested well.
- Run formatter, linter, types and tests in the editor, in a pre-commit hook and in CI; CI is the one that cannot be skipped.
- Comments say why, docstrings say how to call, ADRs say why the design is this way.
- Keep CLAUDE.md or AGENTS.md short: commands, non-obvious rules, files not to touch.
- When an AI makes a failing check pass, read the diff of the tests and config first.
