# Data access — code-craft reference

Stack-agnostic rules for code that reads or writes a store (SQL database, SQLite file, KV, Durable Object storage). They apply in every language; the examples use pseudo-SQL. Each rule was promoted from a review blind spot that recurred across repos (review-pass ledgers: smartbrokr-hono-api, v0-smartbrokr, kiskadee).

Loaded by `code-craft` alongside the language or framework file whenever the code under review or being drafted touches persistence.

---

## A — Tactical

### A1. Read paths never create or migrate
**Rule.** A read path opens its store read-only and never creates, migrates or "fixes" it. A missing or empty store is an error on that path.
**Reason.** A view that runs setup turns "nothing here" into "ok, 0 rows". The real problem gets hidden, and an audit or status command quietly mutates what it's reporting on.
```text
// wrong: `status` reuses the writer's open(), which creates the schema
db = open(path)            // CREATE TABLE IF NOT EXISTS ...
print(count(db))           // "0 entries" on an empty/foreign file
// right
db = open(path, READ_ONLY) // fails if missing
if schema_version(db) == 0: error("not a <app> database")
```

### A2. Lock first, then read what you'll act on
**Rule.** Take the lock or exclusive transaction before reading the state a write depends on. Any "if absent, create" (schema init, upsert-by-check, next sequence number, a clock value that orders writes) runs inside the same exclusive transaction that writes.
**Reason.** A check made outside the transaction is stale by the time the write lands. Two processes both see "absent", both create, and one fails or both commit duplicates. Retry anything the store refuses at once under contention rather than queueing (SQLite's WAL switch is one example).
```text
// wrong
if version(db) == 0: begin(); create_schema(); commit()
// right
begin(IMMEDIATE)             // write lock taken here
if version(db) == 0: create_schema()
commit()
```

### A3. Figures shown together come from one snapshot
**Rule.** Numbers displayed or returned together (totals, per-status counts, "remaining = total - done") come from one query or one read transaction, never from separate auto-committed statements.
**Reason.** A write committed between two statements makes the figures disagree. Derived values (orphans, balances, remaining) go negative or wrong in ways nobody can reproduce.
```text
// wrong
total = query("SELECT COUNT(*) ...")
done  = query("SELECT COUNT(*) ... WHERE status = 'done'")  // newer snapshot
// right
begin()                      // one read snapshot
total, done = query("SELECT COUNT(*), SUM(status = 'done') ...")
commit()
```
