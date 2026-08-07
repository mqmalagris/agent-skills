---
name: heist
description: Turn a settled feature scope into a concrete implementation plan and write it to docs/plans/NNNN-<slug>.md. Plans the job like a heist — crew (files touched), sequence (ordered tasks), getaway (rollback/risks), payoff (acceptance criteria). Use when user has a PRD, ADR, or settled feature spec and wants a step-by-step build plan before coding. Triggers on /heist, "plan this feature", "implementation plan", "break this down", "how do we build X", or after to-prd / compass when ready to code.
---

# heist

Plan the job before pulling it off. Read the context, output a single Markdown file at `docs/plans/NNNN-<slug>.md` (zero-padded, next available index). Don't write code. Don't bundle multiple features.

## Inputs to gather (in order, stop when enough)

1. **Feature spec (what to build)** — PRD, conversation context, or user's brief. Defines scope, user stories, acceptance criteria.
2. **Architectural constraints (how it must be built)** — scan `docs/adr/` for accepted ADRs touching the area. ADRs are locked decisions: stack, paradigm, persistence model, integration style, auth, observability. Read every ADR whose subject overlaps the Crew set. List them in `Sources`. Plan must respect them — if the plan would violate an ADR, stop and surface the conflict to the user before writing.
3. **Codebase shape** — relevant files, framework, conventions. Use Glob/Grep/Read sparingly; depth proportional to feature size. If the PRD has a `## Glossary`, use those terms verbatim in The Job, The Crew descriptions, and acceptance criteria.
4. **Operational constraints** — deadlines, performance/security needs, feature-flag policy.

If feature spec is fuzzy → stop, tell user to run `/grill-me` or `/to-prd` first. Don't invent scope.
If an architectural choice is unsettled (no ADR, no clear convention) → stop, tell user to run `/compass` first. Don't pick paradigms inside a plan.

## Output format

Write to `docs/plans/NNNN-<slug>.md` (zero-padded, next available). Create dir if missing.

```markdown
# Heist: <Feature title>

- **Status**: planned | in-progress | done
- **Date**: YYYY-MM-DD
- **Sources**: <links to PRD/ADR/issue>
- **phase**: <optional — feature/epic tag for maestro grouping, e.g. `auth-rewrite`>
- **depends on**: <optional — comma-separated slugs of other heist plans that must merge first>

## The Job
<1-3 sentences. What's getting built and why. Plain language.>

## The Crew
Files touched. New = create, Mod = modify, Del = delete.

| File | Role | Action |
|------|------|--------|
| `src/auth/magic-link.ts` | token mint + verify | New |
| `src/api/auth.routes.ts` | wire endpoints | Mod |

## The Sequence
Phased plan. Each phase is a coherent milestone, ideally one PR. Tasks inside are checkboxes.

### Phase 1: <phase name>
- **Status**: planned | in-progress | done
- **Goal**: <what this phase delivers>

- [ ] **<task name>** — <one line>. Touches: `<files>`. Done when: `<observable result>`.
- [ ] **<task name>** — ... `(depends on previous)`

### Phase 2: <phase name> (parallel with Phase 3)
- **Status**: planned
- **Goal**: ...

- [ ] **<task name>** — ...

Phases run sequentially unless the header carries a `(parallel with Phase N)` suffix. Parallel phases must not share Crew files. Small features = 1 phase. Large = 3-5. Don't pad.

## The Payoff
Acceptance criteria. Bullet list. Each item testable.

- [ ] <criterion>
- [ ] <criterion>

## The Getaway
Rollback + risk plan.

- **Rollback**: <how to undo if shipped and breaks>
- **Risks**: <named risks, not "might break things">
- **Feature flag?**: yes/no + flag name
- **Migration**: <data/schema changes + reversibility>

## Test Plan
- **Unit**: <what>
- **Integration**: <what>
- **Manual**: <what>

## Open Questions
Unresolved items blocking start. If empty, delete section.

- [ ] <question>
```

## Rules

- **One feature per plan.** Bundling = bad plan.
- **Phases are milestones, not micro-steps.** Each phase ships something working. If a phase has 1 task, collapse phases.
- **Tasks are checkboxes.** Update `- [ ]` → `- [x]` as work progresses. Bump phase Status field too.
- **Crew table is exhaustive for known files.** Add `?` next to speculative ones.
- **Acceptance criteria are testable.** "Works well" is not. "Login completes in <2s p95" is.
- **No code in plan.** Pseudocode rare; only when sequencing isn't clear without it.
- **Honor stack conventions** in this priority: (1) ADR-declared stack/paradigm, (2) existing code patterns in the repo, (3) user override. If they conflict, surface the conflict — don't silently pick.
- **Don't write code after planning.** Hand back to user. They run plan or invoke implementation separately.
- **Update existing plan** if user says "update the plan" — find by slug. Edit-safe sections: `Status`, phase `Status`, task checkboxes (`- [ ]` → `- [x]`), `Open Questions`, adding new phases at the end. Locked sections (require explicit user OK to touch): `The Crew`, `The Payoff`, `Sources`, `phase`, `depends on`. Never delete a phase; mark it `cancelled` instead.

## When to skip heist

- Bug fix (just fix it).
- Single-file change.
- Spike/throwaway.
- Plan already exists and feature unchanged.

## Pipeline placement

`grill-me → to-prd → compass → heist → maestro → code`

- **grill-me** stress-tests the design tree, extracts ubiquitous-language Glossary.
- **to-prd** codifies scope + Glossary into PRD.
- **compass** locks architecture in ADRs (auto-written to `docs/adr/`).
- **heist** consumes PRD + ADRs, outputs plan in `docs/plans/`.
- **maestro** verifies parallel feasibility across N heist plans, orchestrates agents in git worktrees.
- **code** — user (or agent dispatched by maestro) implements one phase at a time.

Skip earlier stages when the artifact already exists. Heist requires at minimum a settled feature spec; if architecture is unsettled, route back to compass first.

## Humanize the written prose (if available)

Before writing generated prose to a file, if the `humanizer` skill is installed, run it on the drafted text so the created document reads naturally and free of AI tells; skip silently if it is not available. Apply it to the human-facing document body only, never to code, frontmatter, file paths, IDs, or literal templates.
