# Postgres and psql

After this you can start a PostgreSQL server, connect to it with `psql`, move around its databases and tables, run a `.sql` file, and read a connection string.

Before this: [The relational model](02-the-relational-model.md) and [Setting up your machine](../../00-start-here/setting-up-your-machine.md), step 7.

## The idea

PostgreSQL (Postgres) is a DBMS that runs as a **server**: a long-running program that owns the data files and waits for connections. Your code, a report tool and a terminal are **clients**. Each client opens a connection, sends SQL as text and receives rows back. No client reads the data files directly.

```mermaid
flowchart LR
    P["psql<br/>(terminal client)"] -->|"SQL over a connection"| S
    A["Your app<br/>(driver library)"] -->|"SQL over a connection"| S
    G["pgAdmin or DBeaver<br/>(GUI client)"] -->|"SQL over a connection"| S
    S["Postgres server<br/>listens on port 5432"] --> D[("Data files<br/>on disk")]
```

In the diagram, three different clients speak the same protocol to one server. The server is the only process that touches the disk. So when "the database is down", the server is not running or not reachable; the files are usually fine.

`psql` is the command-line client that ships with Postgres. It sends what you type to the server and prints the result. GUI clients such as pgAdmin and DBeaver do the same with windows and buttons.

## Key terms

A **cluster** is one running Postgres server instance and its data. It holds many databases.

A **database** is a named, separate collection inside a cluster. A connection is made to exactly one database, and a query cannot read across databases.

A **schema** is a namespace inside a database that groups tables. The default schema is `public`, which is why `customers` means `public.customers`.

A **role** is a Postgres account. A role can log in and can own objects.

A **meta-command** is a `psql` command that starts with a backslash. The psql program handles it; the server never sees it. SQL ends with a semicolon, meta-commands do not.

A **connection string** is one text value that says where and how to connect (below).

## How it works

The hierarchy is cluster, database, schema, table:

```mermaid
flowchart TD
    C["Cluster (one server)"] --> DB1["database: shop"]
    C --> DB2["database: postgres"]
    DB1 --> S1["schema: public"]
    S1 --> T1["customers"]
    S1 --> T2["orders"]
    S1 --> T3["..."]
```

Connect with the host, port, user and database. In WSL, after the install from the setup lesson, this opens `psql` as the Postgres superuser account:

```bash
sudo -u postgres psql
```

For a remote or password-protected server, pass the pieces as options (`-h` host, `-p` port, `-U` user, `-d` database), or one connection string:

```bash
psql -h localhost -p 5432 -U app -d shop
psql "postgres://app:secret@localhost:5432/shop"
```

The string has the form `postgresql://[user[:password]]@[host][:port]/[dbname]`, and `postgres://` is accepted as the same scheme ([libpq connection strings](https://www.postgresql.org/docs/current/libpq-connect.html)). The default port is usually 5432 (as of 2026; see the [psql reference](https://www.postgresql.org/docs/current/app-psql.html)). A password inside a string ends up in shell history and process lists, so for real systems use a `~/.pgpass` file or an environment variable instead, and never commit a connection string to Git.

Inside `psql` the useful meta-commands are:

| Command | What it does |
|---|---|
| `\?` | List all meta-commands |
| `\l` | List databases |
| `\c shop` | Connect to the database `shop` |
| `\dn` | List schemas |
| `\dt` | List tables in the search path |
| `\d customers` | Describe a table: columns, types, keys, indexes |
| `\x` | Toggle expanded output (one column per line, for wide rows) |
| `\timing` | Toggle showing how long each statement took |
| `\i file.sql` | Run the SQL commands in a file |
| `\q` | Quit |

To run a file without opening the prompt, use `psql -d shop -f file.sql`.

The in-browser runner in this book is not a server. It is PostgreSQL compiled to WebAssembly (the PGlite project) and loaded into your tab, with the `shop` database already created. The SQL is the same Postgres SQL, but there are no meta-commands, no network and no other clients. It is for learning queries; use a real server for everything else.

<div class="sql-runner" data-db="shop" markdown>

```sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

</div>

This SQL query lists what `\dt` would show: the five tables of `shop` in the `public` schema.

## Worked examples

<div class="example" markdown>

### Example 1: load shop into your own Postgres

The book's repository has the database as a plain SQL script, `docs/assets/sql/shop.sql`. Copy that file to your Linux home directory as `~/shop.sql`, then work in Ubuntu (WSL).

1. Start the server and create a role that matches your Linux user, allowed to create databases. The server's peer authentication lets that user connect over the local socket without a password.
2. Create the database `shop` owned by that role.
3. Run the script with `-f`.
4. Open `psql` on `shop` and look around.

```bash
sudo service postgresql start
sudo -u postgres createuser --createdb "$USER"
createdb shop
psql -d shop -f ~/shop.sql
psql -d shop
```

Then, at the `shop=>` prompt:

```text
\dt
\d customers
\timing
SELECT count(*) FROM orders;
\x
SELECT * FROM customers WHERE customer_id = 14;
\q
```

Check: `\dt` lists five tables, `\d customers` shows eight columns with `customer_id` as the primary key and a foreign key to `tax_rates`, and the count is 900. These match the browser runner, because both run the same script.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: a statement without a semicolon. The prompt changes from `shop=>` to `shop->` and waits for more input. Type `;` to finish it, or press Ctrl+C to cancel.

</div>

<div class="warning" markdown>

Watch out: confusing the server being off with a wrong password. "Connection refused" means nothing is listening on that host and port (in WSL, run `sudo service postgresql start`). "Password authentication failed" means the server is running and rejected the login.

</div>

<div class="warning" markdown>

Watch out: running a copied script on the wrong database. `shop.sql` begins with `DROP TABLE IF EXISTS ... CASCADE`, so it deletes tables of the same names. Check the prompt (or `\conninfo`) before `\i`.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: client-server, cluster, database, schema, role, connection string, meta-command, `psql`, port 5432.

Prompts to try:

- "I'm on Ubuntu in WSL2 with PostgreSQL installed from apt. `psql -d shop` says: role me does not exist. Explain peer authentication and give the commands to create a matching role."
- "Explain this connection string field by field and tell me which part must be kept secret: [paste a string with the password removed]."

What to check:

- Meta-commands inside SQL, or SQL given as a meta-command. `\dt` does not end with a semicolon and does not work in application code.
- Advice to edit `pg_hba.conf` or set `trust` authentication to fix a login error. Find the cause first; `trust` lets anyone in.
- Invented `psql` flags or meta-commands. Run `psql --help` or `\?` and compare.
- Real passwords in prompts or commits. Use a placeholder.

</div>

## Quiz

1\. Postgres is "down" but the data files are intact. Which part of the client-server picture is missing?

<details class="solution" markdown>
<summary>Answer</summary>

The server process. Clients can only reach the data through it.

</details>

2\. What does `\c orders_db` do, and does it need a semicolon?

<details class="solution" markdown>
<summary>Answer</summary>

It makes psql open a new connection to the database `orders_db`. It is a meta-command, so no semicolon.

</details>

3\. In `postgres://app:secret@db.example.com:5433/shop`, what are the user, host, port and database?

<details class="solution" markdown>
<summary>Answer</summary>

User `app`, password `secret`, host `db.example.com`, port 5433 (not the default), database `shop`.

</details>

4\. List the names of the `shop` tables, using `information_schema`, sorted by name. Expected: 5 rows.

<div class="sql-runner" data-db="shop" data-solution="sol-quiz-4" markdown>

```sql
-- write your query here
SELECT 1;
```

</div>

<details class="solution" id="sol-quiz-4" markdown>
<summary>Solution</summary>

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

</details>

## Lab

<div class="lab" markdown>

### Lab: your own shop database

Goal: run `shop` on a local Postgres server and answer a question with `psql`. Time: about 20 minutes. Runs in: WSL (Ubuntu).

1. Follow Example 1 until `psql -d shop` opens a prompt.
2. Use `\dt` and `\d orders`. How many tables are there, and which column of `orders` is a foreign key to `customers`?
3. Turn on `\timing`, then count the customers in each province. Which province has the most?
4. Cleanup: quit with `\q`, then run `dropdb shop`.

Expected result: 5 tables, `customer_id` is the foreign key, and Ontario has 72 customers.

<div class="sql-runner" data-db="shop" data-solution="sol-lab-3" markdown>

```sql
-- step 3, also runnable here
SELECT 1;
```

</div>

<details class="solution" id="sol-lab-3" markdown>
<summary>Solution</summary>

```sql
SELECT province, count(*) AS customers
FROM customers
GROUP BY province
ORDER BY customers DESC, province
LIMIT 3;
```

Ontario (ON) is first with 72.

</details>

</div>

## Where this shows up

- The Postgres chapter starts with indexes<!-- link: ../04-postgres-in-depth/01-indexes.md --> and uses `\timing` and `EXPLAIN` to see their effect.
- Application code connects with the same connection string; see SQL from code and SQL injection<!-- link: ../05-databases-in-apps/01-sql-from-code-and-sql-injection.md -->.
