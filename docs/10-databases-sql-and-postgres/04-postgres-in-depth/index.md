# Postgres in depth

A compact reference for the eight lessons of this chapter. It teaches nothing new; follow the links for the reasoning.

## Lessons

1. [Indexes](01-indexes.md)
2. [EXPLAIN and query plans](02-explain-and-query-plans.md)
3. [Transactions and ACID](03-transactions-and-acid.md)
4. [Isolation, locking and MVCC](04-isolation-locking-and-mvcc.md)
5. [Roles, privileges and row-level security](05-roles-privileges-and-row-level-security.md)
6. [Views, functions and triggers](06-views-functions-and-triggers.md)
7. [JSONB and full-text search](07-jsonb-and-full-text-search.md)
8. [Backups, replication and pooling](08-backups-replication-and-pooling.md)

## Key terms

| Term | Meaning |
|---|---|
| Index | Sorted structure mapping column values to table rows; default type is B-tree |
| Query plan | The steps the planner chooses to run a query, shown by `EXPLAIN` |
| Transaction | A group of statements that succeed or fail together |
| ACID | Atomicity, consistency, isolation, durability |
| MVCC | Multi-version concurrency control: readers see a snapshot and don't block writers |
| Role | Named holder of privileges; a user is a role with `LOGIN` |
| Least privilege | Each role gets only what its job needs |
| RLS policy | Boolean expression per row deciding which rows a role sees or writes |
| View | Named stored `SELECT`, run on every use |
| Materialized view | Stored query result, fresh only as of the last `REFRESH` |
| Trigger | Function that runs automatically on `INSERT`, `UPDATE` or `DELETE` |
| JSONB | Binary JSON column type that supports indexes and containment |
| tsvector, tsquery | Normalized document and search expression for full-text search |
| WAL | Write-ahead log of every change; basis of recovery and replication |
| PITR | Point-in-time recovery: base backup plus archived WAL |
| Replication lag | How far a replica is behind the primary |
| Connection pooler | Proxy sharing a few real connections among many clients |

## Indexes and plans

```sql
CREATE INDEX idx ON t (a);                       -- B-tree
CREATE INDEX idx ON t (a, b);                    -- composite: leftmost column first
CREATE UNIQUE INDEX idx ON t (a);
CREATE INDEX idx ON t (a) WHERE status = 'open'; -- partial
CREATE INDEX idx ON t (lower(email));            -- expression
CREATE INDEX idx ON t (a) INCLUDE (b);           -- covering
CREATE INDEX CONCURRENTLY idx ON t (a);          -- no write lock; not inside a transaction
DROP INDEX idx;
EXPLAIN SELECT ...;                              -- plan only
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;           -- runs the query, adds real times and page reads
```

Foreign key columns are not indexed automatically. Every index speeds some reads and slows every write.

## Transactions and isolation

```sql
BEGIN;
UPDATE accounts SET balance = balance - 50 WHERE id = 1;
SAVEPOINT s1;
UPDATE accounts SET balance = balance + 50 WHERE id = 2;
ROLLBACK TO s1;          -- undo back to the savepoint only
COMMIT;                  -- or ROLLBACK; to undo everything

BEGIN ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;    -- before the first query of a transaction
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;  -- lock the row until commit
```

Isolation levels in Postgres: `READ COMMITTED` (default), `REPEATABLE READ`, `SERIALIZABLE`. Serializable failures must be retried by the application.

## Roles, privileges and RLS

```sql
CREATE ROLE readonly;                                  -- group role
CREATE ROLE ana LOGIN PASSWORD '...';                  -- user
GRANT readonly TO ana;
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
GRANT SELECT (id, city) ON customers TO support;       -- column level
REVOKE DELETE ON orders FROM app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly;

ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY p ON orders FOR SELECT
  USING (ship_province = current_setting('app.province', true));
SET ROLE ana;  RESET ROLE;                             -- act as another role
```

| Role | Typical privileges |
|---|---|
| Migrator | Owns tables; `CREATE`, `ALTER`, `DROP` |
| App | `SELECT`, `INSERT`, `UPDATE`, `DELETE` on needed tables; no DDL |
| Analyst | `SELECT` only, through a group role |

Owners and superusers bypass RLS. RLS on with no matching policy returns zero rows. Supabase: roles `anon` and `authenticated`, `auth.uid()` in policies, `service_role` bypasses RLS.

## Views, functions and triggers

```sql
CREATE VIEW v AS SELECT ...;
CREATE VIEW v AS SELECT ... WHERE ... WITH CHECK OPTION;   -- updatable, guarded
CREATE MATERIALIZED VIEW m AS SELECT ...;
REFRESH MATERIALIZED VIEW m;                               -- CONCURRENTLY needs a unique index

CREATE FUNCTION f(x numeric) RETURNS numeric LANGUAGE sql IMMUTABLE AS $$ SELECT x * 2 $$;

CREATE FUNCTION trg() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at := now(); RETURN NEW; END $$;
CREATE TRIGGER t BEFORE UPDATE ON tbl FOR EACH ROW EXECUTE FUNCTION trg();
```

`NEW` is the row being written and `OLD` the row it replaces. A `BEFORE` trigger must `RETURN NEW`. List triggers with `SELECT tgname FROM pg_trigger WHERE NOT tgisinternal;`.

## JSONB and full-text search

| Syntax | Meaning |
|---|---|
| `col->'k'`, `col->>'k'` | Value as JSON, value as text |
| `col->0` | Array element |
| `col @> '{"k": 1}'` | Contains |
| `col ? 'k'` | Top-level key exists |
| `jsonb_build_object('k', v)` | Build an object |
| `CREATE INDEX ON t USING gin (col)` | Index for `@>` and `?` |
| `to_tsvector('english', text)` | Document to tsvector |
| `websearch_to_tsquery('english', 'a b -c')` | User text to tsquery |
| `vec @@ query` | Match |
| `ts_rank(vec, query)` | Relevance score |

Use columns for stable, filtered, constrained fields and JSONB for variable shape. Use a generated `tsvector` column with a GIN index instead of `LIKE '%x%'`.

## Backups, replication and pooling

In WSL (Ubuntu), unverified in the book's runner:

```bash
pg_dump --format=custom --file=shop.dump shop
pg_restore --dbname=shop_copy --clean --if-exists shop.dump
pg_basebackup -D /backup/base -Ft -z -P -X stream
```

| Need | Tool |
|---|---|
| Copy or move a database, restore one table | Logical backup, `pg_dump` |
| Fast full restore, recover to a past moment | Base backup plus archived WAL (PITR) |
| Survive a server failure, offload reads | Streaming replication, read replica |
| Replicate some tables or across versions | Logical replication (publication and subscription) |
| Too many connections | PgBouncer, `pool_mode = transaction` |

Replicas are asynchronous by default, so they lag. A replica is not a backup. Transaction pooling breaks `SET`, `LISTEN`, session advisory locks and `PREPARE`; use `SET LOCAL`.
