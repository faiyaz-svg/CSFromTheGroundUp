# Spreadsheets

Cheat sheet for the chapter. Lessons: [Excel formulas and references](01-excel-formulas-and-references.md), [Lookups, pivot tables and charts](02-lookups-pivot-tables-and-charts.md), [Spreadsheets, CSV and SQL](03-spreadsheets-csv-and-sql.md).

## References

| Form | Example | When copied |
|---|---|---|
| relative | `D2` | shifts with the formula |
| absolute | `$I$1` | never changes |
| mixed | `$A2`, `A$2` | column or row stays fixed |
| structured | `Sales[Total]`, `[@Qty]` | named table columns |

## Formulas

| Formula | Result on the chapter sheet |
|---|---|
| `=SUM(F2:F9)` | 267.5 |
| `=AVERAGE(F2:F9)` | 33.4375 |
| `=COUNT(F2:F9)` | 8 |
| `=COUNTIF(B2:B9,"East")` | 3 |
| `=SUMIF(B2:B9,"East",F2:F9)` | 67.5 |
| `=SUMIFS(F2:F9,B2:B9,"East",C2:C9,"Widget")` | 37.5 |
| `=IF(F2>=50,"big","small")` | small |
| `=IFS(F2>=50,"big",F2>=20,"mid",TRUE,"small")` | mid |
| `=IFERROR(x,0)` | 0 if `x` errors |
| `=ROUND(F2*(1+$I$1),2)` | 28.25 |
| `=XLOOKUP(B2,$M$2:$M$4,$N$2:$N$4,"not found")` | Ana |
| `=VLOOKUP(B2,$M$2:$N$4,2,FALSE)` | Ana |
| `=INDEX($N$2:$N$4,MATCH(B2,$M$2:$M$4,0))` | Ana |
| `=SORT(UNIQUE(C2:C9))` | Gadget, Gizmo, Widget |
| `=FILTER(A2:F9,B2:B9="West")` | 3 rows |

## Errors

| Error | Meaning |
|---|---|
| `#DIV/0!` | division by zero |
| `#N/A` | lookup found no match |
| `#REF!` | referenced cells deleted |
| `#VALUE!` | wrong type, often a number stored as text |
| `#SPILL!` | a dynamic array's spill range is blocked |

## Pivot table and charts

Rows and Columns choose the groups, Values chooses the aggregate (Sum, Count, Average), Filters slices. Refresh after the source changes. Bar for comparing categories, line for time, scatter for two numbers, histogram for spread.

## CSV and SQL

- Export as CSV UTF-8. Import with Text column types to protect leading zeros, long IDs and gene names such as `SEPT2`.
- Use ISO dates (`2026-03-04`) in files.
- `COPY t FROM 'file' (FORMAT csv, HEADER)` reads on the server; psql `\copy` reads on your machine.
- `SUMIFS` by region, a pivot with Region in Rows, `SELECT region, SUM(x) FROM t GROUP BY region` and a dict with `+=` in Python all compute the same thing.
