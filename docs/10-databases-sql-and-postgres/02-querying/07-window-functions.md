# Window functions

After this you can number, rank and compare rows within groups, compute running totals and moving averages, and pick the top rows per group, all without collapsing the rows.

Before this: [aggregates, GROUP BY and HAVING](03-aggregates-group-by-and-having.md) and CTEs<!-- link: 06-ctes-and-recursive-queries.md -->.

## The idea

The `events` database logs what each user did: `signup`, `page_view`, `add_to_cart`, `purchase`. Three questions share one shape: "what was this user's second event?", "how long since their previous event?", "what is the running total of purchases this year?". Each answer needs a row to look at other rows near it, and `GROUP BY` can't do that because it replaces many rows with one.

A **window function** computes a value for each row from a set of related rows (its window), and keeps every row in the output. The query below adds a counter and the previous time to each event, restarting for every user. In the table, the horizontal line is where `PARTITION BY user_id` starts a new window.

```text
user_id  event_type  at           n   prev_at
-------  ----------  -----------  --  -----------
1        signup      07-15 08:06  1   NULL
1        page_view   07-24 13:50  2   07-15 08:06
1        page_view   07-25 15:54  3   07-24 13:50
------------------------------------------------- partition boundary
2        signup      03-04 19:39  1   NULL
2        page_view   03-05 03:34  2   03-04 19:39
2        page_view   03-12 04:46  3   03-05 03:34
```

Each user is a partition, rows inside it are ordered by time, and `n` and `prev_at` are computed within that order.

## Key terms

A **window function** is a function followed by `OVER (...)`. Without `OVER`, `sum()` is an ordinary aggregate that collapses rows; with `OVER`, it returns one value per row.

`PARTITION BY` splits the rows into independent groups, and the function restarts in each. Leaving it out makes the whole result one partition. `ORDER BY` inside `OVER` orders the rows within each partition, and is needed for ranking, `lag` and running totals. It does not sort the final output.

A **frame** is the part of the partition that the function sees for the current row, such as "this row and the two before it": `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`.

## How it works

The window functions run after `FROM`, `WHERE`, `GROUP BY` and `HAVING`, and just before the final `ORDER BY` and `LIMIT`. They see the rows that survived filtering, and aggregates that are already computed.

<div class="sql-runner" data-db="events" markdown>

```sql
SELECT user_id, event_type, to_char(occurred_at, 'MM-DD HH24:MI') AS at,
       row_number() OVER w AS n,
       to_char(lag(occurred_at) OVER w, 'MM-DD HH24:MI') AS prev_at
FROM events
WHERE user_id IN (1, 2)
WINDOW w AS (PARTITION BY user_id ORDER BY occurred_at)
ORDER BY user_id, occurred_at
LIMIT 6;
```

</div>

`WINDOW w AS (...)` names a window so two functions can share it. The first row of each user has `NULL` in `prev_at`, because `lag` finds no earlier row. `lead` looks forward instead, and both take an optional offset and default: `lag(x, 2, 0)`.

Three ranking functions differ only on ties. This runner uses a list of scores with a tie at 85.

<div class="sql-runner" data-db="events" markdown>

```sql
SELECT v, row_number() OVER (ORDER BY v DESC) AS row_number,
          rank() OVER (ORDER BY v DESC) AS rank,
          dense_rank() OVER (ORDER BY v DESC) AS dense_rank
FROM (VALUES (90), (85), (85), (70)) AS t(v)
ORDER BY v DESC;
```

</div>

`row_number` gives 1, 2, 3, 4 and breaks ties arbitrarily. `rank` gives 1, 2, 2, 4: tied rows share a rank and the next rank skips. `dense_rank` gives 1, 2, 2, 3 with no gap.

With an `ORDER BY` in the window, an aggregate such as `sum()` becomes a running total, because the default frame runs from the start of the partition to the current row. The explicit frame `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` makes a moving window of three rows. Here is the frame for the April row of the monthly purchase counts:

```text
month       purchases   running_total       avg_3_months
2025-01     19          19
2025-02     36          55  |-- frame --|
2025-03     34          89  |  36 + 34  |
2025-04     25          114 |  + 25     |  = 95 / 3 = 31.7
```

In the table, the three rows in the frame for April are February, March and April. For the running total the frame is every row from January to April: 19 + 36 + 34 + 25 = 114.

## Worked examples

<div class="example" markdown>

### Example 1: running total and moving average

1. A CTE counts purchases per month, with one row per month.
2. `sum(purchases) OVER (ORDER BY month)` adds up all rows so far.
3. `avg(...) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` averages the current and two previous months. The first two rows have fewer than three rows in their frame, so they average what exists.

<div class="sql-runner" data-db="events" markdown>

```sql
WITH monthly AS (
  SELECT date_trunc('month', occurred_at)::date AS month, count(*) AS purchases
  FROM events
  WHERE event_type = 'purchase'
  GROUP BY 1
)
SELECT month, purchases,
       sum(purchases) OVER (ORDER BY month) AS running_total,
       round(avg(purchases) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1) AS avg_3_months
FROM monthly
ORDER BY month;
```

</div>

Check: there are 20 months. January 2025 has 19 purchases, and by April the running total is 114 and the 3-month average is 31.7. The last running total is 227, the number of `purchase` events.

</div>

<div class="example" markdown>

### Example 2: top 2 users per plan

A window function can't appear in `WHERE`, because `WHERE` runs before windows exist. Compute the rank in a CTE (or subquery), then filter in the next step.

<div class="sql-runner" data-db="events" markdown>

```sql
WITH buyers AS (
  SELECT u.plan, u.user_id, count(*) AS purchases
  FROM users u
  JOIN events e USING (user_id)
  WHERE e.event_type = 'purchase'
  GROUP BY u.plan, u.user_id
),
ranked AS (
  SELECT plan, user_id, purchases,
         row_number() OVER (PARTITION BY plan ORDER BY purchases DESC, user_id) AS rn
  FROM buyers
)
SELECT plan, user_id, purchases, rn
FROM ranked
WHERE rn <= 2
ORDER BY plan, rn;
```

</div>

Check: 6 rows, 2 per plan. The `basic` plan has users 28 and 191, both with 4 purchases: a tie, which `user_id` in the window's `ORDER BY` settles. To keep every tied user, use `rank` or `dense_rank` instead of `row_number`.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: filtering a window function in `WHERE`.

<!-- sql: expect-error -->
<!-- db: events -->
```sql
SELECT user_id, row_number() OVER (ORDER BY occurred_at) AS rn
FROM events
WHERE row_number() OVER (ORDER BY occurred_at) <= 3;
```

PostgreSQL answers "window functions are not allowed in WHERE". Move the window into a CTE or subquery and filter there, as in Example 2.

</div>

<div class="warning" markdown>

Watch out: a missing or incomplete `ORDER BY` in `OVER`. Without it, `row_number` and `lag` depend on whatever order the rows arrive in, and the answer can change between runs. Add a tie-breaker (a unique column) when the sort column can repeat.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: window function, `PARTITION BY`, frame, `ROWS BETWEEN`, `row_number`, `rank`, `dense_rank`, `lag`.

Prompts to try:

- "PostgreSQL 17, table `events(event_id, user_id, event_type, occurred_at)`. For each user, return the time between each event and the one before it. Use `lag` and show the result for user 2."
- "Return the top 3 users per plan by purchases, and say what happens on ties with `row_number`, `rank` and `dense_rank`."

What to check:

- Which ranking function it chose, and whether ties should be kept. Run the query on data with a tie.
- That the window has an `ORDER BY` with a tie-breaker, so repeated runs return the same rows.
- That the filter on the window result is in an outer query, not in `WHERE`.
- That the frame is stated when you want a moving window; the default frame includes all earlier rows.

</div>

## Quiz

1\. What is the difference between `sum(x)` with `GROUP BY` and `sum(x) OVER (PARTITION BY g)`?

<details class="solution" markdown>
<summary>Answer</summary>

`GROUP BY` returns one row per group. The window version keeps every input row and repeats the group's sum on each of them.

</details>

2\. What do `rank()` and `dense_rank()` return for the values 10, 10, 8 ordered descending?

<!-- db: events -->
```sql
SELECT v, rank() OVER (ORDER BY v DESC) AS rank, dense_rank() OVER (ORDER BY v DESC) AS dense_rank
FROM (VALUES (10), (10), (8)) AS t(v);
```

<details class="solution" markdown>
<summary>Answer</summary>

`rank` gives 1, 1, 3 and `dense_rank` gives 1, 1, 2. After a tie, `rank` skips the numbers the tied rows used.

</details>

3\. Return the number of signups per month, and a running total. Columns: `month` (text like `2025-01`), `signups`, `total_signups`. Sorted by month. Expected: 20 rows, starting 70, 41, 32 with totals 70, 111, 143.

<div class="sql-runner" data-db="events" data-solution="sol-quiz-3" markdown>

```sql
-- write your query here
SELECT 1;
```

</div>

<details class="solution" id="sol-quiz-3" markdown>
<summary>Solution</summary>

```sql
SELECT to_char(date_trunc('month', occurred_at), 'YYYY-MM') AS month,
       count(*) AS signups,
       sum(count(*)) OVER (ORDER BY date_trunc('month', occurred_at)) AS total_signups
FROM events
WHERE event_type = 'signup'
GROUP BY date_trunc('month', occurred_at)
ORDER BY month;
```

The window `sum` runs after `GROUP BY`, so it adds up the monthly counts.

</details>

4\. Return each user's first purchase date. Columns: `user_id`, `first_purchase` (text `YYYY-MM-DD`), sorted by `user_id`. Expected: 134 rows, starting with user 2 on 2025-03-26.

<div class="sql-runner" data-db="events" data-solution="sol-quiz-4" markdown>

```sql
-- write your query here
SELECT 1;
```

</div>

<details class="solution" id="sol-quiz-4" markdown>
<summary>Solution</summary>

```sql
SELECT user_id, first_purchase
FROM (
  SELECT user_id, to_char(occurred_at, 'YYYY-MM-DD') AS first_purchase,
         row_number() OVER (PARTITION BY user_id ORDER BY occurred_at) AS rn
  FROM events
  WHERE event_type = 'purchase'
) t
WHERE rn = 1
ORDER BY user_id;
```

`min(occurred_at) ... GROUP BY user_id` gives the same dates; the window version also lets you keep other columns of that row.

</details>

## Lab

<div class="lab" markdown>

### Lab: three window tasks on events

Goal: use `lag`, `dense_rank` and a share-of-total window. Time: about 20 minutes. Runs in: the browser.

1. Task 1. For each user, find the longest gap in whole days between two consecutive events (use `occurred_at::date` and `lag`). Return `user_id` and `max_gap_days` for the top 3, largest first, then by `user_id`. Users with one event have a `NULL` gap and must come last. Expected: users 232, 75 and 50 with 37, 35 and 31 days.
2. Task 2. Return the top 2 users per plan by number of `page_view` events, keeping ties (`dense_rank`). Columns: `plan`, `user_id`, `views`. Sorted by `plan`, `views` descending, `user_id`. Expected: 6 rows, with `free` led by user 26 with 31 views.
3. Task 3. For each month's purchases, return `month` (a date), `purchases` and `pct` (the month's share of all purchases, rounded to 1 decimal), highest `pct` first, limit 3. Expected: 2025-02 at 15.9, 2025-03 at 15.0, 2025-04 at 11.0.

<div class="sql-runner" data-db="events" data-solution="sol-lab-1" markdown>

```sql
-- task 1
SELECT 1;
```

</div>

<details class="solution" id="sol-lab-1" markdown>
<summary>Solution</summary>

```sql
SELECT user_id, max(gap) AS max_gap_days
FROM (
  SELECT user_id,
         occurred_at::date - lag(occurred_at::date) OVER (PARTITION BY user_id ORDER BY occurred_at) AS gap
  FROM events
) g
GROUP BY user_id
ORDER BY max_gap_days DESC NULLS LAST, user_id
LIMIT 3;
```

</details>

<div class="sql-runner" data-db="events" data-solution="sol-lab-2" markdown>

```sql
-- task 2
SELECT 1;
```

</div>

<details class="solution" id="sol-lab-2" markdown>
<summary>Solution</summary>

```sql
WITH views AS (
  SELECT u.plan, e.user_id, count(*) AS views
  FROM events e JOIN users u USING (user_id)
  WHERE e.event_type = 'page_view'
  GROUP BY u.plan, e.user_id
), ranked AS (
  SELECT *, dense_rank() OVER (PARTITION BY plan ORDER BY views DESC) AS r FROM views
)
SELECT plan, user_id, views
FROM ranked WHERE r <= 2
ORDER BY plan, views DESC, user_id;
```

</details>

<div class="sql-runner" data-db="events" data-solution="sol-lab-3" markdown>

```sql
-- task 3
SELECT 1;
```

</div>

<details class="solution" id="sol-lab-3" markdown>
<summary>Solution</summary>

```sql
WITH monthly AS (
  SELECT date_trunc('month', occurred_at)::date AS month, count(*) AS purchases
  FROM events WHERE event_type = 'purchase' GROUP BY 1
)
SELECT month, purchases, round(100.0 * purchases / sum(purchases) OVER (), 1) AS pct
FROM monthly ORDER BY pct DESC LIMIT 3;
```

</details>

Expected result: all three tasks show "matches".

</div>

## Where this shows up

- Dashboards: running totals, month-over-month change with `lag`, "latest row per customer" and "top N per category".
- Window functions also run over time-ordered data in time-series queries and in data warehouses<!-- link: ../../11-data-engineering-and-data-science/01-data-engineering/01-oltp-vs-olap-and-warehouses.md -->.
- [Indexes](../04-postgres-in-depth/01-indexes.md) on the `PARTITION BY` and `ORDER BY` columns can avoid a sort.
