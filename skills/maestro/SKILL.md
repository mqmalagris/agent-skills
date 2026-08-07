---
name: maestro
description: Verify plans, PRDs, and ADRs for parallel-execution feasibility, build a conflict graph from files-touched data, judge whether parallelizing is actually worthwhile, then orchestrate agents in git worktrees to implement, test, and clean up when it is. Use when the user asks to parallelize work across plans, run plans concurrently, split feature work across multiple agents, set up git worktrees for several plans, dispatch agents to implement plans, check if PRDs/ADRs/plans conflict, decide if work from the same or different phases can run in parallel, or runs /maestro.
---

# maestro

Verify planning docs, build parallelization plan, orchestrate agents in worktrees — only when it actually makes sense.

## Source modes

Pick one with the user before scanning:

1. **Auto-scan** (default) — `py -3 scripts/scan_plans.py --root .` (Windows; use `python3` on POSIX) finds `docs/plans/*.md`, `docs/prds/*.md`, `docs/adrs/*.md`, plus common variants.
2. **User paths** — user passes file globs or absolute paths.
3. **Conversation context** — when the current chat already contains a settled plan/PRD/ADR, use that text directly (write it to a temp file under the repo's `.claude/tmp/` so the parsers can read it).

Always confirm the source set with the user before extraction.

## Workflow

All scripts run on Python 3. On Windows use `py -3` (this user's default `python` is Py2.7); on POSIX use `python3`. Examples below show `py -3`.

1. **Scan** — `py -3 scripts/scan_plans.py [--root <path>]` returns JSON list `{type, path}`.
2. **Extract** — `py -3 scripts/extract_files.py <file>` per doc. Returns `files_touched`, `phase`, `deps`, parser `format`. Heist `## Crew` section parsed strict; otherwise heuristic path scan over the whole doc.
3. **Conflict matrix** — `py -3 scripts/conflict_matrix.py <doc> <doc> ...`. Pairwise file-overlap + declared-dep edges, builds DAG, marks each pair `serial` or `parallel-ok`. Detects dep cycles.
4. **Worth-it check** — `py -3 scripts/worth_it.py <doc>` per parallelizable doc. Verdicts: `worth-it`, `not-worth-it`, `review-needed`, `serial-recommended`. Heuristics flag migrations, shared schema/types, doc size, dir isolation.
5. **Propose** — print to user:
   - DAG (mermaid + ASCII fallback)
   - Per-doc verdict table
   - Worktree commands (`git worktree add ../<repo>-<slug> -b parallel/<slug>`)
   - Agent dispatch table (doc → agent type → worktree → fg/bg)
6. **Confirm** — ask user: full plan / subset / abort. Accept partial agreement ("do A and B parallel, skip C", "create worktrees but hold spawning"). Record exactly what they OK'd.
7. **Execute** (only after explicit OK) —
   - Create worktrees per agreed doc, branch name `parallel/<slug>` (slug = plan filename without extension)
   - Spawn agents — default: parallel `Agent` tool calls in a single message, one per worktree. Switch to `run_in_background: true` if user asked for background. Each agent prompt includes: worktree absolute path, plan file path inside the worktree, hard scope ("only edit files listed in the plan's Crew/files-touched section, stop and report if you need to touch anything else"), commit guidance (small commits on the branch, never push, never merge).
   - Track per user preference (poll, notify-on-done, both).
8. **Integrate + cleanup** (after agents finish) —
   - Per agent done, report: commit count, files touched, any out-of-scope edits.
   - Suggest merge order from the DAG (topological).
   - User merges locally, branch by branch — skill does NOT auto-merge and does NOT push.
   - After each merge, run tests on the integrated branch:
     - `py -3 scripts/detect_tests.py [--root <path>]` returns runner command (vitest, cargo test, pytest, playwright, etc.). Falls back to asking user when ambiguous.
     - Run via `rtk` wrapper when available (`rtk vitest run`, `rtk cargo test`, `rtk playwright test`).
     - On pass → `git worktree remove ../<repo>-<slug>` + `git branch -d parallel/<slug>`.
     - On fail → keep worktree and branch, surface failures, abort cleanup for that slug only.
   - Final summary: which slugs merged + cleaned, which still blocked.

## Permission gates

Confirm before:
- Creating any worktree (writes branches and a working dir)
- Spawning any agent (cost, parallel work)
- Removing a worktree or deleting a branch in cleanup (only after tests pass)
- Pushing branches (default: no auto-push, ever — user can opt in per slug)

Partial OK is valid and must be honored exactly — never expand scope past what was approved.

## When parallel does NOT make sense

Recommend serial even with no file overlap if:
- Plans share a migration, schema, or generated artifact
- One plan's output (types, API surface) is consumed by another
- Plans tagged same phase + tightly coupled domain
- Total work below coordination overhead (rough floor: < ~30 min each)

## Output spec, edge cases, format details

See [REFERENCE.md](REFERENCE.md).
