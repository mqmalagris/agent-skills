---
name: dev-flow
description: Route a dev task through the right subset of the canonical skill chain (adhd → grill-me → to-prd → compass → heist → maestro → code → verify → code-review → implementation-review → pr-craft), matching ceremony to stakes. Detects the task tier (bug / feature / architecture / client), shows the exact chain it will run and what it skips, confirms, then drives the sub-skills in order — pausing where each needs user input. Use when the user says "start a feature", "new feature", "kickoff", "route this through the workflow", "run the chain", "which skills for this", or /dev-flow. NOT for tasks already mid-chain (a PRD/plan exists) — invoke the specific next skill instead.
---

# dev-flow

Conductor for the canonical dev chain. It does NOT re-implement the sub-skills — each one owns its own logic and its own "when to skip" rules. This skill only picks the tier, orders the stages, and drives them. Match ceremony to stakes: a bug gets three steps, a new subsystem gets ten.

Executor note: this is a prompt, not a script. Sub-skills still pause for user input (grill-me interrogates, pr-craft wants approval). Drive one stage, wait for it to finish, then start the next. Never fire the whole chain blind.

## Protocol

1. **Isolate** — a dev-flow run dirties the working tree and makes commits across many stages. If another agent might touch this repo concurrently (the default assumption on a shared machine), call `EnterWorktree` before driving any stage so this whole run gets its own working tree + branch and the main checkout stays free for that other agent. This is the parallel-worktrees "isolating your own work" path (see that skill). Name the worktree after the task. Skip only if already in a worktree session, or it's a throwaway one-liner on a repo you're certain is yours alone; when skipping, say so in the plan so the user can override.
2. **Detect tier** from the task description (table below). If ambiguous, ask one question: which tier.
3. **Print the plan** — the ordered stage list for that tier, each stage marked RUN or SKIP with a one-line reason. Honor each sub-skill's own skip rules (e.g. grill-me skips single-file changes; to-prd skips bug fixes). Reflect those in the SKIP reasons. Lead with the isolation decision (worktree name, or why skipped).
4. **Confirm** — user says go / edit / abort. Accept partial edits ("skip the PRD", "add adhd", "no worktree"). Record exactly what they approved.
5. **Drive** — invoke each RUN stage via the Skill tool, in order. After each returns, checkpoint: report what it produced (file path, decision, diff), then start the next. Stop and surface if a stage can't proceed (fuzzy scope → route back to grill-me; unsettled architecture → route to compass).
6. **Close** — after the last stage, one-line summary of artifacts produced (PRD path, ADR path, plan path, PR URL). If you entered a worktree in step 1, `ExitWorktree` with `keep` (never `remove` — the branch holds your commits and the pushed PR).

## Tiers

Detect from the task. When in doubt, pick the lower-ceremony tier and let the user upgrade.

| Tier | Signal | Chain |
|------|--------|-------|
| **bug** | obvious cause, single-file, spike, throwaway | code → verify → pr-craft |
| **feature** | multi-file, some design surface, user-visible | grill-me → to-prd → heist → code → verify → code-review → implementation-review → pr-craft |
| **architecture** | new subsystem, public API, hard-to-reverse decision, schema, "how should I structure X" | adhd → grill-me → to-prd → compass → heist → code → verify → code-review → implementation-review → pr-craft |
| **client** (Arctic Leaf) | agency client work, delivery for a stakeholder | wrap the feature/architecture chain in cagan-check: kickoff (before) + review (before PR) |

### Stage gates (only RUN when the gate is true)

- **adhd** — only if the approach is open-ended / you're stuck. Skip if the approach is obvious or the user used closed phrasing ("quick", "standard", "just").
- **grill-me** — only if scope has non-obvious tradeoffs. Skip single-file / obvious.
- **to-prd** — only if a spec adds value. Skip bug/spike (commit message is enough).
- **compass** (architect/ADR) — only if an architectural decision is unsettled and hard-to-reverse. Skip if convention already dictates the shape.
- **maestro** — only if there are multiple independent **plans/PRDs/ADRs** worth parallelizing; derives the conflict graph and merge order from them. Not in the default chains; add on request.
- **parallel-worktrees** — the plan-optional counterpart to maestro. Two uses here, both governed by that skill: (a) **run-level isolation** — the `EnterWorktree` step 1 above, so this run doesn't collide with a separately-launched agent on the same repo; (b) **intra-stage fan-out** — when a stage (usually **code**) splits into independent slices on disjoint files with no formal plan docs to feed maestro, it handles the go/no-go, file partitioning, subagent isolation, and integration. Not a chain stage itself; a primitive any stage can invoke. Use maestro when plans exist, this when they do not.
- **verify** — only if the change has runtime surface to drive. Skip docs/test-only diffs.
- **code-review** — run for anything beyond a trivial one-liner. Hunts correctness bugs in the diff.
- **implementation-review** — the pre-commit gate: seven parallel checks (plan gaps, use-case coverage, missing test scenarios, test philosophy, SOLID, Clean Code, security). Runs after code-review, before pr-craft makes the commit. RUN for feature/architecture; SKIP for the bug tier (code-review already covers a small diff, and the plan/coverage checks are moot without a plan). It applies its own skip rules internally (drops Checks 1-2 when no plan is findable), so it degrades gracefully on lighter work.
- **commit-report** — optional, at the end, if the user wants a standup/PM/client note.

## Rules

- **Never skip a stage silently.** Print SKIP + the reason, so the user can override.
- **Never expand past what the user approved.** Partial OK is valid — honor it exactly.
- **Artifacts flow forward.** grill-me's Glossary → to-prd → heist, verbatim. Don't paraphrase domain terms between stages.
- **Respect existing artifacts.** If a PRD/ADR/plan already exists for this work, mark that stage SKIP (done) and start from the next.
- **This skill drives; it doesn't decide inside a stage.** Once a sub-skill is invoked, follow that skill's own instructions — don't second-guess its internals.
- **Obey CLAUDE.md conventions** (shell-command wrappers, commit-message trailers, etc.) — sub-skills that touch the shell already honor these; don't override them.

## When to skip dev-flow entirely

- Task is already mid-chain (a plan or PRD exists) — invoke the specific next skill directly, no need to route.
- One-line edit, typo, rename — just do it.
- Non-dev task (CV, content, research) — those have their own skills.
