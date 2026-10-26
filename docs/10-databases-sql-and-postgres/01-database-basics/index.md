# Database basics

Cheat sheet for the chapter. Lessons: [What a database is](01-what-a-database-is.md), [The relational model](02-the-relational-model.md), [Postgres and psql](03-postgres-and-psql.md).

## What a DBMS gives you

| Need | DBMS feature |
|---|---|
| Many writers at once | Concurrency control and transactions |
| Bad data kept out | Types, keys, `CHECK`, `NOT NULL` |
| Finding data | SQL (declarative) and indexes |
| Surviving a crash | Durability through a write-ahead log |

Families: relational (tables, SQL), document, key-value, graph, column store. OLTP means many small reads and writes from applications.

## Relational model terms

| Formal term | Everyday term |
|---|---|
| relation | table |
| tuple | row |
| attribute | column |
| domain | data type plus rules |

- A primary key identifies one row, is never `NULL` and never repeats.
- A foreign key holds another table's primary key; the DBMS rejects a value with no matching row.
- `NULL` means missing or unknown. Compare with `IS NULL`, never `= NULL`. `count(column)` skips `NULL`.
- A table has no row order unless the query has `ORDER BY`.

## The shop schema

| Table | Primary key | Foreign keys |
|---|---|---|
| `tax_rates` | `province` | none |
| `customers` | `customer_id` | `province` to `tax_rates` |
| `products` | `product_id` | none |
| `orders` | `order_id` | `customer_id` to `customers`, `ship_province` to `tax_rates` |
| `order_items` | `order_item_id` | `order_id` to `orders`, `product_id` to `products` |

Rows: 10 tax rates, 200 customers, 38 products, 900 orders, 1689 order items.

## Postgres terms

| Term | Meaning |
|---|---|
| Cluster | One server instance and its data |
| Database | Named collection in a cluster; a connection uses one |
| Schema | Namespace of tables inside a database; default `public` |
| Role | A Postgres account |

## psql meta-commands

| Command | What it does |
|---|---|
| `\?` | Help on meta-commands |
| `\l` | List databases |
| `\c dbname` | Connect to another database |
| `\dn` | List schemas |
| `\dt` | List tables |
| `\d table` | Describe a table |
| `\x` | Toggle expanded output |
| `\timing` | Toggle statement timing |
| `\i file.sql` | Run a SQL file |
| `\conninfo` | Show the current connection |
| `\q` | Quit |

Meta-commands have no semicolon. A missing `;` on SQL shows the `->` prompt.

## Connecting

```bash
sudo -u postgres psql
psql -h localhost -p 5432 -U app -d shop
psql "postgres://app:secret@localhost:5432/shop"
psql -d shop -f file.sql
```

Connection string: `postgresql://[user[:password]]@[host][:port]/[dbname]`. The default port is usually 5432. Keep passwords out of Git and shell history.
