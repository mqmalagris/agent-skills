---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree and emitting a Design Notes + Glossary block for handoff to /to-prd. Use when user wants to stress-test a plan, get grilled on their design, do a pre-PRD design review, challenge an idea before writing it up, or mentions "grill me" or runs /grill-me.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer (with brief reasoning); skip the recommendation only when the codebase or my prior answers haven't given you enough signal.

## Rules of engagement

- **One question at a time.** No multi-part dumps.
- **Codebase first.** If a question can be answered by reading the repo, read it instead of asking.
- **ADR awareness.** Scan `docs/adr/` before grilling. Don't relitigate settled architectural decisions; treat ADRs as locked inputs and grill *around* them.
- **Converge.** Stop when every major branch of the decision tree has either a resolved decision or an explicit `OPEN` marker. Cap: ~20 questions per session unless I ask to keep going.
- **OPEN markers.** If a branch can't be resolved (I defer, codebase silent, needs external input), record it as `OPEN: <question>` and move on. Don't loop.

## Questioning lens

Drive questions through these angles, in roughly this order. Skip ones that don't apply.

1. **Scope** — what's in, what's out, what's deferred.
2. **Actors + user stories** — who triggers this, what do they expect.
3. **Domain vocabulary** — see "Capture the domain vocabulary" below.
4. **Data shape** — entities, relations, identity, lifecycle, persistence.
5. **Boundaries + integrations** — which subsystems / services / external APIs are touched, sync vs async.
6. **Failure modes** — what breaks, what's transient vs fatal, retry policy, idempotency.
7. **Edge cases** — empty states, max sizes, concurrency, race conditions, duplicates.
8. **Security + auth** — who's allowed, what they see, attack surface, PII handling.
9. **Performance + scale** — expected volume, p95 latency targets, hot paths.
10. **Observability** — what gets logged / metered / traced, alert thresholds.
11. **Rollback + migration** — how to undo, schema reversibility, feature-flag plan.
12. **Testability** — what's testable end-to-end, what needs mocks, prior test patterns to mirror.

## Capture the domain vocabulary

While interviewing, build a **ubiquitous language** for this feature — the shared terms used by the business, the user, and the code. Rules:

- When the user names an entity, action, or concept (e.g., "order", "checkout", "subscription"), note the exact word. Don't paraphrase.
- When generic words appear ("the thing", "this object", "the record"), ask: "What does the business call this?" Force a real term.
- When two terms seem to overlap ("user" vs "customer", "cart" vs "order"), ask which is which and where the boundary is — that's a bounded-context signal.
- Capture aliases too: if devs say `OrderItem` and the business says "line", record both and pick one as canonical.

## Output

At end of session (or when I say "wrap it up"), emit a single markdown block:

```markdown
# Design Notes: <feature title>

## Resolved decisions
- <decision>: <chosen option> — <one-line rationale>
- ...

## Open questions
- OPEN: <question> — <who/what needs to answer it>
- ...

## Glossary
Term — definition. (aliases: <other names if any>)
...
```

This block is the handoff to `/to-prd`, which synthesizes it into a PRD. Don't write to disk — the user copies the block into the next step or keeps it in conversation.

## When to skip grill-me

- Bug fix with obvious cause.
- Single-file change, no design tradeoffs.
- Spike / throwaway exploration.
- Design already settled in a PRD or ADR (read those instead).

## Pipeline placement

`grill-me → to-prd → compass → heist → maestro → code`

- **grill-me** (this skill) — stress-tests decision tree, extracts Glossary + OPEN questions.
- **to-prd** — synthesizes Design Notes into a PRD on disk + tracker.
- **compass** — locks architectural decisions in ADRs.
- **heist** — produces implementation plan.
- **maestro** — orchestrates parallel execution.
- **code** — implement.

Skip earlier stages when the artifact already exists. grill-me is optional for small features but high-leverage for anything with non-obvious tradeoffs.

## Humanize the written prose (if available)

Before writing generated prose to a file, if the `humanizer` skill is installed, run it on the drafted text so the created document reads naturally and free of AI tells; skip silently if it is not available. Apply it to the human-facing document body only, never to code, frontmatter, file paths, IDs, or literal templates.
