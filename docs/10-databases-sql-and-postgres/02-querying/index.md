# Querying

A compact reference for the nine lessons of this chapter. The sample databases are `shop` (customers, products, orders, order_items, tax_rates) and `events` (users, events). No new teaching here; follow the lesson links for the explanations.

## Lessons

| # | Lesson | One line |
|---|---|---|
| 1 | [SELECT, WHERE and ORDER BY](01-select-where-and-order-by.md) | Choose columns, filter rows, sort, limit. |
| 2 | [NULL and three-valued logic](02-null-and-three-valued-logic.md) | `NULL` is unknown, and a comparison can be true, false or unknown. |
| 3 | [Aggregates, GROUP BY and HAVING](03-aggregates-group-by-and-having.md) | Collapse rows into groups and filter the groups. |
| 4 | [Joins](04-joins.md) | Combine tables on a key; keep unmatched rows with an outer join. |
| 5 | [Subqueries](05-subqueries.md) | A query inside a query: scalar, list, correlated, `EXISTS`. |
| 6 | [CTEs and recursive queries](06-ctes-and-recursive-queries.md) | Name steps with `WITH`; walk hierarchies with `WITH RECURSIVE`. |
| 7 | [Window functions](07-window-functions.md) | Per-row values over a window of rows, without collapsing them. |
| 8 | [Set operations and CASE](08-set-operations-and-case.md) | Combine result sets; if-then-else inside a query. |
| 9 | [Text, dates and times](09-text-dates-and-times.md) | String functions, patterns, dates, intervals and time zones. |

## The order a query runs

1. `FROM` and `JOIN` build the rows.
2. `WHERE` keeps rows (no aggregates, no window functions).
3. `GROUP BY` forms groups.
4. `HAVING` keeps groups.
5. `SELECT` computes the output columns, including window functions.
6. `ORDER BY` sorts, then `LIMIT` cuts.

A column alias made in `SELECT` can be used in `ORDER BY`, but not in `WHERE` or `HAVING`.

## Lessons 1 to 3: filtering, NULL and groups

<!-- db: shop -->
```sql
SELECT first_name, last_name, province
FROM customers
WHERE province IN ('ON', 'QC') AND signed_up >= '2025-01-01'
ORDER BY last_name, first_name
LIMIT 5;
```

- Comparisons: `=`, `<>`, `<`, `<=`, `IN (...)`, `BETWEEN a AND b` (both ends included), `LIKE`. `ORDER BY ... DESC` reverses; `LIMIT n OFFSET m` pages.
- `NULL` is not equal to anything, not even `NULL`. Test with `IS NULL` and `IS NOT NULL`, or `IS DISTINCT FROM` for a null-safe comparison.
- `WHERE` keeps a row only when the condition is true; unknown (from a `NULL`) drops the row. `x NOT IN (list containing NULL)` is never true.
- `COALESCE(x, 0)` replaces `NULL`; `NULLIF(a, b)` returns `NULL` when the two are equal. `ORDER BY x NULLS LAST` controls where `NULL` sorts.

<!-- db: shop -->
```sql
SELECT ship_province, count(*) AS orders, count(DISTINCT customer_id) AS customers
FROM orders
WHERE status <> 'cancelled'
GROUP BY ship_province
HAVING count(*) > 100
ORDER BY orders DESC;
```

- Aggregates: `count(*)` counts rows, `count(x)` skips `NULL`, `sum`, `avg`, `min`, `max`, `count(DISTINCT x)`. `sum` of no rows is `NULL`.
- Every non-aggregate column in `SELECT` must be in `GROUP BY`. `WHERE` filters rows before grouping; `HAVING` filters groups after.
- `count(*) FILTER (WHERE status = 'refunded')` counts a subset inside one aggregate.

## Lesson 4: joins

| Join | Keeps |
|---|---|
| `INNER JOIN` (or `JOIN`) | Only pairs where `ON` is true |
| `LEFT JOIN` | All left rows; right columns `NULL` when nothing matches |
| `RIGHT JOIN` | All right rows |
| `FULL JOIN` | Unmatched rows from both sides |
| `CROSS JOIN` | Every left row with every right row |

<!-- db: shop -->
```sql
SELECT c.customer_id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
```

This lists the 42 customers with no orders. A filter on the right table of a left join goes in `ON`, not `WHERE`. Joining "one" to "many" repeats the one row (1689 rows for 900 orders), so count with `count(DISTINCT ...)`. `USING (col)` replaces `ON a.col = b.col` and keeps one copy of the column.

## Lesson 5: subqueries

<!-- db: shop -->
```sql
SELECT name, price
FROM products p
WHERE price > (SELECT avg(price) FROM products)
  AND EXISTS (SELECT 1 FROM order_items i WHERE i.product_id = p.product_id)
ORDER BY price DESC
LIMIT 3;
```

- A scalar subquery returns one value, and can be used anywhere a value fits. `IN (SELECT ...)` tests membership.
- A correlated subquery refers to the outer row and runs once per outer row (conceptually). `EXISTS` is true when it returns any row, and `NOT EXISTS` is the safe way to say "no match" (unlike `NOT IN` with a `NULL`).
- A subquery in `FROM` needs an alias.

## Lesson 6: CTEs and recursive queries

<!-- db: shop -->
```sql
WITH RECURSIVE n(i) AS (
  SELECT 1                          -- anchor member
  UNION ALL
  SELECT i + 1 FROM n WHERE i < 5   -- recursive member
)
SELECT i FROM n;
```

- `WITH a AS (...), b AS (SELECT ... FROM a) SELECT ...`: later CTEs read earlier ones. A CTE lives for one statement.
- `AS MATERIALIZED` and `AS NOT MATERIALIZED` (PostgreSQL 12 and later) force storing or inlining a CTE.
- A recursive CTE runs in rounds and stops when a round returns no rows. Guard against cycles with a depth limit or `CYCLE id SET is_cycle USING trail` (PostgreSQL 14 and later).
- For a plain sequence use `generate_series(start, stop, step)`.

## Lesson 7: window functions

<!-- db: events -->
```sql
SELECT user_id, event_type,
       row_number() OVER w AS n,
       lag(event_type) OVER w AS previous
FROM events
WINDOW w AS (PARTITION BY user_id ORDER BY occurred_at)
ORDER BY user_id, n
LIMIT 4;
```

| Function | Result |
|---|---|
| `row_number()` | 1, 2, 3, ... with no ties |
| `rank()` | Ties share a rank; gaps follow (1, 1, 3) |
| `dense_rank()` | Ties share a rank; no gaps (1, 1, 2) |
| `lag(x, n)`, `lead(x, n)` | Value n rows before or after in the partition |
| `first_value(x)`, `last_value(x)` | First or last value in the frame |
| `sum(x) OVER (ORDER BY ...)` | Running total |
| `avg(x) OVER (ORDER BY ... ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` | 3-row moving average |

Window functions cannot appear in `WHERE` or `HAVING`. To filter on one (top N per group), compute it in a CTE or subquery and filter in the outer query. `PARTITION BY` restarts the function per group; `ORDER BY` inside `OVER` does not sort the final output.

## Lesson 8: set operations and CASE

| Operation | Result |
|---|---|
| `A UNION B` | Rows in either, duplicates removed |
| `A UNION ALL B` | Rows in either, duplicates kept (faster) |
| `A INTERSECT B` | Rows in both |
| `A EXCEPT B` | Rows in A and not in B (order matters) |

Both queries need the same number of columns with compatible types; names come from the first query; `INTERSECT` binds tighter than `UNION` and `EXCEPT`.

<!-- db: shop -->
```sql
SELECT CASE WHEN price < 20 THEN 'budget'
            WHEN price < 100 THEN 'mid'
            ELSE 'premium' END AS band,
       count(*) AS products
FROM products
GROUP BY 1;
```

- `CASE` tries branches top to bottom and returns the first match; with no `ELSE` the result is `NULL`. Simple form: `CASE col WHEN 'a' THEN ... END`.
- Pivot: `sum(CASE WHEN status = 'x' THEN 1 ELSE 0 END)` or `count(*) FILTER (WHERE status = 'x')`, one per output column.

## Lesson 9: text, dates and times

| Task | Syntax |
|---|---|
| Join text | `a \|\| ' ' \|\| b` (`NULL` if either is `NULL`), `concat_ws(', ', a, b)` (skips `NULL`) |
| Case, trim, size | `lower`, `upper`, `initcap`, `trim`, `length` |
| Cut and find | `left(s, n)`, `substr(s, from, n)`, `split_part(s, '@', 2)`, `position('x' IN s)`, `replace(s, a, b)` |
| Simple pattern | `s LIKE 'S%'` (`%` any run, `_` one character), `ILIKE` ignores case |
| Regular expression | `s ~ '^[0-9]{3}-'`, `~*` ignores case, `regexp_replace(s, '[^0-9]', '', 'g')` |
| Start of a period | `date_trunc('month', ts)` |
| One field | `extract(year FROM ts)`, `extract(dow FROM ts)` (Sunday is 0), `isodow` (Monday is 1) |
| Format | `to_char(ts, 'YYYY-MM-DD HH24:MI')` |
| Arithmetic | `date + 7`, `ts + interval '1 month'`, `date1 - date2` (days), `age(ts1, ts2)` |
| Time zone | `SET TIME ZONE 'America/Toronto'`, `ts AT TIME ZONE 'America/Toronto'` |
| Every day in a range | `generate_series(ts_start, ts_end, interval '1 day')` then `LEFT JOIN` |

<!-- db: events -->
```sql
SELECT to_char(date_trunc('month', occurred_at), 'YYYY-MM') AS month, count(*) AS purchases
FROM events
WHERE event_type = 'purchase'
  AND occurred_at >= '2025-01-01' AND occurred_at < '2025-04-01'
GROUP BY 1
ORDER BY 1;
```

- Types: `date` is a day; `timestamp` is a clock reading with no zone; `timestamptz` is a moment stored as UTC and shown in the session's `TimeZone`. Use `timestamptz` for real events.
- Filter timestamps with a half-open range (`>= start AND < next_start`), not `BETWEEN`.
- `interval '1 day'` follows the calendar (a daylight-saving day can be 23 hours); `interval '24 hours'` is exact elapsed time.

## Common mistakes in this chapter

- A `WHERE` filter on the right table of a left join, which silently turns it into an inner join.
- Counting after a one-to-many join without `DISTINCT`.
- `NOT IN` with a list that contains `NULL`: use `NOT EXISTS`.
- Filtering a window function in `WHERE`.
- `UNION` where `UNION ALL` was meant (or the reverse).
- `CASE` inside `sum` with no `ELSE 0`, which can return `NULL`.
- `BETWEEN` on timestamps, and `timestamp` used for real moments.
