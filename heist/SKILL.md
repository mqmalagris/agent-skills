---
name: heist
description: Turn a settled feature scope into a concrete implementation plan and write it to docs/plans/<slug>.md. Plans the job like a heist — crew (files touched), sequence (ordered tasks), getaway (rollback/risks), payoff (acceptance criteria). Use when user has a PRD, ADR, or settled feature spec and wants a step-by-step build plan before coding. Triggers on /heist, "plan this feature", "implementation plan", "break this down", "how do we build X", or after to-prd / compass when ready to code.
---

# heist

Plan the job before pulling it off. Read the context, output a single Markdown file at `docs/plans/<slug>.md`. Don't write code. Don't bundle multiple features.

## Inputs to gather (in order, stop when enough)

1. **Feature spec** — PRD, ADR, conversation context, or user's brief.
2. **Codebase shape** — relevant files, framework, conventions. Use Glob/Grep/Read sparingly; depth proportional to feature size.
3. **Constraints** — deadlines, stack, performance/security needs.

If feature spec is fuzzy → stop, tell user to run `/grill-me` or `/to-prd` first. Don't invent scope.

## Output format

Write to `docs/plans/NNNN-<slug>.md` (zero-padded, next available). Create dir if missing.

```markdown
# Heist: <Feature title>

- **Status**: planned | in-progress | done
- **Date**: YYYY-MM-DD
- **Sources**: <links to PRD/ADR/issue>

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

### Phase 2: <phase name>
- **Status**: planned
- **Goal**: ...

- [ ] **<task name>** — ...

Phases run sequentially unless marked parallel. Small features = 1 phase. Large = 3-5. Don't pad.

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
- **Honor stack conventions.** If repo uses kebab-case files, plan uses kebab-case. Read existing structure before naming.
- **Don't write code after planning.** Hand back to user. They run plan or invoke implementation separately.
- **Update existing plan** if user says "update the plan" — find by slug, modify, bump status.

## When to skip heist

- Bug fix (just fix it).
- Single-file change.
- Spike/throwaway.
- Plan already exists and feature unchanged.

## Pipeline placement

`compass → grill → to-prd → heist → code`

heist consumes PRD/ADR, outputs plan, hands to code.
