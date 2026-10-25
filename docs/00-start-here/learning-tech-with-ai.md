# Learning tech with AI

After this you can use an AI assistant to learn and to write code without trusting it blindly: you know what it does well, where it fails, and a loop that catches the failures.

This book assumes you will use AI coding tools at work. It does not try to make you memorize every flag and API. It tries to give you the vocabulary and mental models to ask a precise question and to judge whether the answer is right.

## Why vocabulary comes first

An assistant answers the question you typed, not the one you meant. "Make my database faster" has dozens of valid answers: add an index, rewrite a join, cache the result, change the data type, add a connection pool. If you know the words "index", "query plan" and "N+1 query", you can write "this query does a sequential scan on a 2-million-row table; suggest an index and show me how to confirm it with `EXPLAIN`". That prompt names the problem, so the answer can be checked.

The same knowledge is how you judge the output. A person who has never seen a SQL injection cannot notice one in generated code. The assistant will not warn you, because from its point of view the code works.

## What an assistant is good and bad at

An **LLM** (large language model) produces text that is statistically likely to follow your prompt. It has no built-in way of checking that the text is true. Good uses follow from that:

- Explaining a concept or an unfamiliar error in plain words.
- Drafting boilerplate, tests and small functions in well-known languages.
- Translating between formats or languages (a shell script to Python, JSON to a type definition).
- Suggesting what to look at when you are stuck.

The failure modes are specific, and each one is checkable.

| Failure | What it looks like | How to check |
|---|---|---|
| Confident error | Wrong explanation in a calm, fluent tone | Run the code; compare with the official docs |
| Outdated API | A function or option that was removed or renamed | Check the docs for the version you use |
| Invented flag, function or package | `--fast-mode` that no tool has; a library name that does not exist | Run `--help`; search the package registry; read the package's page |
| Security mistake | SQL built from strings, hard-coded secrets, disabled certificate checks | Read the code for these patterns; run a scanner |
| Almost right | Works on the example, fails on empty input or unusual characters | Test the edges yourself |

The Stack Overflow 2025 Developer Survey puts numbers on this. Among all respondents, 84% use or plan to use AI tools, and 66% name "AI solutions that are almost right, but not quite" as a top frustration. 45.2% say debugging AI-generated code takes more time. More respondents distrust the accuracy of AI output (46%) than trust it (33%) ([Stack Overflow 2025, AI section](https://survey.stackoverflow.co/2025/ai)).

MIT's Missing Semester course gives matching advice for agentic tools: review output for correctness and security bugs, and give the model a way to check itself, such as a test suite or type checker. It also warns that verifying code can be harder than writing it, and that for critical code you may want to write it by hand ([Agentic Coding, 2026](https://missing.csail.mit.edu/2026/agentic-coding/)).

## The loop

1. Learn the concept. Read the lesson until you can say what it is and name the parts.
2. Ask precisely. Give the language and version, the goal, what you already tried, and the exact error text.
3. Get the answer. Read the text around the code block too.
4. Verify. Run it, run the tests, read the official docs for anything unfamiliar.
5. Explain it back. Say in your own words what each part does and why. If you cannot, ask the assistant to explain the part, then verify that explanation too.

Step 5 is the one people skip, and it is the one that stops you shipping code you do not understand. The Missing Semester lecture warns that leaning on agents too heavily can leave you with a shallow understanding.

## The Working with AI box

Each lesson ends its main text with a box like this one. It has three parts.

- Words to use: three to six terms from the lesson. Put them in your prompt.
- Prompts to try: two or three prompts a developer would send, with the context an assistant needs.
- What to check: failure modes particular to that topic, each with a way to verify it.

The box is part of the lesson. Treat "What to check" as the exam: it is the list of things a reviewer should catch.

## A worked example

<div class="example" markdown>

### Example 1: a vague prompt and a precise one

The task: save a new user to a database.

Vague prompt:

```text
write python code to save users to the database
```

The assistant has to guess the database, the library, the table and what a "user" is. You might get SQLite when you use PostgreSQL, or a class you did not ask for.

Precise prompt:

```text
Python 3.12, PostgreSQL 16, psycopg 3. Table users(id serial primary key,
email text unique not null, name text not null). Write add_user(conn, email, name)
that inserts one row and returns the new id. Use a parameterized query. If the
email already exists, raise a ValueError instead of a database error. Include
two pytest tests.
```

Each phrase fixes one decision: versions, schema, function signature, injection safety, error behaviour, tests. Now check the answer against four points.

1. Is the SQL built with a placeholder, not with an f-string?
2. Does the unique-violation case really raise `ValueError`, and does the code roll back the transaction?
3. Do the tests include an empty or odd input?
4. Is every function and keyword argument in the psycopg 3 docs?

Check 1 in code. This runs on every machine with Python (it uses SQLite's `?` placeholder instead of PostgreSQL's `%s`, but the idea is the same):

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE users (name TEXT)")
name = "O'Brien"

# Shape 1: SQL built by string formatting
try:
    db.execute(f"INSERT INTO users (name) VALUES ('{name}')")
except sqlite3.OperationalError as e:
    print("string-built SQL failed:", e)

# Shape 2: parameterized query
db.execute("INSERT INTO users (name) VALUES (?)", (name,))
print(db.execute("SELECT name FROM users").fetchall())
```

```text
string-built SQL failed: near "Brien": syntax error
[("O'Brien",)]
```

A name with an apostrophe breaks the first shape. A name crafted on purpose does worse than break it: that is SQL injection, covered in SQL from code and SQL injection<!-- link: ../10-databases-sql-and-postgres/05-databases-in-apps/01-sql-from-code-and-sql-injection.md -->.

</div>

## Privacy rules

Many AI tools send your prompts and files to a server you do not control; the Missing Semester lecture says the same about code and conversations going to the cloud. So:

- Do not paste passwords, API keys, tokens, private keys or `.env` files. If one slips into a prompt, treat it as leaked and rotate it.
- Do not paste your employer's code, customer data or internal documents into a public tool. Use the tools your employer approves, and read its policy first.
- Replace real values with placeholders (`user@example.com`, `API_KEY_HERE`) before you paste an error or a config.
- Keep permission prompts on when a tool can run commands or edit files. The lecture says skipping them is only reasonable inside an isolated environment such as a VM or container.

More on this in AI security risks<!-- link: ../15-ai-and-llms/03-ai-assisted-development/04-ai-security-risks.md --> and reviewing AI code<!-- link: ../15-ai-and-llms/03-ai-assisted-development/03-reviewing-ai-code.md -->.

## Working with AI

<div class="ai" markdown>

### Working with AI

Words to use: hallucination, context window, prompt, verification, version, reproducible example.

Prompts to try:

- "Explain what a context window is, then tell me three ways a long chat can make your earlier answers worse. I will check each against your provider's documentation."
- "Here is my function and the failing test output (pasted). List the three most likely causes, ranked, and for each give one command that would confirm or rule it out."

What to check:

- Every package, command and flag the answer names exists. Run `--help` or open the package page.
- The answer matches your versions. Ask which version it assumed.
- The code handles empty, huge and malformed input.
- Nothing in the answer asks you to disable a security check "to make it work".

</div>

## Where this shows up

- Writing prompts that carry context is covered in prompt and context engineering<!-- link: ../15-ai-and-llms/02-building-with-llms/02-prompt-and-context-engineering.md -->, and why models produce wrong answers in sampling and hallucinations<!-- link: ../15-ai-and-llms/01-how-llms-work/04-sampling-and-hallucinations.md -->.
- Reading what comes back is the subject of [Reading docs and error messages](reading-docs-and-error-messages.md).
