---
name: database-design-and-migrations
title: "Database Migration and Schema Design: Keys, Indexes"
description: "Database schema design rules for keys and indexes, plus zero-downtime database migration patterns and lock levels for PostgreSQL, MySQL, SQLite."
license: Apache-2.0
compatibility: "Needs a SQL client or database MCP tool for live checks; works from schema files alone."
rules:
  - match((?i)\b(schema|table|database|data\s+model)\s+(design|migrations?|changes?)\b)
  - match((?i)\b(design|model)\s+(a\s+|an\s+|the\s+|my\s+|our\s+)?(database\s+|db\s+)?(schema|tables?)\b)
  - match((?i)\b(foreign\s+keys?|composite\s+index|primary\s+key|partial\s+index|covering\s+index|unique\s+constraint)\b)
  - match((?i)\b(which|what)\s+(index|indexes|indices)\s+(should|do|to)\b)
  - match((?i)\b(add|drop|rename|change|alter|create)\s+(an?\s+|the\s+)?(\w+\s+){0,2}(columns?|index|indexes|constraint|table)\b)
  - match((?i)\bzero[- ]downtime\s+(migration|schema|ddl)s?\b)
  - match((?i)\b(expand[/ -]+contract|online\s+(index|ddl|schema)|create\s+index\s+concurrently|gh-ost|alembic|flyway|liquibase)\b)
  - content(migration)
  - content(migrations)
---

## Overview

An application schema outlives the code that first used it, and a schema change is the one deploy step that can lock a production table. This skill gives the rules for choosing keys and indexes, and the step order for changing a live schema without blocking reads and writes. It covers PostgreSQL, MySQL (InnoDB) and SQLite. Lock and rewrite behavior below was checked against the PostgreSQL 18 docs, the MySQL 8.4 manual and the SQLite ALTER TABLE page in 2026-11. Behavior changes between versions, so check the version in use before running DDL on a large table.

## Mental model

Two questions decide every change. First, does the statement take a lock that blocks traffic, and for how long? Second, does it rewrite or scan the whole table while holding that lock? A change is safe on a large table only when the answer to both is "briefly" or "no". When the answer is "yes", split the change into steps that each pass the test. This split is the expand/contract pattern.

## Rules

### Keys

- Every table has a primary key. Use a surrogate key (bigint identity, or a time-ordered UUID such as `uuidv7()` in PostgreSQL 18) when no natural key is stable. Random v4 UUIDs scatter inserts across the index.
- Keep a natural unique key as a separate `UNIQUE` constraint when the business needs it (email, external id). The surrogate key is for joins, the unique key is for correctness.
- Use `int` primary keys only for tables that cannot reach 2 billion rows. Changing `int` to `bigint` later rewrites the table in PostgreSQL and MySQL.
- Declare foreign keys. Index the referencing column yourself: PostgreSQL and SQLite do not create it, and a missing one makes parent deletes scan the child table. MySQL InnoDB creates it automatically if none exists.
- Store money as integer minor units or `numeric`/`DECIMAL`, never float. Store timestamps in UTC (`timestamptz` in PostgreSQL).

### Indexes

| Situation | Rule |
|---|---|
| Composite index | Equality columns first, then the range or sort column. Put the most selective equality column first only if the leading columns are always filtered. |
| Skewed filter (`status = 'active'`) | Partial index (PostgreSQL, SQLite) on the hot subset. MySQL has no partial indexes; use a composite. |
| Hot read needs only a few extra columns | Covering index: `INCLUDE` (PostgreSQL), or append the columns (MySQL, SQLite). |
| Filter on an expression (`lower(email)`) | Expression index (PostgreSQL, SQLite) or a generated column plus index (MySQL). |
| Foreign key column | Index it (see Keys). |
| Low-cardinality column alone (boolean) | Don't index it alone; combine it with another column or use a partial index. |
| Unused index | Drop it. Every index taxes every write. Check `pg_stat_user_indexes.idx_scan` in PostgreSQL before dropping. |

Prove each new index with the query plan before and after (`EXPLAIN`). An index the planner does not use is cost without benefit.

### Zero-downtime change order (expand/contract)

1. Expand: add the new column, table or index in a form old code ignores (nullable, or with a default that needs no rewrite).
2. Dual-write: deploy code that writes both old and new shapes. Reads still use the old one.
3. Backfill: copy old data to the new shape in batches (1,000 to 10,000 rows per transaction, with a pause between batches so replicas keep up). Resume from a saved key, not an offset.
4. Verify: row counts and a checksum or sum on key columns match between old and new.
5. Switch reads to the new shape. Keep dual-writes for one release.
6. Contract: stop writing the old shape, then drop it in a later release. Dropping and renaming never share a deploy with the code change that stops using the name.

Rules for every step:

- Each migration is a forward-only script in version control. Write the rollback for steps 1 to 5 before running them; step 6 is irreversible without a backup, so it waits for explicit approval.
- Run schema changes on a copy of production-sized data first and time them.
- Set a short lock timeout (PostgreSQL `SET lock_timeout = '3s'`, MySQL `SET SESSION lock_wait_timeout = 10`) so the migration fails fast instead of queuing all other traffic behind it. Retry later.
- Check for long-running or idle-in-transaction sessions before starting. A pending exclusive lock blocks every later query on that table, including reads.

### PostgreSQL (18.x docs)

| Change | Lock | Rewrite or full scan | Safe pattern |
|---|---|---|---|
| `ADD COLUMN` with a non-volatile default | `ACCESS EXCLUSIVE`, brief | No rewrite | Direct. A volatile default, stored generated column or identity column rewrites the table: add nullable, then backfill in batches. |
| `ADD COLUMN ... NOT NULL` without default | `ACCESS EXCLUSIVE` | Fails on non-empty table | Add nullable, backfill, then enforce (next row). |
| `SET NOT NULL` | `ACCESS EXCLUSIVE` | Full scan unless a valid `CHECK (col IS NOT NULL)` exists | Add `CHECK ... NOT VALID`, `VALIDATE CONSTRAINT`, then `SET NOT NULL`, then drop the check. |
| `ADD CONSTRAINT ... CHECK` or `FOREIGN KEY` | Check: `ACCESS EXCLUSIVE`; FK: `SHARE ROW EXCLUSIVE` on both tables | Full scan | Add with `NOT VALID` (no scan), then `VALIDATE CONSTRAINT` (`SHARE UPDATE EXCLUSIVE`, allows reads and writes). |
| `CREATE INDEX` | Blocks writes | Full scan | `CREATE INDEX CONCURRENTLY` (outside a transaction block; two table scans; one concurrent build per table). |
| Failed concurrent build | none | Leaves an `INVALID` index that still costs writes | `DROP INDEX CONCURRENTLY`, or `REINDEX INDEX CONCURRENTLY`, then retry. |
| `ALTER COLUMN TYPE` | `ACCESS EXCLUSIVE` | Usually full rewrite (none if binary-coercible, such as `varchar(n)` to `text`) | New column, dual-write, backfill, switch, drop. |
| `DROP COLUMN` | `ACCESS EXCLUSIVE`, brief | No rewrite | Direct, after code stops reading it. |
| Partitioned table index | n/a | `CONCURRENTLY` is not supported on the parent | Build each partition concurrently, then create the parent index non-concurrently. |

PostgreSQL DDL is transactional: a failed multi-statement migration rolls back cleanly, except `CREATE INDEX CONCURRENTLY`, which cannot run in a transaction.

### MySQL 8.4 (InnoDB)

| Change | Algorithm | Concurrent DML | Notes |
|---|---|---|---|
| Add or drop column | `INSTANT` (default in 8.4) | Yes | State `ALGORITHM=INSTANT` so the statement fails instead of silently copying the table. |
| Add secondary index | `INPLACE` | Yes | Table stays readable and writable. |
| Rename column | `INSTANT` or `INPLACE` | Yes if type and nullability are unchanged | A column referenced from another table needs `INPLACE`. |
| Change column type | `COPY` only | No | Full table copy: use an external online schema tool (gh-ost or pt-online-schema-change) or the expand/contract pattern. |
| Add auto-increment column | `INPLACE`, `LOCK=SHARED` at least | No | Blocks writes. |

- Always write `ALGORITHM=` and `LOCK=NONE` explicitly. If the engine cannot honor them, the statement errors instead of blocking.
- DDL takes a metadata lock at the start and an exclusive one briefly at the end. A long-running or idle transaction delays the end lock and stalls later queries; check `SHOW FULL PROCESSLIST` first.
- MySQL DDL is not transactional: a failed migration can leave partial state. Keep one change per script.

### SQLite

- `ALTER TABLE` supports `RENAME TO`, `RENAME COLUMN`, `ADD COLUMN` and `DROP COLUMN`. `ADD COLUMN` cannot add a `PRIMARY KEY` or `UNIQUE` column, a `NOT NULL` column without a non-null default, or a stored generated column. `DROP COLUMN` fails if the column is indexed, in a primary key or unique constraint, in a foreign key, or used by a view, trigger or generated column.
- For any other change, use the table-rebuild procedure from the SQLite docs: `PRAGMA foreign_keys=OFF`, `BEGIN`, create `new_X`, copy rows, `DROP TABLE X`, `ALTER TABLE new_X RENAME TO X`, recreate indexes, triggers and views, `PRAGMA foreign_key_check`, `COMMIT`, `PRAGMA foreign_keys=ON`. Create the new table before renaming; the reverse order can corrupt references in views and triggers.
- SQLite 3.53.0 (2026-04-09) added `ALTER COLUMN ... SET NOT NULL` and `DROP NOT NULL`. On older versions use the rebuild.
- Enable `PRAGMA foreign_keys=ON` per connection; it is off by default. Write-ahead logging (`PRAGMA journal_mode=WAL`) lets readers continue during one writer. The database file is locked for writes during a rebuild, so keep it short and run it in a transaction.
- SQLite has no concurrent index build. `CREATE INDEX` blocks writers for its duration; on a large file, build it in a maintenance window.

## Examples

Bad: add a required column in one step on a 200 million row PostgreSQL table.

```sql
ALTER TABLE orders ADD COLUMN region text NOT NULL DEFAULT lookup_region();
```

A volatile default rewrites the table under `ACCESS EXCLUSIVE`. Writes stop for the whole rewrite.

Good: expand, backfill, enforce.

```sql
SET lock_timeout = '3s';
ALTER TABLE orders ADD COLUMN region text;                       -- step 1, brief lock
-- step 3: batches of 5,000 rows, resume from the last id
UPDATE orders SET region = lookup_region(id) WHERE id > :last AND id <= :last + 5000 AND region IS NULL;
ALTER TABLE orders ADD CONSTRAINT region_nn CHECK (region IS NOT NULL) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT region_nn;                -- reads and writes continue
ALTER TABLE orders ALTER COLUMN region SET NOT NULL;             -- no scan: valid CHECK exists
ALTER TABLE orders DROP CONSTRAINT region_nn;
```

## Checklist

- [ ] The engine and version are named, and the lock level and rewrite behavior of each statement were looked up for that version.
- [ ] Every statement on a large table passes both questions: brief lock, no whole-table rewrite while locked.
- [ ] Lock timeout is set and long-running sessions were checked first.
- [ ] Backfill is batched, resumable, and ends with a count and sum reconciliation.
- [ ] A rollback exists for every step before the contract step; the contract step has explicit approval.
- [ ] New indexes have a before and after query plan; foreign key columns are indexed.
- [ ] Destructive statements (`DROP`, `TRUNCATE`, narrowing `ALTER`) were not run without approval of the exact statement and target.

## Composition / References

- PostgreSQL ALTER TABLE: https://www.postgresql.org/docs/current/sql-altertable.html (18.7)
- PostgreSQL CREATE INDEX: https://www.postgresql.org/docs/current/sql-createindex.html
- MySQL 8.4 online DDL operations: https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html
- MySQL 8.4 online DDL locking: https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-performance.html
- SQLite ALTER TABLE: https://www.sqlite.org/lang_altertable.html
- Companion skill in this domain: `analytical-report` for presenting results.
