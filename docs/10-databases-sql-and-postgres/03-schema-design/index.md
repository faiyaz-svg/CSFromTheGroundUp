# Schema design

A compact reference for choosing types, writing constraints, changing tables, modelling relationships and normalizing. No new teaching here; each lesson explains the why.

Lessons: [data types and constraints](01-data-types-and-constraints.md), [creating and changing tables and data](02-creating-and-changing-tables-and-data.md), [modelling relationships and ER diagrams](03-modelling-relationships-and-er-diagrams.md), [normalization and denormalization](04-normalization-and-denormalization.md).

## Data type chooser

| Job | Use | Avoid |
|---|---|---|
| Counts, small whole numbers | `integer` | |
| Ids that may pass 2.1 billion | `bigint` | |
| Money, exact decimals | `numeric(12,2)` | `real`, `double precision` |
| Measurements | `double precision` | comparing with `=` |
| Text | `text` | `varchar(n)` unless a limit is a real rule |
| Yes or no | `boolean` | `integer` flags |
| A calendar day | `date` | |
| A moment in time | `timestamptz` | `timestamp` for events |
| Row id | `bigint GENERATED ALWAYS AS IDENTITY` | |
| Id made outside the database | `uuid` (`gen_random_uuid()`) | |
| Nested, flexible data | `jsonb` | using it to skip modelling |
| Short list of tags | `text[]` | arrays you need to join on |

## Constraint syntax

| Rule | Column form | Table form |
|---|---|---|
| Value required | `email text NOT NULL` | |
| Default value | `status text DEFAULT 'new'` | |
| No duplicates | `email text UNIQUE` | `UNIQUE (a, b)` |
| Condition | `qty integer CHECK (qty > 0)` | `CHECK (end_date >= start_date)` |
| Row identity | `id bigint PRIMARY KEY` | `PRIMARY KEY (a, b)` |
| Reference | `author_id integer REFERENCES authors` | `FOREIGN KEY (author_id) REFERENCES authors (author_id)` |

Foreign key delete behaviour: `ON DELETE RESTRICT` (refuse), `ON DELETE CASCADE` (delete children), `ON DELETE SET NULL` (keep children, blank the key). The default is `NO ACTION`, which refuses like `RESTRICT`.

## Changing tables and data

| Task | Statement |
|---|---|
| New table | `CREATE TABLE t (...)` |
| Add, drop, rename column | `ALTER TABLE t ADD COLUMN c type`, `DROP COLUMN c`, `RENAME COLUMN c TO d` |
| Add a constraint | `ALTER TABLE t ADD CONSTRAINT name CHECK (...)` |
| Add one without a long scan | `... NOT VALID`, then `ALTER TABLE t VALIDATE CONSTRAINT name` |
| Remove table / all rows | `DROP TABLE t` / `TRUNCATE t` |
| Insert rows | `INSERT INTO t (a, b) VALUES (1, 'x'), (2, 'y')` |
| Copy rows | `INSERT INTO t (a, b) SELECT a, b FROM s WHERE ...` |
| Change rows | `UPDATE t SET a = 1 WHERE ...` |
| Delete rows | `DELETE FROM t WHERE ...` |
| See what changed | add `RETURNING a, b` |
| Insert or update | `INSERT ... ON CONFLICT (key) DO UPDATE SET a = EXCLUDED.a` |

Rules: always list columns in `INSERT`; write the `SELECT` with the same `WHERE` before an `UPDATE` or `DELETE`; on a big table, add nullable, backfill in batches, then constrain.

## Relationships

| Cardinality | Crow's foot | Implementation |
|---|---|---|
| 1:1 | `\|\|--o\|` | Foreign key plus `UNIQUE` |
| 1:N | `\|\|--o{` | Foreign key on the "many" side |
| M:N | `}o--o{` | Junction table, pair of foreign keys as primary key |

Naming: plural `snake_case` tables, `<singular>_id` primary keys, a foreign key named like the key it references.

## Normal forms in one line each

| Form | One line |
|---|---|
| 1NF | One value per cell, no repeating groups, and a key. |
| 2NF | Every non-key column depends on the whole key. |
| 3NF | Non-key columns depend on the key and nothing else. |
| BCNF | Every determinant is a candidate key. |

Anomalies: update (a fact changed in some rows only), insert (a fact can't be stored alone), delete (removing a row loses another fact). Denormalize on purpose with a materialized view, a summary table or a cache, and decide how it is refreshed.
