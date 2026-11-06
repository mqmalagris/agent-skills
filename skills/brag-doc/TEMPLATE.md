# Brag Doc — Templates

## Monthly entry (the recurring unit — Lucas Faria's 4 fields, plus Caught and Story seeds)

Copy this block to the top of the target doc on the 1st of each month.

```md
## <Month Year>
_<projects covered> · drafted from <sources> on <date>_

**Shipped + impact**
↳ <what shipped>: <outcome: who uses it / metric / $ saved / time saved>. `[mine | led | with <role> | contributed] · <status as of date> · refs: <PRs, tickets, ADR, query>`
↳ ...

**Caught**
↳ <what was wrong>: <who caught it: me / AI reviewer / QA / client>, <how>, <did tests miss it?>. refs: <PR, commit>

**Challenges & how I tackled them**
↳ <challenge> → <what I did about it>

**Would be much better if…**
↳ <what's blocking me / what would unblock me / what I'd change>

**Focus next month**
↳ <1–3 priorities>

**Story seeds**
↳ [<type>] <one-line headline>: <the check or evidence> · refs: <thread, PR>
```

### The tags

| Tag | Values | Rule |
|---|---|---|
| Ownership | `mine`, `led`, `with <role>`, `contributed` | Matches git: authored commits, not merged or reviewed. Name what already existed. |
| Status | `prod <date>`, `staging`, `dev`, `PR open`, `flagged off`, `beta <N> users`, `not shipped` | As of the drafting date. Never round staging up to shipped. |
| Refs | PR #, ticket ID, ADR, commit, query file | Enough to find the evidence in six months. |

**Numbers carry their method** inline or as a footnote: source, sample, environment, window. A quick one-off measurement is tagged `[smoke test]` and stays out of CVs until re-measured against the system of record.

### Story seed types

`agent-wrong` (an AI agent or reviewer was wrong and you caught it) · `disagreement` · `my-mistake` · `decision` (a choice with the alternative you rejected) · `pushback` (on a requirement) · `discovery` (evidence before a build) · `incident` · `cost-perf`

A seed is one line. It needs the type, what happened, and the check that made it real (a test order, a query, a re-run). The `compile stories` mode expands seeds into full cards later; the seed only has to be findable and true.

Impact-line rule (Julia Evans): a line is done when it survives *"so what?"*.
- Task (weak): "Refactored the checkout service."
- Impact (strong): "Refactored checkout, cutting p95 latency 40%, so it now handles Black Friday load without the manual scale-up." Fuzzy work → **goal → actions → observable effect**.

## Rollup (for `compile` → promo packet / self-review — Julia's categories)

Assemble from several monthly entries; don't maintain by hand.

```md
# Rollup — <period>

### Goals (this period / next)
### Projects & impact          # the headline outcomes, quantified
### Collaboration & mentorship # reviews, onboarding, pairing, talks others built on
### Design & documentation     # design docs, RFCs, docs written and why
### Company building           # interviewing, process, recruiting beyond the day job
### What I learned             # tech, tools, domain, soft skills
### Outside of work            # OSS, blog posts, talks, shipped side apps
```

Not every category fires every period — omit empty ones. "Make it sound exactly as good as it is."

## Story seeds rollup (for `compile stories`)

```md
# Story seeds — <range>

## Coverage
| Type | Seeds | Strongest |
|---|---|---|
| agent-wrong | ... | ... |
| (every type; "none" when empty) | | |

## <Seed headline>
**Type:** <type> · **Month:** <Month Year> · **Status:** <as of date>
**A. Headline:** one sentence: what happened and what I did.
**B. 20 seconds:** spoken version.
**C. 60 to 90 seconds:** answer, me, context, decision, check, result.
**E. Follow-ups:** 3 likely questions with short answers.
**F. Ownership:** mine vs others'.
**G. Evidence:** refs.
**Open:** what only I can confirm before telling it.
```
