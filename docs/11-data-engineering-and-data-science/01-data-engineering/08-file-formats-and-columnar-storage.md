# File formats and columnar storage

After this you can choose between CSV, JSON lines, Parquet and Avro, and explain why a query on a Parquet file reads less data than the same query on a CSV file.

Before this: [OLTP vs OLAP and warehouses](01-oltp-vs-olap-and-warehouses.md).

## The idea

An analytics question usually touches few columns of many rows: "total `amount` by `province`" over 100 million orders. A row-oriented file such as CSV stores each order together, so to read `amount` you must scan past every other field of every row. A column-oriented file stores all `amount` values together, so the reader fetches only the columns the query names.

```text
Row layout (CSV, Avro, a Postgres table page)
  [id=1 | ON | 25.00 | 2026-01-01] [id=2 | BC | 40.00 | 2026-01-02] [id=3 | ON | 10.00 | 2026-01-01] ...

Column layout (Parquet, ORC)
  id:     [1, 2, 3, ...]
  prov:   [ON, BC, ON, ...]      <- similar values sit together, so they compress well
  amount: [25.00, 40.00, 10.00, ...]   <- a query on amount reads only this line
  date:   [2026-01-01, 2026-01-02, 2026-01-01, ...]
```

In the drawing, a row layout reads every bracket to answer a question about one field; the column layout reads one line. The cost is that rebuilding one whole row means touching every column, which is why OLTP databases favour rows and analytics stores favour columns, as in [OLTP vs OLAP](01-oltp-vs-olap-and-warehouses.md).

## Key terms

A **file format** defines how records are laid out as bytes in a file. A **schema** names each field and gives its type; a format either carries the schema inside the file or leaves it out.

**CSV** is text with one record per line and comma-separated fields. It has no types (everything is text until a reader guesses), no standard for quoting, and no schema in the file.

**JSON lines** (also called NDJSON) is one JSON object per line. It carries field names on every row and allows nested data, so it is larger than CSV but flexible. It is common for event logs and API exports.

**Parquet** is an open columnar format. A file is split into **row groups**; inside each, each column is stored as a compressed chunk, with a schema and per-chunk statistics (minimum, maximum, null count) in the footer ([Parquet docs](https://parquet.apache.org/docs/)).

**Avro** is an open row-based binary format that stores its schema with the data and supports schema evolution. It is common for Kafka messages, where records are written and read one at a time ([Avro docs](https://avro.apache.org/docs/)).

**Column pruning** means reading only the columns a query uses. **Predicate pushdown** means using the statistics (or partition folders) to skip chunks that cannot match the `WHERE` filter.

**Partitioning** splits a dataset into folders by a column's value, such as `province=ON/` or `year=2026/month=01/`. A query that filters on that column reads only the matching folders. The `key=value` folder naming is called Hive-style.

## How it works

Parquet gets small files and fast column reads from three things. Values of one column are alike, so **encoding** (dictionary encoding turns repeated strings into small integers) and **compression** (snappy is fast, zstd is smaller and slower) work well. Each column chunk is read on its own, giving column pruning. And chunk statistics in the footer let a reader skip a row group whose maximum is below the filter value.

Partition columns work one level up. Choose a column that queries filter on and that has few distinct values. A partition on `customer_id` with 50,000 values would create 50,000 tiny folders, and listing and opening files then costs more than the data.

## Worked examples

<div class="example" markdown>

### Example 1: CSV vs Parquet on 1 million rows

We generated one million orders (`order_id`, `customer_id`, `province`, `amount`, `order_date`) with a fixed seed and wrote them three ways using `pyarrow` 26.0.0 on a Windows laptop.

1. Write `orders.csv`, `orders.parquet` (snappy) and `orders_zstd.parquet`, then compare file sizes.
2. Time reading all columns, then only `amount`, taking the best of 3 runs.
3. Write a copy partitioned by `province` and read one province.

<details class="code" markdown>
<summary>In code</summary>

```python
import numpy as np, pyarrow as pa, pyarrow.csv as pacsv
import pyarrow.parquet as pq, pyarrow.dataset as ds

rng = np.random.default_rng(42)
n = 1_000_000
table = pa.table({
    "order_id": np.arange(n),
    "customer_id": rng.integers(1, 50_000, n),
    "province": rng.choice(["ON", "QC", "BC", "AB", "MB"], n),
    "amount": np.round(rng.gamma(2.0, 30.0, n), 2),
    "order_date": (np.datetime64("2025-01-01") + rng.integers(0, 365, n)).astype("datetime64[D]"),
})
pacsv.write_csv(table, "orders.csv")
pq.write_table(table, "orders.parquet", compression="snappy")
pq.write_table(table, "orders_zstd.parquet", compression="zstd")

only_amount = pq.read_table("orders.parquet", columns=["amount"])
bc = pq.read_table("orders.parquet", columns=["province", "amount"],
                   filters=[("province", "=", "BC")])
ds.write_dataset(table, "part", format="parquet", partitioning=ds.partitioning(
    pa.schema([("province", pa.string())]), flavor="hive"))
```

</details>

```text
orders.csv                34.7 MB
orders.parquet            10.0 MB
orders_zstd.parquet        6.8 MB
CSV: read all columns                               33 ms
Parquet: read all columns                           36 ms
Parquet: read only 'amount'                          5 ms
Parquet: filter province='BC', 2 cols               30 ms
['province=AB', 'province=BC', 'province=MB', 'province=ON', 'province=QC']
rows read for BC: 200854  total: 1000000
```

Check: Parquet is 3.5 times smaller than CSV with snappy (34.7 / 10.0) and 5.1 times smaller with zstd. Reading all columns takes about the same time in both (pyarrow's CSV reader is multi-threaded and fast; Parquet still has to decode), so the speed gain comes from reading less: one column took 5 ms, about 7 times faster than all five. The BC filter did not speed things up here because this file has a single row group whose statistics span AB to QC, so nothing could be skipped. The partitioned copy read only the `province=BC` folder, 200,854 of the million rows. Your times will differ; the ratios are what matter.

</div>

<div class="example" markdown>

### Example 2: choosing a format

A service emits click events, one at a time, to Kafka: use Avro or JSON with a schema. A nightly export for a spreadsheet user: CSV. A 5 GB history of orders for analysts: Parquet, partitioned by month. Raw API responses you want to keep unchanged: JSON lines, then convert to Parquet downstream.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: opening a CSV and trusting the column types. A zip code `02134` becomes the number 2134, and a column of dates may be read as text. Give the reader an explicit schema, or use a format that stores one.

</div>

<div class="warning" markdown>

Watch out: many tiny Parquet files. Each file has a footer to open and read, so a million 10 KB files is much slower than a hundred 100 MB ones. Write fewer, larger files, and partition by a low-cardinality column.

</div>

<div class="warning" markdown>

Watch out: `SELECT *` on a columnar file. It reads every column and removes the advantage. Name the columns you need.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: columnar, row group, column pruning, predicate pushdown, partitioning, Hive-style, snappy, zstd, schema evolution.

Prompts to try:

- "I have 200 GB of JSON lines events with fields ts, user_id, event, payload. Propose a Parquet layout in S3: partition columns, target file size, compression, and say what each choice costs."
- "This pyarrow code reads a CSV, filters, and writes Parquet: [paste]. Add an explicit schema and write it partitioned by year and month."

What to check:

- Partition columns with thousands of distinct values (too many small files).
- Invented pyarrow arguments. Compare calls with the [pyarrow docs](https://arrow.apache.org/docs/python/parquet.html).
- Performance claims with no measurement. Time a sample of your own data.
- Dates and decimals: confirm the schema types after a round trip.

</div>

## Quiz

1\. Why does a columnar file compress better than a row file of the same data?

<details class="solution" markdown>
<summary>Answer</summary>

Values in one column have the same type and are often repeated or close together (a `province` column has five distinct values), so dictionary encoding and compression find more redundancy than in rows that mix types.

</details>

2\. A query is `SELECT sum(amount) FROM orders WHERE province = 'BC'` on data partitioned by `province` in Parquet. Which two things does the engine skip?

<details class="solution" markdown>
<summary>Answer</summary>

The folders for the other provinces (partition pruning), and the columns other than `amount` and `province` (column pruning).

</details>

3\. In Example 1, reading the whole Parquet file took 36 ms and the CSV 33 ms. Is Parquet slower?

<details class="solution" markdown>
<summary>Answer</summary>

Not in a meaningful sense: when all columns are read, the work is about the same, and Parquet must decode. Its advantage shows when you read fewer columns (5 ms) or can skip data. The file is also 3.5 times smaller, which matters for storage and network.

</details>

4\. Which format suits a Kafka topic of individual events whose fields will change over time, and why?

<details class="solution" markdown>
<summary>Answer</summary>

Avro. It is row-based, so each event is written whole, and it carries a schema and supports schema evolution (adding fields with defaults).

</details>

## Lab

<div class="lab" markdown>

### Lab: measure CSV against Parquet

Goal: reproduce the size and read-time comparison with your own data. Time: about 15 minutes. Runs in: WSL (Ubuntu) or any shell with Python (the example above ran on Windows).

1. Create a virtual environment and run `pip install pyarrow numpy`.
2. Build the table from Example 1 with 500,000 rows.
3. Write CSV, snappy Parquet and zstd Parquet, and print each file size.
4. Time `pq.read_table(..., columns=["amount"])` against reading all columns.
5. Write a partitioned copy by `province` and list the folders.
6. Cleanup: delete the files and the virtual environment.

Expected result: Parquet files several times smaller than the CSV, and the one-column read several times faster than the all-column read.

<details class="solution" markdown>
<summary>Solution</summary>

Use the code in Example 1 with `n = 500_000`. Time each read with `time.perf_counter()` around the call, and print `os.path.getsize(path) / 1e6`.

</details>

</div>

## Where this shows up

- [Lakes, lakehouses and cloud warehouses](10-lakes-lakehouses-and-cloud-warehouses.md): Parquet files in object storage are the base of a data lake.
- [Batch and streaming](05-batch-and-streaming.md): Avro and JSON are the usual message formats in Kafka.
