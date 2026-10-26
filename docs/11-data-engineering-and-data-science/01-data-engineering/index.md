# Data engineering

A compact reference for the ten lessons of this chapter. The sample database is `warehouse` (a star schema: `fact_sales` and four dimensions). No new teaching here; follow the lesson links for the explanations.

## Lessons

| # | Lesson | One line |
|---|---|---|
| 1 | [OLTP vs OLAP and warehouses](01-oltp-vs-olap-and-warehouses.md) | Short transactions on a few rows versus big scans for analysis. |
| 2 | [Star schemas and dimensional modelling](02-star-schemas-and-dimensional-modelling.md) | One fact table at a chosen grain, surrounded by dimensions. |
| 3 | [ETL and ELT pipelines](03-etl-and-elt-pipelines.md) | Extract, transform, load, or load raw first and transform in the warehouse. |
| 4 | [Loading data into Postgres](04-loading-data-into-postgres.md) | `COPY` into staging, then upsert into the real table. |
| 5 | [Batch and streaming](05-batch-and-streaming.md) | Process a window of data at once, or each event as it arrives. |
| 6 | [Orchestration and idempotent jobs](06-orchestration-and-idempotent-jobs.md) | DAGs of tasks, retries, backfills, and writes that are safe to repeat. |
| 7 | [dbt and SQL transformations](07-dbt-and-sql-transformations.md) | Each model is a `SELECT`; `ref()` builds the graph; tests return bad rows. |
| 8 | [File formats and columnar storage](08-file-formats-and-columnar-storage.md) | Parquet is smaller and lets queries read only what they need. |
| 9 | [Data quality](09-data-quality.md) | Count rule violations after the load and stop the run if any are found. |
| 10 | [Lakes, lakehouses and cloud warehouses](10-lakes-lakehouses-and-cloud-warehouses.md) | Open files plus a table format; storage and compute billed separately (optional). |

## Terms

| Term | Meaning |
|---|---|
| OLTP | Many short transactions touching a few rows; normalized, row-oriented. |
| OLAP | Fewer, larger queries that scan and aggregate many rows; often column-oriented. |
| Data warehouse | Database of history copied from source systems, organized for analysis. |
| Fact table | Events with numeric measures, at a declared grain. |
| Dimension table | Descriptive context (who, what, where, when) joined to facts. |
| Grain | What one row of the fact table means. |
| Surrogate key | Meaningless integer key made by the warehouse; the source id is the business key. |
| Slowly changing dimension | A dimension whose attributes change over time; type 2 keeps a new row per version. |
| ETL / ELT | Transform before loading, or load raw data and transform inside the warehouse. |
| Staging | Where raw data lands first, unchanged. |
| Batch / streaming | Process a bounded window at once, or process events continuously. |
| CDC | Change data capture: database changes published as a stream of events. |
| Topic, partition, offset | Kafka: a named log, its ordered slices, and a record's position in a partition. |
| DAG | Tasks with one-way dependencies and no cycles. |
| Logical date | The slice of time a run's data belongs to, not when it ran. |
| Backfill | Running a job for past logical dates. |
| Idempotent | Running once or many times gives the same final state. |
| Model (dbt) | A `.sql` file with one `SELECT`; dbt builds it as a view or table. |
| Materialization | How dbt stores a model: view, table, incremental, ephemeral. |
| Column pruning | Reading only the columns a query uses. |
| Predicate pushdown | Skipping chunks or folders that cannot match the `WHERE` filter. |
| Reconciliation | Comparing the same figure (rows, sums) in two places. |
| Lakehouse | Open files on object storage plus a table format and SQL engine. |
| Table format | Metadata that tracks which files make up a table: Delta Lake, Apache Iceberg. |

## SQL and commands

Rollups on the star schema (lesson 2):

<!-- db: warehouse -->
```sql
SELECT d.year, p.category, sum(f.net_amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY ROLLUP (d.year, p.category)
ORDER BY d.year, p.category;
```

Upsert by key (lessons 4 and 6):

<!-- db: warehouse -->
```sql
CREATE TABLE totals (date_key integer PRIMARY KEY, revenue numeric(12,2));
INSERT INTO totals
SELECT date_key, sum(net_amount) FROM fact_sales GROUP BY date_key
ON CONFLICT (date_key) DO UPDATE SET revenue = EXCLUDED.revenue;
SELECT count(*) FROM totals;
```

Bulk load (lesson 4; needs a Postgres server, so it does not run in the browser):

```sql
COPY staging_orders FROM '/path/orders.csv' WITH (FORMAT csv, HEADER true);
```

To replace one partition (lesson 6), run `DELETE ... WHERE date_key = :d;` then `INSERT ... WHERE date_key = :d;`, both in one transaction. `MERGE INTO t USING s ON ... WHEN MATCHED ... WHEN NOT MATCHED ...` needs PostgreSQL 15 or later.

dbt (lesson 7):

| Command or file | What it does |
|---|---|
| `dbt run` | Build the models in dependency order. |
| `dbt test` | Run the tests; zero returned rows means pass. |
| `dbt build` | Run and test together, in order. |
| `dbt docs generate` | Write the docs site with the lineage graph. |
| `ref('m')`, `source('s', 't')` | Refer to a model, or to a raw table (inside `{{ }}`). |
| `unique`, `not_null`, `accepted_values`, `relationships` | The four built-in tests. |

## Quality checks

| Dimension | Example check (count the violations) |
|---|---|
| Completeness | `WHERE col IS NULL`; row count equals the source. |
| Validity | `WHERE quantity NOT BETWEEN 1 AND 100`. |
| Uniqueness | `GROUP BY key HAVING count(*) > 1`. |
| Consistency | `LEFT JOIN dim ... WHERE dim.key IS NULL` finds orphans. |
| Freshness | `max(loaded_at)` is recent enough. |

## File formats

| Format | Layout | Schema in file | Typical use |
|---|---|---|---|
| CSV | Rows, text | No | Exports, spreadsheets |
| JSON lines | Rows, text | Field names per row | Logs, API dumps |
| Avro | Rows, binary | Yes | Kafka messages |
| Parquet | Columns, binary | Yes | Analytics, lakes |

On one million generated orders (lesson 8, `pyarrow` 26.0.0): CSV 34.7 MB, Parquet with snappy 10.0 MB, with zstd 6.8 MB; reading one column took 5 ms against 36 ms for all five. Partition folders are named `column=value`, such as `year=2026/month=01/`.

## Rules to remember

1. Declare the grain before you design a fact table.
2. A task must be safe to run twice: write by partition (delete-insert) or by key (upsert), in one transaction.
3. Use the logical date, never `now()`, inside a task.
4. Check the data in staging and stop the run on failure; a finished job is not a correct job.
5. Name only the columns you need; partition by a column that queries filter on and that has few distinct values.
6. Prices, versions and free tiers change; read the vendor's current page.
