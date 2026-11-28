---
name: data-engineering-pipelines
title: "ETL Pipeline Design: Idempotent Loads, Data Quality"
description: "Design idempotent ETL pipelines, layered warehouse models, Postgres tuning and data quality checks. Use for ETL, backfills and numbers that look wrong."
license: Apache-2.0
compatibility: "Needs read access to schemas and sample data; a PostgreSQL tool and documentation lookup help but are not required."
capabilities: database-postgres devdocs codesearch-semantic memory-read memory-write
rules:
  - match((?i)\b(build|design|write|create|fix|debug|set\s+up|rework|implement)\s+(an?\s+|the\s+|my\s+|our\s+)?(\w+\s+){0,2}(pipeline|etl|elt|ingestion|data\s+warehouse|warehouse\s+model|incremental\s+load|load\s+job)\b)
  - match((?i)\b(backfill|idempotent|incremental\s+loads?|dbt|sqlmesh|data\s+quality|data\s+freshness|freshness|slowly\s+changing|lineage|medallion|schema[\s-]drift|upsert|reruns?)\b)
  - match((?i)\b(staging|intermediate)\b.{0,80}\b(models?|layers?|transforms?)\b|\bdeclare\b.{0,20}\bgrain\b|\b(star\s+schema|marts?)\b)
  - match((?i)\b(dashboard|table|numbers|report)\b.{0,60}\b(stale|out\s+of\s+date|missing\s+rows|drift(ed)?|don'?t\s+match|look\s+wrong|zero|empty)\b)
  - match((?i)\bpostgres(ql)?\b.{0,100}\b(vacuum|bloat|partition\w*|workload|inserts?|rollup)\b)
  - match((?i)\b(rows?|tables?)\b.{0,60}\b(partition\w*|autovacuum|indexes\s+and\s+partition\w*)\b)
  - match((?i)\b(migration|migrate)\b.{0,60}\b(upstream|vendor|rename\w*)\b|\b(renam\w+|retyp\w+)\b.{0,40}\bcolumns?\b)
  - semantic(build a reliable data pipeline that can be rerun safely, 0.72)
  - semantic(why do the numbers in our warehouse not match the source, 0.72)
  - semantic(design a layered model for our warehouse tables, 0.72)
  - semantic(tune this slow Postgres database and add data quality checks, 0.72)
  - semantic(backfill historical data without creating duplicates, 0.72)
---

## Overview

Use this skill to build the plumbing that analytics and products stand on: ingestion that survives reruns, warehouse models with a declared grain, transforms in disciplined layers, Postgres that performs under load, and quality checks that catch drift before a dashboard shows it. The outcome is a design or implementation that fails loudly instead of delivering wrong data on time.

## Mental model

Pipelines fail silently and are trusted loudly. The values that protect against that are boring ones: idempotency, explicit schemas, and tested assumptions. Documented shape and real shape differ in every warehouse, so read the real schema and sample the real data first.

## Rules

### Method

1. Map the terrain: sources, volumes, update frequencies, and who consumes what for which decision. Read the actual schemas, sample the actual data, and code-search the existing pipeline before designing.
2. Declare the grain: write each table's grain (one row = one what) before any SQL. Grain ambiguity is where fan-out joins, double counting and silent revenue inflation start.
3. Design for rerun: every job is idempotent. Rerunning yesterday produces yesterday's correct state, not duplicates. Use MERGE or upsert by natural key, or delete-insert or overwrite by partition. Never blind append.
4. Build in layers: staging (rename, cast, dedupe only, 1:1 with source), intermediate (business logic, joins), marts (consumption-shaped). Logic lives in exactly one layer; a metric defined in three places is three different metrics. Look up framework and dialect specifics in documentation, not from memory.
5. Test the data, not just the code: wire the quality checks below into the pipeline and fail loudly at the layer boundary. Run what is runnable (psql, jobs, checks) and report real output.
6. Ship carefully: propose DDL and backfills with row-count estimates and a rollback path. Destructive operations (DROP, DELETE, TRUNCATE, type-narrowing ALTER) wait for explicit approval. Store conventions, grains and gotchas in memory.

### Modeling

- Star schema for consumption: fact tables (events or transactions at declared grain, foreign keys and measures) and dimension tables (the nouns, with attributes). Snowflaking is usually premature normalization of an analytics layer.
- Slowly changing dimensions: default to type 1 (overwrite) unless history is genuinely queried. Type 2 (validity ranges) needs from and to timestamps, a current flag, and an explicit reason.
- Naming: consistent and boring. Timestamps end in `_at` (UTC always), dates in `_date`, booleans start with `is_` or `has_`. Timezone conversion happens at presentation, never in storage.
- Late-arriving data is normal: incremental windows overlap (reprocess the trailing N days), and completeness is asserted per source watermark, not assumed at midnight.
- Surrogate keys: bigint identity or time-ordered UUIDs (`uuidv7()`, built in since PostgreSQL 18). Random v4 UUIDs scatter inserts across the index.

### Transform tooling and table formats

- A transform framework (dbt, SQLMesh) earns its keep through model contracts on marts, unit tests on tricky logic, and source freshness checks, not only DAG ordering. dbt Core v2 and the Fusion engine are still alpha; confirm status in documentation before adopting.
- Open table formats (Iceberg, Delta): idempotency comes from MERGE by key or partition overwrite. Schedule compaction and snapshot expiry, or small files and stale snapshots degrade every reader. Keep schema evolution additive.
- DuckDB is a good default for local and medium-sized transforms, tests, and reading Parquet or Iceberg directly. A warehouse is not needed for every pipeline.

### Postgres performance

- Diagnose with EXPLAIN (ANALYZE, BUFFERS) before touching anything (PostgreSQL 18 includes buffer counts with ANALYZE by default). The slow part is where rows times loops are, not where intuition points.
- Indexes: b-tree by default. Order composites equality first, then range (PostgreSQL 18 skip scan can use a composite without its leading column, but a well-ordered index still wins). Use partial indexes for skewed predicates (`status = 'active'`) and covering indexes (INCLUDE) for hot index-only scans. Every index taxes writes; drop indexes nobody scans.
- Batch big writes: thousands per transaction, not millions in one and not one per row. Check VACUUM and autovacuum health when bloat or wraparound symptoms appear.
- Partition by time when tables reach hundreds of millions of rows or retention-dropping is needed. Partition pruning plus DROP PARTITION beats DELETE by orders of magnitude.
- Assume connection pooling. Long-running transactions block vacuum and replication: flag them.
- Major-version upgrades: PostgreSQL 18 pg_upgrade carries planner statistics over. On older versions run ANALYZE right after upgrading or the planner flies blind.

### Data quality tests

The non-negotiable four: not-null and unique on every declared key, referential integrity at layer boundaries, freshness (data newer than X per source), and volume anomaly (today within a tolerance band of the trailing average). Then domain asserts: totals reconcile to source (count and sum on money columns), enum values in the allowed set, no future timestamps. A backfill or migration ends with a reconciliation query, not with "it ran".

### Schema changes

Go additive first: new column nullable, backfill, then tighten. Renames and drops are two-phase with a deprecation window, because something always still reads the old name. Announce contract changes to consumers before, not after. Migrations are forward-only scripts in version control with a tested rollback path. For key and index rules, lock levels and the expand/contract steps per engine, use the `database-design-and-migrations` skill.

### Common requests

| Request | Response |
|---|---|
| "Build a pipeline for X" | Ask terrain questions if unanswered (at most 3: sources, volume, consumers), then give the layered design with quality gates. |
| "This query or dashboard is slow" | EXPLAIN ANALYZE first, evidence-based fix, measured verification. |
| "The numbers look wrong" | Trace lineage layer by layer with reconciliation queries until the divergence point; report the layer, cause and blast radius. |
| "Add a field or source" | Schema-change protocol: additive path, affected consumers, backfill plan. |
| Ambiguous | Ask one question, usually the grain: "one row should equal one what?" |

In an autonomous, non-interactive brief, don't ask. Infer the grain from the real schema and data, proceed, and list the assumptions in the design. Destructive statements still wait for explicit approval.

### Guards

- Don't run destructive statements (DROP, DELETE, TRUNCATE, narrowing ALTER) or bulk writes without approval of the exact statement and target.
- Don't design a non-idempotent load. Blind appends are duplicate factories.
- Don't leave a backfill or migration unreconciled. Count and sum against source before calling it done.
- Declare the grain of every table before writing its SQL.
- Read real schemas and sample real data before designing.

### Scope limits

The statistical interpretation of results, one-off analytical queries, spreadsheets, predictive models, and infrastructure provisioning or orchestrator deployment are separate jobs.

## Output format

- Designs as `pipeline-<name>.md` or `model-<domain>.md`: grain declarations up front, layer diagram, load strategy, quality checks, open questions.
- SQL and DDL in the project's dialect and style; migrations as numbered forward scripts.
- Tuning reports: symptom, EXPLAIN evidence, change, measured before and after.
- Backfill plans: scope, row estimates, batching, reconciliation query, rollback.

## Checklist

- [ ] Every table has a written grain.
- [ ] Every load is idempotent and survives a rerun.
- [ ] Logic lives in one layer.
- [ ] The four core quality checks are wired in and fail loudly.
- [ ] Each backfill or migration ends with a count and sum reconciliation.
- [ ] Destructive statements have explicit approval of the exact statement and target.

## Composition / References

- `database-design-and-migrations` covers keys, indexes, lock levels and expand/contract migrations.
- `data-sql-queries` covers one-off analytical query debugging.
