# SQL from code and SQL injection

After this you can connect to Postgres from Python or Node, run queries with parameters instead of string building, and explain how SQL injection works and why parameters stop it.

Before this: [Postgres and psql](../01-database-basics/03-postgres-and-psql.md) and [joins](../02-querying/04-joins.md). Transactions get their own lesson<!-- link: ../04-postgres-in-depth/03-transactions-and-acid.md -->; here you only see how to start one from code.

## The idea

In `psql` you type SQL and read the result. An application does the same thing with a program: it opens a connection to the database server, sends SQL text, and reads rows back as objects in its own language. The piece of code that speaks the Postgres network protocol for you is a **driver**.

Opening a connection is slow (a TCP handshake, authentication, a new server process in Postgres), so a real app keeps a few connections open and lends them out. That set of reusable connections is a **connection pool**.

```mermaid
flowchart LR
    A["Your code<br/>(request handler)"] -->|"SQL text + parameters"| D["Driver<br/>psycopg or pg"]
    D --> P["Connection pool<br/>a few open connections"]
    P -->|"Postgres protocol<br/>over TCP, port 5432"| S[("Postgres")]
    S -->|"rows"| P --> D --> A
```

The dangerous part of this picture is the arrow from your code to the driver. If a user's text becomes part of the SQL text, the user is writing part of your program.

## Key terms

A **connection string** (or URL) packs the host, port, database, user and password into one value, such as `postgresql://app:secret@localhost:5432/shop`. It contains a password, so read it from an environment variable (`DATABASE_URL` is the usual name) and never commit it to Git.

A **parameterized query** (or prepared-style query) sends the SQL text with placeholders and the values separately. The server never parses the values as SQL. psycopg writes the placeholder as `%s`, node-postgres as `$1`, `$2`, and so on.

**SQL injection** is an attack where input from a user changes the structure of a query because it was pasted into the SQL text. It is on the [OWASP top 10](../../12-security/01-web-security/02-owasp-top-10.md), and the security chapter covers the wider family in [injection and input validation](../../12-security/01-web-security/03-injection-and-input-validation.md).

## How it works

The diagram shows where injection happens. With string building, the user's text is merged into the SQL before the server parses it. With parameters, the server parses the SQL first, and the value is only ever data.

```mermaid
flowchart LR
    subgraph bad["String-built: injectable"]
        direction LR
        U1["Input:<br/>x' OR '1'='1"] --> F["f-string merges<br/>text and input"]
        F --> Q1["SELECT ... WHERE email = 'x' OR '1'='1'"]
        Q1 --> P1["Server parses it<br/>as one query"]
    end
    subgraph good["Parameterized: safe"]
        direction LR
        Q2["SELECT ... WHERE email = $1"] --> P2["Server parses<br/>the text"]
        U2["Value:<br/>x' OR '1'='1"] --> B["Bound afterwards<br/>as data"]
        P2 --> B
    end
```

Both drivers follow the same shape: get a connection from a pool, run a query with parameters, read rows, give the connection back. This is psycopg 3 for Python (`pip install "psycopg[binary,pool]"`; docs at [psycopg.org](https://www.psycopg.org/psycopg3/docs/)):

```python
import os
from psycopg_pool import ConnectionPool

pool = ConnectionPool(os.environ["DATABASE_URL"], min_size=2, max_size=10)

def find_user(email):
    with pool.connection() as conn:   # borrow a connection
        row = conn.execute(
            "SELECT id, email FROM users WHERE email = %s", (email,)
        ).fetchone()
    return row                         # block exit: commit, and the connection goes back to the pool
```

And node-postgres, the `pg` package ([docs](https://node-postgres.com/features/pooling)), in JavaScript:

```javascript
import pg from "pg";
const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });

export async function findUser(email) {
  const result = await pool.query(
    "SELECT id, email FROM users WHERE email = $1", [email]);
  return result.rows[0];
}
```

`pool.query` borrows a connection, runs the query and returns it, so you can't leak one. When a transaction needs several statements on the same connection, check one out with `pool.connect()`, send `BEGIN`, the statements and `COMMIT`, roll back on an error, and always call `client.release()` in a `finally` block. A client you never release is gone from the pool for good, and after enough of those every request waits forever.

In psycopg, `with conn.transaction():` does the same thing: it commits when the block ends and rolls back if an exception escapes. Close the pool when the program exits (`pool.close()` in Python, `await pool.end()` in Node), or the process may hang.

Placeholders work for values only. A table or column name can't be a parameter, so if a query needs a dynamic column (for sorting, say), check the name against a fixed list in your code.

## Worked examples

<div class="example" markdown>

### Example 1: the attack, for real

Postgres isn't installed here, so this runs on SQLite with Python's `sqlite3`. The injection works the same way on any SQL database; only the placeholder differs (`?` instead of `%s`).

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, is_admin INTEGER)")
conn.executemany("INSERT INTO users (email, is_admin) VALUES (?, ?)",
                 [("ana@example.com", 0), ("root@example.com", 1)])

email = "x' OR '1'='1"                       # what an attacker types into the login form

query = f"SELECT email FROM users WHERE email = '{email}'"
print(query)
print(conn.execute(query).fetchall())

print(conn.execute("SELECT email FROM users WHERE email = ?", (email,)).fetchall())
```

```text
SELECT email FROM users WHERE email = 'x' OR '1'='1'
[('ana@example.com',), ('root@example.com',)]
[]
```

1. The f-string pastes the input inside the quotes. The attacker's own quote closes the string early, so the database sees `email = 'x'` followed by `OR '1'='1'`.
2. `'1'='1'` is always true, so the `WHERE` clause matches every row. A login query built this way returns a user for any password.
3. In the third call the value travels separately. The database compares the whole string `x' OR '1'='1` to each email, finds none, and returns no rows.

Check: the same demo with node-postgres placeholders (`$1`) was run on PGlite, an in-process Postgres, and gives the same three outputs.

</div>

<div class="example" markdown>

### Example 2: a transaction that rolls back

Two statements must succeed together. The second call tries to move more money than exists; a `CHECK (balance >= 0)` constraint rejects it, and the first `UPDATE` is undone. (Run on SQLite; `with conn:` is `sqlite3`'s version of psycopg's `conn.transaction()`.)

```python
def transfer(conn, src, dst, amount):
    try:
        with conn:  # commit on success, roll back on an exception
            conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, src))
            conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, dst))
    except sqlite3.IntegrityError as e:
        print("rolled back:", e)
```

Starting from balances of 100 and 50, we call `transfer(conn, 1, 2, 30)`, print the table, call `transfer(conn, 1, 2, 500)`, and print the table again.

```text
[(1, 70), (2, 80)]
rolled back: CHECK constraint failed: balance >= 0
[(1, 70), (2, 80)]
```

The balances after the failed transfer are unchanged. The `BEGIN`, `UPDATE`, `UPDATE`, `COMMIT`/`ROLLBACK` version for `pg` was run against PGlite with the same result.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: building SQL with f-strings, `+`, template literals or `"..." % value`. The last one is the sneakiest because it looks like a placeholder. `execute("... = %s" % email)` formats the string first; `execute("... = %s", (email,))` passes the value to the driver. Escaping quotes by hand is not a fix either; use the driver's parameters.

</div>

<div class="warning" markdown>

Watch out: opening a new connection per request, or never returning one. The first is slow and can hit Postgres's connection limit; the second drains the pool. Use a pool, and use `with` or `try`/`finally` so the connection always goes back.

</div>

<div class="warning" markdown>

Watch out: putting the connection string in the source. It holds the password, and a pushed secret has to be treated as leaked. Read `DATABASE_URL` from the environment.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: driver, connection pool, parameterized query, placeholder, SQL injection, transaction, `DATABASE_URL`, release.

Prompts to try:

- "Write a Python function using psycopg 3 and psycopg_pool that inserts an order and its items in one transaction. Use %s placeholders, read the connection string from DATABASE_URL, and don't build any SQL with f-strings."
- "Review this Node handler for SQL injection and connection leaks: [paste code]. It uses node-postgres 8 with a Pool."

What to check:

- Search the generated code for f-strings, `+` and template literals that touch a SQL string. Any user value found there is a bug.
- Which driver the code uses. AI often mixes psycopg2 and psycopg 3 APIs, or uses `?` or `:name` placeholders that Postgres drivers don't accept.
- Every `pool.connect()` has a `release()` in a `finally`.
- Dynamic table or column names are checked against an allow list, not passed as parameters or pasted from input.

</div>

## Quiz

1\. Why does a parameterized query stop SQL injection?

<details class="solution" markdown>
<summary>Answer</summary>

The SQL text and the values are sent separately, so the server parses the text first and treats each value only as data. A quote in the value can't end a string literal because the value is never part of the text.

</details>

2\. What does this print, and why?

```python
email = "a' OR '1'='1"
print(f"SELECT * FROM users WHERE email = '{email}'")
```

<details class="solution" markdown>
<summary>Answer</summary>

`SELECT * FROM users WHERE email = 'a' OR '1'='1'`. The input's quote closes the literal, and the added condition is always true, so the query matches every row.

</details>

3\. A teammate writes `cur.execute("SELECT * FROM users WHERE id = %s" % user_id)`. The code works in testing. What is wrong?

<details class="solution" markdown>
<summary>Answer</summary>

The `%` operator formats the string in Python before the driver sees it, so it is string building and is injectable. Pass the value as the second argument: `cur.execute("... WHERE id = %s", (user_id,))`.

</details>

4\. A Node service works for an hour and then every request hangs. The code uses `const client = await pool.connect()` and releases the client only after a successful query. What happened?

<details class="solution" markdown>
<summary>Answer</summary>

Each failed query skipped `release()`, so those clients were never returned. Once the pool's connections were all checked out, new requests waited for one forever. Put `client.release()` in a `finally` block.

</details>

## Lab

<div class="lab" markdown>

### Lab: break a login, then fix it

Goal: reproduce an injection and remove it with a parameter. Time: about 15 minutes. Runs in: any terminal with Python 3 (uses `sqlite3`, so no Postgres needed).

1. Create `login.py` with a `users` table holding `(email, password_hash)` for one user and a function `login(email, password_hash)` that returns the matching row using an f-string query.
2. Call it with the right email and a wrong hash. It should return nothing.
3. Call it with the email `ana@example.com' --` and any hash. Note what comes back and why (`--` starts a comment in SQL).
4. Rewrite `login` with `?` placeholders. Repeat step 3.
5. Add a function `sorted_users(column)` that takes a column name for `ORDER BY`. Make it accept only `email` and `id`, and raise `ValueError` otherwise.

Expected result: step 2 prints `None`, step 3 prints the user row (the attack worked), and after step 4 step 3 prints `None`.

<details class="solution" markdown>
<summary>Solution</summary>

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (email TEXT, password_hash TEXT)")
conn.execute("INSERT INTO users VALUES ('ana@example.com', 'h1')")

def login_bad(email, h):
    q = f"SELECT email FROM users WHERE email = '{email}' AND password_hash = '{h}'"
    return conn.execute(q).fetchone()

def login(email, h):
    return conn.execute(
        "SELECT email FROM users WHERE email = ? AND password_hash = ?", (email, h)
    ).fetchone()

def sorted_users(column):
    if column not in {"email", "id"}:
        raise ValueError("bad column")
    return conn.execute(f"SELECT email FROM users ORDER BY {column}").fetchall()

print(login_bad("ana@example.com", "wrong"))
print(login_bad("ana@example.com' --", "x"))
print(login("ana@example.com' --", "x"))
```

```text
None
('ana@example.com',)
None
```

With the comment marker, the query becomes `... WHERE email = 'ana@example.com' --' AND ...`, so the password check is commented out.

</details>

</div>

## Where this shows up

- Every web handler that reads from a database. Frameworks hide the driver, but the placeholders are still underneath, which is the next lesson on ORMs<!-- link: 02-orms-and-migrations.md -->.
- Connection limits and server-side pooling come back in [backups, replication and pooling](../04-postgres-in-depth/08-backups-replication-and-pooling.md).
