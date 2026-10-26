# Databases in apps

A compact reference for the chapter. Lessons: [SQL from code and SQL injection](01-sql-from-code-and-sql-injection.md), [ORMs and migrations](02-orms-and-migrations.md), [NoSQL databases](03-nosql-databases.md), [Redis and caching](04-redis-and-caching.md).

## Key terms

| Term | Meaning |
|---|---|
| driver | Library that speaks the database protocol (psycopg 3 for Python, `pg` for Node) |
| connection pool | A set of open connections that requests borrow and return |
| connection string | One URL with host, port, database, user, password; read from `DATABASE_URL` |
| parameterized query | SQL text with placeholders, values sent separately |
| SQL injection | User input changes a query's structure because it was pasted into the SQL text |
| ORM | Maps tables to classes and rows to objects (SQLAlchemy, Prisma, Drizzle) |
| N+1 problem | 1 query for the parents plus N queries for their children |
| migration | Versioned script that changes the schema, tracked in a table and in Git |
| schema-on-write / read | Structure checked at insert / interpreted by the code at read time |
| cache-aside | App checks the cache, loads from the database on a miss, writes the cache |
| TTL | Seconds until a key is deleted automatically |
| stampede | Many requests rebuild the same expired key at once |
| eviction | Redis deleting keys at the `maxmemory` limit |

## Placeholders and driver calls

| Driver | Placeholder | Run a query | Transaction |
|---|---|---|---|
| psycopg 3 | `%s` | `conn.execute(sql, (a, b))` | `with conn.transaction():` |
| node-postgres | `$1`, `$2` | `pool.query(sql, [a, b])` | `BEGIN` / `COMMIT` / `ROLLBACK` on one `pool.connect()` client, then `release()` |
| sqlite3 (used in the demos) | `?` | `conn.execute(sql, (a, b))` | `with conn:` |

## Rules

- Never build SQL from user input with f-strings, `+`, template literals or `%`. Pass values as parameters.
- Placeholders are for values only. Check dynamic table or column names against a fixed list.
- Keep the connection string in an environment variable, not in Git.
- Always return a connection: `with`, or `finally { client.release() }`.
- Count queries when looping over ORM objects. Use eager loading (`selectinload`, `joinedload`, `include`) for relationships you read.
- Never edit an applied migration. Write a new one. Read generated migrations before committing.
- Live schema change: add a nullable column, write both, backfill in batches, switch reads, drop the old column later.
- Postgres is the source of truth. Redis holds copies, with a TTL and an invalidation on write.

## Commands

```bash
alembic init migrations
alembic revision --autogenerate -m "message"
alembic upgrade head
alembic downgrade -1
prisma migrate dev          # not run here
prisma migrate deploy       # not run here
drizzle-kit generate        # not run here
drizzle-kit migrate         # not run here
```

## NoSQL families

| Family | Example | Good at |
|---|---|---|
| document | MongoDB | records with varying shape, read as one unit |
| key-value | Redis, DynamoDB | lookup by key, caches, counters |
| wide-column | Cassandra | very high write volume, queries by partition key |
| graph | Neo4j | relationship traversal |

Postgres with a `jsonb` column covers many document cases: `@>` contains, `->` JSON, `->>` text, `?` has key, GIN index.

## Redis quick reference

| Type | Commands |
|---|---|
| string | `SET key value EX 300`, `GET`, `INCR`, `DEL`, `TTL`, `EXPIRE` |
| hash | `HSET`, `HGETALL` |
| list | `RPUSH`, `LPOP` (a one-line queue) |
| set | `SADD`, `SCARD` |
| sorted set | `ZADD`, `ZREVRANGE` |

`SET key value NX EX 10` sets only if the key is absent (a short lock). Eviction policies (as of 2026): `noeviction`, `allkeys-lru`, `allkeys-lfu`, `allkeys-random`, `volatile-lru`, `volatile-lfu`, `volatile-ttl`, `volatile-random`.
