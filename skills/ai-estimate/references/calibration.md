# Calibration examples

Each example shows both layers. The pattern to notice: on small and medium changes the human layer is usually larger than the agent layer, and the grounding step changes the module list.

## 1. "Other" option with a free-text field on an existing form (real)

A stakeholder wanted an "Other" choice in a category picker on a directory entity's form, with the dependent subcategory field becoming free text when it's picked. Bulk import explicitly out of scope.

**What grounding changed.** The first estimate from the ticket alone was 3-4h and assumed one form. Reading the code found:
- two separate implementations of the form (Add dialog, Edit page), plus a third self-service editor
- the backend already accepted any string on create/update, and only the import validated against the preset list, so no backend work was needed
- the list filter built its options from the constants, so custom values couldn't be filtered
- the preset constant also fed the import templates, so "Other" had to be a separate constant

| # | Module | Rounds | Risk | Eff. |
|---|--------|--------|------|------|
| 1 | Constant + helpers + i18n | 1 | 1.0 | 1 |
| 2 | Add dialog: option, text field, validation, payload | 3 | 1.0 | 3 |
| 3 | Edit page: same, plus prefilling existing custom values | 3 | 1.3 | 4 |
| 4 | Filter options derived from data | 2 | 1.0 | 2 |
| 5 | Self-service editor fix | 1 | 1.0 | 1 |
| 6 | Tests | 2 | 1.3 | 3 |
| | Integration | +2 | | 2 |

Agent: ~16 rounds ≈ 45-60 min.

| Human | Time |
|-------|------|
| Review (~300 lines) | 30-40 min |
| Local run (multi-tenant login) | 15 min |
| QA: add, edit, filter, self-service (4 flows) | 40-60 min |
| Lint + typecheck + tests + CI | 20-30 min |

**AI-assisted total: 2-3h** (this is what was quoted). A per-workspace table that remembers used values was priced separately; the stakeholder chose the basic version.

Lessons: the first 3-4h was ungrounded and assumed one form. The next pass was grounded but sized in manual-dev hours (6-8h), and had to be recomputed as AI-assisted. It also briefly folded an out-of-scope extra (the workspace table) into the headline number, which the stakeholder pushed back on.

## 2. New backend endpoint + migration

Add a per-workspace list resource: table, migration, list/upsert service, GET/POST routes, an integration test. There's a precedent table with the same shape.

| # | Module | Rounds | Risk | Eff. |
|---|--------|--------|------|------|
| 1 | Schema + migration | 2 | 1.0 | 2 |
| 2 | Service list/upsert | 2 | 1.0 | 2 |
| 3 | Routes, auth scoping, route ordering | 2 | 1.3 | 3 |
| 4 | Integration test | 3 | 1.3 | 4 |
| | Integration | +1 | | 1 |

Agent: 12 rounds ≈ 35-45 min.

| Human | Time |
|-------|------|
| Review (~250 lines, incl. SQL) | 30 min |
| Run migration locally, hit the routes | 20-30 min |
| CI + one fix | 20-30 min |
| Migration/deploy verification | 30 min |

**AI-assisted total: 2-2.5h.** The migration line is what makes this bigger than it looks.

## 3. One-line bug fix, hard to reproduce

A date filter is off by one day in some timezones. The fix is one line; reproducing and proving it takes the time.

| # | Module | Rounds | Risk | Eff. |
|---|--------|--------|------|------|
| 1 | Reproduce + locate | 4 | 1.5 | 6 |
| 2 | Fix + regression test | 2 | 1.0 | 2 |

Agent: 8 rounds ≈ 25 min.

| Human | Time |
|-------|------|
| Review | 15 min |
| Verify in 2 timezones | 20-30 min |
| CI + PR | 20 min |

**AI-assisted total: 1-1.5h.** The line count says 5 minutes; the verification says an hour.

## What inflates, what shrinks

Inflates:
- a surface duplicated in places the ticket doesn't mention
- env friction for local runs (auth, subdomains, seed data, slow dev server)
- schema changes (the migration line, plus backfill if old rows need it)
- a flaky CI suite (budget a re-run)
- open product questions (the PM loop line grows)

Shrinks:
- a sibling implementation to copy (modules drop to 1 round)
- the backend already accepts the data
- the person already has the app running and a test account ready
