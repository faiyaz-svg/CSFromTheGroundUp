# Excel formulas and references

After this you can write Excel formulas that copy correctly, summarise rows with SUMIFS and COUNTIFS, and read the four common error codes.

Before this: [Data formats: JSON, YAML and CSV](../02-project-plumbing/03-data-formats-json-yaml-csv.md).

## The idea

Someone in finance sends you `sales.xlsx` and asks for totals by region. A spreadsheet is a grid of cells, and each cell holds either a value or a formula that computes one. You can think of it as a program where every variable is a cell and the "assignment" re-runs whenever an input changes.

We use one small sheet through this chapter: eight sales rows, with `Total` computed from `Qty` and `Price`, and a tax rate stored once in `I1`.

```text
      A           B       C        D    E      F       G          H    I
1     Date        Region  Product  Qty  Price  Total   With tax   Tax  0.13
2     2026-01-05  East    Widget   10   2.50   25.00   28.25
3     2026-01-07  West    Gadget    4  10.00   40.00   45.20
4     2026-01-12  East    Gadget    3  10.00   30.00   33.90
5     2026-02-02  West    Widget    8   2.50   20.00
6     2026-02-09  East    Widget    5   2.50   12.50
7     2026-02-15  North   Gadget    6  10.00   60.00
8     2026-03-01  West    Gizmo     2  25.00   50.00
9     2026-03-04  North   Widget   12   2.50   30.00
```

Column letters and row numbers give each cell an address such as `D2`. In the diagram, `F2` holds `=D2*E2` and `G2` holds `=ROUND(F2*(1+$I$1),2)`.

## Key terms

A **cell reference** names a cell (`D2`) and a **range** names a block of cells (`D2:D9`). A **formula** starts with `=` and combines values, references and functions.

A **relative reference** (`D2`) changes when you copy the formula to another cell. An **absolute reference** (`$I$1`) never changes. A **mixed reference** fixes only the column (`$A2`) or only the row (`A$2`). See Microsoft's page on [relative, absolute and mixed references](https://support.microsoft.com/en-us/office/switch-between-relative-absolute-and-mixed-references-dfec08cd-ae65-4f56-839e-5f0d8d0baca9). Pressing F4 while editing a reference cycles through the four forms.

## How it works

When you copy a formula, Excel keeps the formula's offset from its own cell, not the literal address. Copy `F2` down one row and `D2` becomes `D3`, because "two columns left, same row" still holds.

```text
Formula in F2:   =D2*E2                  (relative)
Copied to F3:    =D3*E3                  (shifts down 1 row)

Formula in G2:   =ROUND(F2*(1+$I$1),2)   ($I$1 absolute)
Copied to G3:    =ROUND(F3*(1+$I$1),2)   (F shifts, $I$1 stays)

Mixed:   =$A2*B$1  copied one right and one down  ->  =$A3*C$1
```

Without the dollar signs, `G3` would point at `I2`, which is empty, and every total would be wrong without any error showing.

The functions you meet most, run on the sheet above:

| Formula | Result | What it does |
|---|---|---|
| `=SUM(F2:F9)` | 267.5 | add numbers |
| `=AVERAGE(F2:F9)` | 33.4375 | mean |
| `=COUNT(F2:F9)` | 8 | count numeric cells |
| `=COUNTIF(B2:B9,"East")` | 3 | rows where Region is East |
| `=SUMIF(B2:B9,"East",F2:F9)` | 67.5 | sum Total where Region is East |
| `=SUMIFS(F2:F9,B2:B9,"East",C2:C9,"Widget")` | 37.5 | several conditions, sum range first |
| `=COUNTIFS(B2:B9,"West",A2:A9,">="&DATE(2026,2,1))` | 2 | several conditions |
| `=ROUND(AVERAGE(F2:F9),1)` | 33.4 | round to 1 decimal |
| `=IF(F2>=50,"big","small")` | small | one test |
| `=IFS(F2>=50,"big",F2>=20,"mid",TRUE,"small")` | mid | first true test wins |
| `=IFERROR(F2/D2,0)` | 2.5 | value, or 0 if the formula errors |

The single-condition `SUMIF` puts the sum range last, while `SUMIFS` puts it first ([SUMIFS](https://support.microsoft.com/en-us/office/sumifs-function-c9e748f5-7ea7-455d-9406-611cebce642b), [COUNTIF](https://support.microsoft.com/en-us/office/countif-function-e0de10c6-f885-4e71-abb4-1f464816df34), [IFS](https://support.microsoft.com/en-us/office/ifs-function-36329a26-37b2-467c-972b-4a39bd951d45), [IFERROR](https://support.microsoft.com/en-us/office/iferror-function-c526fd07-caeb-47b8-8bb6-63f3e417f611)). Build date criteria with `DATE(...)` as shown, because a typed date string is read according to your locale.

Text and date functions work the same way: `=UPPER(TRIM(B2))`, `=LEFT(C2,3)` ("Wid"), `=B2&"-"&C2` ("East-Widget"), `=TEXT(A2,"mmm yyyy")`, `=MONTH(A2)`, `=EOMONTH(A2,0)`. A date is a serial number (days since 1899-12-30), so `2026-01-05` is 46027 and `=A9-A2` gives 58 days.

An **Excel table** (Insert, Table) gives the range a name and lets formulas use column names, called **structured references**: `=SUM(Sales[Total])`, or `=[@Qty]*[@Price]` inside the table's own row. Tables grow when you add rows, so formulas don't need their ranges edited ([structured references](https://support.microsoft.com/en-us/office/using-structured-references-with-excel-tables-f5ed2452-2337-4f71-bed3-c8ae6d2b276e)).

Four error codes cover most failures:

| Error | Meaning | Typical cause |
|---|---|---|
| `#DIV/0!` | division by zero | `=F2/D2` where `D2` is 0 or empty |
| `#N/A` | no match found | a lookup that doesn't find its key |
| `#REF!` | the reference is gone | you deleted a row or column the formula used |
| `#VALUE!` | wrong type of value | `=D2+"abc"`, or a number stored as text |

Google Sheets uses the same function names for everything in this lesson. Its `IFS` and `SUMIFS` match Excel's argument order.

## Worked examples

<div class="example" markdown>

### Example 1: a tax column and a region total

We want the East total (67.5) and the tax-inclusive total of row 2.

1. Click `G2` and type `=ROUND(F2*(1+$I$1),2)`. The result is 28.25.
2. Drag the fill handle down to `G4`. `G3` becomes `=ROUND(F3*(1+$I$1),2)` and shows 45.20.
3. In a free cell type `=SUMIF(B2:B9,"East",F2:F9)`. The result is 67.5.
4. Type `=F2/COUNTIF(B2:B9,"South")`. No row has region South, so this divides by 0 and shows `#DIV/0!`. Wrapping it as `=IFERROR(F2/COUNTIF(B2:B9,"South"),0)` shows 0.

Check by recomputing outside Excel:

```python
rows = [("East", 10, 2.5), ("West", 4, 10), ("East", 3, 10), ("West", 8, 2.5),
        ("East", 5, 2.5), ("North", 6, 10), ("West", 2, 25), ("North", 12, 2.5)]
totals = [q * p for _, q, p in rows]
print(sum(totals), sum(t for (r, _, _), t in zip(rows, totals) if r == "East"))
print(round(totals[0] * 1.13, 2))
```

```text
267.5 67.5
28.25
```

Excel's `ROUND` rounds halves away from zero, so `=ROUND(2.5,0)` is 3. Python's `round(2.5)` is 2 (banker's rounding), so a Python check of rounded values can differ at exact halves.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: forgetting `$` on a constant such as a tax rate. The copied formula points at an empty cell and silently multiplies by 0. Check one copied formula by clicking it, not just the first one.

Watch out: whole-number looking values that are text. `SUM` ignores text cells, so a column of numbers pasted from a CSV can sum to less than it should. Left-aligned numbers are the clue.

Watch out: hiding errors with `IFERROR` everywhere. It also hides a real `#REF!`. Wrap only the cell where an error is expected.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: relative reference, absolute reference, mixed reference, SUMIFS, structured reference, table, `#N/A`.

Prompts to try:

- "My column G formula `=F2*(1+I1)` gives wrong totals after I fill down. Explain why in terms of relative and absolute references and give the fixed formula."
- "Write a SUMIFS formula for an Excel table named Sales: sum Total where Region is West and Date is in February 2026. Use structured references."

What to check:

- Argument order in `SUMIF` versus `SUMIFS` (sum range last or first). AI often mixes them.
- Functions that don't exist in your version (`XLOOKUP`, `FILTER` need Excel 2021 or Microsoft 365).
- Locale: separators are `;` in some locales, and date criteria depend on locale.

</div>

## Quiz

1\. What is the difference between `$A2`, `A$2` and `$A$2` when copied?

<details class="solution" markdown>
<summary>Answer</summary>

`$A2` fixes the column and lets the row change, `A$2` fixes the row and lets the column change, and `$A$2` fixes both.

</details>

2\. In the sheet above, what does `=COUNTIF(B2:B9,"West")` return?

<details class="solution" markdown>
<summary>Answer</summary>

3 (rows 3, 5 and 8).

</details>

3\. `=SUM(F2:F9)` returns 0 after you paste data from a CSV, yet the cells show numbers. What is likely wrong?

<details class="solution" markdown>
<summary>Answer</summary>

The numbers are stored as text, and `SUM` ignores text. Convert them (Text to Columns, or multiply by 1) and check the alignment.

</details>

4\. Which error appears when you delete column E, which `F2` uses?

<details class="solution" markdown>
<summary>Answer</summary>

`#REF!`, because the referenced cells no longer exist.

</details>

## Lab

<div class="lab" markdown>

### Lab: build the sales sheet

Goal: reproduce the sheet and check five results. Time: about 15 minutes. Runs in: Excel or Google Sheets.

1. Type the eight rows into `A1:E9` with the headers. Put `0.13` in `I1`.
2. Fill `F2:F9` with `=D2*E2`, and `G2:G9` with `=ROUND(F2*(1+$I$1),2)`.
3. Compute SUM of `F`, `COUNTIF` for East, `SUMIF` for East, `SUMIFS` for East and Widget, and an `IFS` size label in column `J`.
4. Click `G9` and confirm `$I$1` did not move.

Expected result:

```text
267.5   3   67.5   37.5   G9 = 33.90
```

<details class="solution" markdown>
<summary>Solution</summary>

`G9` is `=ROUND(F9*(1+$I$1),2)`, which is 33.9. The other four values are 267.5, 3, 67.5 and 37.5.

</details>

</div>

## Where this shows up

- The next lesson, [Lookups, pivot tables and charts](02-lookups-pivot-tables-and-charts.md), builds on this sheet.
- Parsing the same file in code: [Data formats: JSON, YAML and CSV](../02-project-plumbing/03-data-formats-json-yaml-csv.md).
