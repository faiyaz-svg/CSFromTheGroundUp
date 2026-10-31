# Testing in depth

Cheat sheet for the chapter. Lessons: [TDD and test strategy](01-tdd-and-test-strategy.md), [Property-based testing, fuzzing and mutation testing](02-property-based-testing-fuzzing-and-mutation-testing.md).

## Key terms

| Term | Meaning |
|---|---|
| Red-green-refactor | Failing test, least code to pass, clean up with the tests green |
| Test pyramid | Many unit tests, fewer integration tests, a handful of end-to-end tests |
| Testing trophy | Integration tests as the biggest layer, static checks as the base |
| Line coverage | Share of lines that ran during the tests |
| Branch coverage | Share of decision outcomes (both sides of each `if`) that ran |
| Flaky test | Passes and fails on the same code |
| Quarantine | Moving a flaky test out of the blocking suite, with an owner and a deadline |
| Mirror test | A test whose expected value comes from the same logic as the code |
| Property | A rule that must hold for every valid input |
| Strategy | Hypothesis description of how to generate one kind of input |
| Shrinking | Searching for the smallest input that still fails |
| Oracle | An independent way to get the right answer |
| Fuzzing | Feeding generated or mutated inputs to a program to find crashes and hangs |
| Corpus | The inputs a fuzzer has kept because they reached new code |
| Fuzz harness | Small function that passes one input to the code under test |
| Mutant | A copy of the code with one small change |
| Killed, survived | A mutant is killed if a test fails, and survives if all tests pass |
| Mutation score | Share of mutants killed |

## Commands and syntax

| Task | Command or code |
|---|---|
| Branch coverage report | `pytest --cov=fees --cov-branch --cov-report=term-missing` |
| Branch coverage in config | `branch = true` under `[tool.coverage.run]` |
| Reproduce a set-order failure | `PYTHONHASHSEED=2 pytest -q` (Git Bash or WSL) |
| Generate inputs | `@given(st.lists(st.integers()))` |
| Repeatable Hypothesis run | `@settings(derandomize=True)` |
| Pin a failing case | `@example(items=[0], size=2)` |
| See how many cases ran or were discarded | `pytest --hypothesis-show-statistics` |
| Fuzz harness for Python | `atheris.Setup(sys.argv, test_one_input)` then `atheris.Fuzz()` |
| Mutation testing (WSL) | `mutmut run`, then `mutmut browse` |

## Property patterns

| Pattern | Example |
|---|---|
| Round trip | `json.loads(json.dumps(d)) == d` |
| Invariant | `len(sorted(xs)) == len(xs)` |
| Oracle | `slow_max(xs) == max(xs)` |

## Rules

- Test behaviour, edge cases and every bug you fix. Skip the language, libraries and private helpers.
- Coverage shows what no test ran, not what tests check. Turn on branch coverage and never make a percentage the goal.
- Reproduce a flaky test, then fix the cause. Do not retry, add `sleep` or delete.
- Review AI-written tests for three things: an assertion on a result, an expected value written by hand, and a failure when the code is broken.
- Pin every failure Hypothesis finds with `@example`. Its exact first failing input can differ between runs.
- Fuzzing finds crashes and hangs in code that parses untrusted input, and cannot see a wrong answer.
- A surviving mutant points at a missing test. A score of 100% is not the aim.
