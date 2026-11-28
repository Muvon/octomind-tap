---
name: data-sql-queries
title: "SQL Query Optimization: Join Grain, EXPLAIN, Debugging"
description: "Write, debug and speed up analytical SQL: SQL query optimization by processing order, join grain and sargability. Use for wrong totals or slow queries."
license: Apache-2.0
compatibility: "Works from pasted SQL; a connected SQLite or PostgreSQL database tool allows live schema inspection and read-only runs."
capabilities: database-sqlite database-postgres
rules:
  - match((?i)\b(write|fix|debug|optimi[sz]e|tune|rewrite|review|speed\s+up|convert|make)\s+(my\s+|this\s+|the\s+|a\s+|an\s+)?(\w+\s+){0,3}(queries|query)\b)
  - match((?i)\bquer(y|ies)\b.{0,60}\b(slow|wrong|doubled|duplicat\w+|errors?|no\s+rows|explain|timeout|timing\s+out|inflated|faster|nothing)\b)
  - match((?i)\b(group\s+by|having|window[\s-]functions?|left\s+join|inner\s+join|self[\s-]join|explain\s+analyze|row_number|qualify|sargable|not\s+in|count\s*\(\s*distinct|lag\s*\(|lag[\s-]based|subquery|subqueries|ctes?)\b)
  - match((?i)\b(joins?|joined)\b.{0,80}\b(more\s+rows|row\s+count|double[\s-]counting|inflated|fan[\s-]?out)\b|\b(more|extra)\s+rows\b.{0,60}\bjoin\b)
  - match((?i)\b(rolling|running|month[\s-]over[\s-]month|rank\w*)\b.{0,60}\b(spend|revenue|growth|query)\b|\byear\s*\(\s*\w+\s*\)\s*=)
  - match((?i)\bi\s+need\s+(a|an)\s+(sql|query)\b)
  - semantic(my SQL query returns the wrong numbers, 0.72)
  - semantic(write a query to count users per month with joins, 0.72)
  - semantic(why does my join duplicate rows and inflate the total, 0.72)
  - semantic(speed up this slow analytical query, 0.72)
  - semantic(my query returns no rows and I do not know why, 0.72)
---

## Overview

Use this skill to turn "my query returns wrong numbers, no rows, or is slow" into a correct, readable query the user understands. Reason from logical query processing order, join grain, and sargability instead of guessing. The outcome is the corrected or new query, the root cause in plain words, and a way to verify it.

## Mental model

A query is a pipeline of logical steps, not the order it is written in. Most wrong-number bugs are a join that multiplies rows or a filter in the wrong step. Most slow queries are one costly plan node. Name the dialect first, because syntax and optimizer behavior differ between PostgreSQL, SQLite, DuckDB, MySQL, SQL Server and cloud warehouses.

## Rules

### Method

1. Clarify what the query should return, the dialect and version, and for tuning the table sizes, indexes, and the EXPLAIN or EXPLAIN ANALYZE plan. When a live database is connected (SQLite or PostgreSQL tools), inspect the real schema first and run the query read-only instead of reasoning blind.
2. Correctness bug: trace the query through logical processing order. Check join grain (fan-out), GROUP BY validity, NULL and three-valued-logic traps, and outer-join filter placement. Pinpoint the exact wrong step.
3. Write request: confirm the grain (one row per what), then draft readable SQL. Use CTEs for multi-step logic and window functions for per-group ranking or running totals.
4. Optimize request: read the plan bottom-up, find the costly node (sequential scan, cardinality misestimate, non-sargable filter, runaway nested loop), propose a rewrite, and explain why through the plan.
5. Deliver the corrected or written query, a short root-cause explanation, and a verification step (compare row counts, EXPLAIN ANALYZE before and after).

### Concepts

| Concept | Source | What it means |
|---|---|---|
| Logical processing order | Ben-Gan; SQL standard | FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, ORDER BY. Aliases work in ORDER BY but not WHERE, and window functions can't go in WHERE. |
| Join fan-out and grain | Dimensional-modeling practice | A one-to-many join multiplies rows and inflates SUM and COUNT. Aggregate the child table before joining. |
| GROUP BY rule | SQL functional dependency | Every SELECT column is in an aggregate or in GROUP BY. WHERE filters before aggregation, HAVING after. |
| Window functions | SQL:2003 | func() OVER (PARTITION BY ... ORDER BY ...) keeps rows. Filter on them with QUALIFY where the engine has it (DuckDB, Snowflake, BigQuery, Databricks), otherwise wrap in a CTE and filter on rn = 1. |
| CTE vs subquery | SQL standard; PostgreSQL 12 | Logically equivalent. Not an optimization fence in PostgreSQL 12+ and MySQL 8+, but PostgreSQL still materializes a CTE referenced more than once unless marked NOT MATERIALIZED. |
| Sargability | IBM System R; Winand | Keep the indexed column bare (`col >= '2026-01-01'`, not `YEAR(col) = 2026`) so an index range can be used. |
| EXPLAIN | PostgreSQL docs | Read the plan tree bottom-up. Watch for Seq Scan on big tables, estimate-versus-actual row gaps, and Filter on an indexed column. PostgreSQL 18 shows buffer counts with ANALYZE by default and can skip-scan a composite index without its leading column. |

Traps: a LEFT JOIN silently becomes INNER when a right-table filter sits in WHERE (put it in ON). NOT IN against a nullable subquery can return zero rows (use NOT EXISTS).

### Common requests

| Request | Response |
|---|---|
| "Column must appear in the GROUP BY" | Explain the functional-dependency rule and fix. |
| "My SUM is doubled after a join" | Suspect one-to-many fan-out; aggregate before joining. |
| "WHERE row_number() = 1 errors" | Use QUALIFY if the engine supports it; otherwise move it into a CTE and filter on the rank outside. |
| "Query is slow" | Ask for the EXPLAIN plan, sizes, and indexes before diagnosing. |

In an autonomous, non-interactive brief, don't ask for what a connected database can give you (schema, EXPLAIN). Assume PostgreSQL when the dialect is unstated, and say so in the output.

### Guards

- Don't add DISTINCT to hide duplicate rows. It masks a grain or fan-out bug; fix the join.
- Don't claim a query is slow because of SELECT * or a missing index without reading the actual plan.
- Don't treat CTEs as an optimization fence on PostgreSQL 12+ or MySQL 8+.
- Don't use NOT IN against a subquery that may contain NULLs.
- Before running any UPDATE, DELETE or DROP, test on a copy and use a transaction. This skill writes queries; it does not replace DBA review on production.

### Scope limits

Schema design, DDL and migrations belong to `database-design-and-migrations`. Statistical interpretation of results is a separate job. BI-tool configuration (Power BI, Tableau, Looker, Metabase) is not covered: say so plainly and offer the underlying SQL.

## Examples

Fan-out: orders joined to order_items, then `SUM(orders.total)` doubles revenue.

```sql
-- wrong: orders.total repeats once per item row
SELECT c.region, SUM(o.total) FROM orders o JOIN order_items i ON i.order_id = o.id JOIN customers c ON c.id = o.customer_id GROUP BY c.region;

-- right: aggregate the child first, or do not join it at all
SELECT c.region, SUM(o.total) FROM orders o JOIN customers c ON c.id = o.customer_id GROUP BY c.region;
```

Root cause: the join to order_items changed the grain from one row per order to one row per item.

## Output format

- The corrected or newly written query, formatted and readable
- Root cause: one or two plain sentences naming the exact step that was wrong
- Verify: how to confirm (row-count check, EXPLAIN ANALYZE before and after)
- Dialect and version assumed, plus any data-dependent caveat

## Checklist

- [ ] The dialect is named.
- [ ] Join grain was checked before trusting any SUM or COUNT.
- [ ] The root cause comes from the real plan or a traced step, not from a guess.
- [ ] A verification step is given.
- [ ] No write statement ran without a copy and a transaction.

## Composition / References

- `database-design-and-migrations` covers schema, keys, indexes and migrations.
- `analytical-report` covers presenting query results as a report.
