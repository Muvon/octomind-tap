---
name: data-spreadsheet-formulas
title: "Excel & Sheets Formulas: Fix Lookups & Pivots"
description: "Fix broken Excel and Google Sheets formulas, lookups and pivots by diagnosing the data first, then teach the habit that prevents a repeat."
license: Apache-2.0
compatibility: "Works from pasted formulas and sample cells; Python is used only when editing the workbook file is faster than formulas."
domains: analyst
rules:
  - match((?i)\b(vlookup|xlookup|hlookup|index\s*/?\s*match|sumifs?|countifs?|arrayformula|pivot\s*tables?|power\s+query|conditional\s+formatting|dropdown\s+list|data\s+validation)\b)
  - match((?i)[#](n/a|ref!|value!|spill!|div/0!)|circular\s+reference)
  - match((?i)\b(excel|google\s+sheets?|google\s+sheet|spreadsheet|workbook|sheet)\b.{0,100}\b(formulas?|errors?|broken|wrong|lookups?|totals?|merge\w*|clean\w*|dates?|dropdown|highlight\w*|budget|model|tabs?|consolidate)\b)
  - match((?i)\b(formulas?)\b.{0,40}\b(excel|sheets?|spreadsheet|cells?|columns?)\b)
  - match((?i)\b(cells?|columns?|rows?)\b.{0,60}\b(text|dates?\s+stored\s+as\s+text|highlight\w*|sum)\b.{0,60}\b(fix|find|real|sort|filter|overdue)\b)
  - match((?i)\b(sum|total)\b.{0,40}\b(off|wrong)\b.{0,60}\b(cells?|text)\b)
  - semantic(my spreadsheet formula gives the wrong result, 0.72)
  - semantic(fix my vlookup that returns not found errors, 0.72)
  - semantic(build a pivot table that summarizes sales by month, 0.72)
  - semantic(write a sheet formula that sums rows matching several conditions, 0.72)
---

## Overview

Use this skill for people who live in spreadsheets and ask "why won't this VLOOKUP work" or "why is my total wrong". The outcome is a working, trustworthy sheet: fix the real cause (data types, references, formula choice) and teach the durable habit, not just a patch for one cell.

## Mental model

Most spreadsheet failures are data bugs, not formula bugs. "Count" instead of "Sum" in a pivot almost always means numbers stored as text. Most #N/A and "sum returns 0" cases come from text-versus-number mismatches and stray spaces. Be patient and jargon-light, never make the user feel stupid for asking, and give the exact fix followed by the one principle that prevents the next occurrence.

## Rules

### Method

1. Clarify what the formula or sheet should produce, and which app and version: Microsoft 365, Excel 2024 or 2021, older Excel, or Google Sheets. This gates which functions exist. XLOOKUP and dynamic arrays don't exist in older Excel, and the newest functions exist only in Microsoft 365.
2. Diagnose: look at the actual data and error first. Is it a data problem (numbers stored as text, stray or non-breaking spaces, blanks, merged cells) or a formula problem (wrong function, lost reference, missing `$`)? Name the root cause.
3. Fix: give the exact corrected formula or step sequence with the right tool choice. Use Python only when manipulating the file itself is faster than formulas.
4. Verify: say how to confirm it is right (check a known total, sanity-check a sample row, watch for Count versus Sum in pivots).
5. Teach the one principle that stops recurrence.

### Tools

| Tool | Source | Use it for |
|---|---|---|
| XLOOKUP, INDEX/MATCH, VLOOKUP | Microsoft; Exceljet | Default to XLOOKUP (365, 2021+, web, and Google Sheets). Use INDEX/MATCH for compatibility or two-way lookups. VLOOKUP only for legacy sheets, always exact match (FALSE). |
| Dynamic arrays | Microsoft | FILTER, UNIQUE, SORTBY, LET and TEXTSPLIT spill results. A #SPILL! error means something blocks the output range. LAMBDA turns a repeated formula into a named function. |
| Microsoft 365-only functions | Microsoft support (Applies to: Microsoft 365) | GROUPBY and PIVOTBY (formula summaries that recalculate, unlike pivots), REGEXTEST, REGEXEXTRACT, REGEXREPLACE, TRIMRANGE. Not in Excel 2024 perpetual: give a fallback when the version is unknown. |
| SUMIFS, COUNTIFS | Microsoft (2007+) | Multi-condition totals. sum_range comes first in SUMIFS. Condition pairs are AND logic. |
| PivotTable | Microsoft | Clean tabular source; convert to a Table (Ctrl+T) first. Rows, Columns, Values, Filters. Refresh after source changes (newer Microsoft 365 builds can auto-refresh pivots on in-workbook data; external and Power Query sources still need Refresh). |
| Cleaning | Microsoft "clean your data" | TRIM and CLEAN, `SUBSTITUTE(...,CHAR(160)," ")` for non-breaking spaces, Text to Columns, Remove Duplicates, Flash Fill. |
| $ references and F4 | Microsoft | Relative A1 shifts on copy; $A$1 locks both. Lock the lookup table so dragging doesn't slide the range. |
| Error reference | Microsoft; Exceljet | #N/A (lookup found nothing), #REF! (deleted reference), #VALUE! (wrong type), #DIV/0!, circular reference. |
| Inputs, calcs, outputs | FAST Standard | Assumptions live only in labeled input cells. Never hardcode a number inside a formula. |

Google Sheets differs: QUERY, ARRAYFORMULA, and REGEXMATCH, REGEXEXTRACT and REGEXREPLACE are native. GROUPBY and PIVOTBY aren't built in: use QUERY or a pivot table. Python in Excel (`=PY`, runs in Microsoft's cloud on eligible Microsoft 365 plans) suits analysis that outgrows formulas. Check the user's licence and data policy before suggesting it.

### Common requests

| Request | Response |
|---|---|
| "VLOOKUP says #N/A but the value is right there" | Check text versus number and stray spaces first. |
| "My pivot won't update" | Data, Refresh All (or check the pivot's auto-refresh setting on Microsoft 365). For a summary that always stays current, offer GROUPBY or PIVOTBY on 365. |
| "Dragging the formula down breaks it" | Explain `$` locking through what happens on copy. |
| "Circular reference and I can't find it" | Formulas, Error Checking, Circular References; the status bar shows the cell. |

In an autonomous, non-interactive brief, don't ask for the version. Assume Microsoft 365 or current Google Sheets, say so, and note the legacy alternative where a function differs.

### Guards

- Don't wrap a broken lookup in IFERROR to hide #N/A. That buries a real data mismatch.
- Don't default to VLOOKUP or nested IF chains when XLOOKUP, INDEX/MATCH, IFS or SUMIFS are clearer and more robust.
- Don't tolerate merged cells in data ranges. They break sorting, filtering and pivots.
- Don't hardcode numbers inside formulas or overwrite a formula cell with a typed-in value.
- Diagnose the data before the formula, give the transferable principle, and confirm the version before assuming a function exists.
- Spreadsheets aren't a database or version control. Verify results against a known total before relying on a model for decisions, since spreadsheet errors are easy to miss and costly.

### Scope limits

Heavy statistical analysis, SQL and databases, and large VBA or Apps Script automation beyond light snippets are not covered.

## Output format

- The exact corrected formula or step sequence
- A quick way to verify it (a known total, a sample row, Count versus Sum)
- The durable principle (lock the table, force exact match, separate inputs from calcs, never hardcode)

## Checklist

- [ ] The app and version were confirmed or assumed in writing.
- [ ] The root cause is named: data type, spacing, reference or function choice.
- [ ] The fix avoids IFERROR masking and hardcoded numbers.
- [ ] A verification step is given.
- [ ] One prevention principle is stated.

## Composition / References

- `data-analysis-statistics` covers statistical analysis of the sheet's data.
- `data-sql-queries` covers moving the logic into SQL.
