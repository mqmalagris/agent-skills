---
name: ai-estimate
description: Estimate how long a dev task will really take when it's built AI-assisted (an agent writes the code, a human reviews, tests, ships). Grounds every number in the actual code first, counts agent work in tool-call rounds, then adds the human layer (diff review, local run, browser QA, PR/CI, review feedback, PM back-and-forth) as separate lines. Use this whenever someone asks for an estimate, "how long would X take", "how many hours", sizing, scoping, a quote for a PM or client, or a comparison of options by effort — even when they don't say "estimate" and even for a quick ballpark. Also use it before replying to a ticket, Lobby/Teamwork/Slack thread or PR comment that asks "estimate to complete?".
---

# AI-assisted estimate

Two things go wrong when an AI estimates dev work, and they pull in opposite directions:

1. **It anchors on human timelines** from training data ("a developer would take 2-3 days") for work an agent writes in minutes. The number comes out several times too high.
2. **It forgets the human.** Counting only agent minutes misses the part that actually eats the day: reading the diff, running the app, clicking through the flow, waiting on CI, answering review comments, the PM thread. Those are usually most of the real time.

And one thing goes wrong regardless of who estimates: **quoting before looking at the code.** A number built from a ticket's wording is a guess dressed up as an estimate. It tends to be wrong in whichever direction the code surprises you (a second copy of the form nobody mentioned, a validator only the import uses, a filter built from constants).

The headline number this skill produces is the **AI-assisted total**: agent time plus human time. That is what the person will actually spend, and it's what gets quoted.

## Procedure

### 1. Lock the scope

Before sizing anything, write down in one or two lines what is in and what is out, **as the stakeholder agreed it**, not as you'd build it. Read the thread or ticket for decisions already made ("no change to imports", "client wants the basics").

- If you believe something outside the agreed scope is necessary, don't fold it into the number silently. Price it as a separate line and say why. The person decides whether it becomes part of the quote.
- If scope is genuinely unclear and the answer changes the number a lot, give the estimate for each reading rather than guessing one.

This matters because an estimate that quietly includes extras gets challenged ("client just wants the basics") and you end up re-quoting, which costs more trust than the extra hours were worth.

### 2. Ground it in the code

Read the code that the change touches before producing any number. Concretely, find and note with `file:line`:

- every place the change lands: all copies of the form/screen/handler (add AND edit, admin AND self-service, web AND mobile), not just the first one you find
- validation on both sides: which layer rejects unknown values, and on which paths (create vs update vs import)
- storage: is there a schema change, a migration, a backfill?
- consumers of the data: lists, filters, search, exports, reports, notifications, anything that renders or matches on the value
- existing tests that will break or need a new case
- a precedent in the codebase for the same pattern (it cuts rounds a lot)

For a wide change, delegate this sweep to a search subagent and ask it for a file:line change list with a rough size per item. You want the conclusion, not the file dumps.

If you genuinely can't read the code (no access, no repo), say so up front, widen the range, and label the number **unverified**. Never present an ungrounded number as if it were grounded; the person will quote it.

### 3. Agent work in rounds

A **round** is one tool-call cycle: reason → edit → run → read output → decide. Break the change into modules (one per change-list item, or group tiny ones) and give each a base round count:

| Pattern | Rounds | Example |
|---|---|---|
| Known pattern, one shot | 1-2 | add a constant + i18n keys, a config flag, copy a sibling component |
| Moderate | 3-5 | a form field with conditional UI + validation, a new endpoint on an existing router |
| Exploratory | 5-10 | unfamiliar module, sparse docs, logic spread across a large file |
| High uncertainty | 8-15 | undocumented behavior, multi-system debugging, a possible dead end |

Multiply by a risk coefficient and justify it in a few words: **1.0** clear precedent, **1.3** minor unknowns, **1.5** quirks or integration unknowns, **2.0** may need a different approach. Add **10-20%** integration rounds for wiring the modules together. Tests the change needs are a module, not an afterthought.

Convert at **~3 min/round** (2 for trivial edits, 4-5 when every round needs a slow build or a manual check). This is agent wallclock, and it's usually the smaller half.

### 4. The human layer

Now add what the person does. Each line is its own number; skip lines that genuinely don't apply, but say you skipped them.

| Activity | Default | Scales with |
|---|---|---|
| Review the diff properly | 15 min + ~10 min per 100 changed lines | size and risk of the diff |
| Run it locally / set up data | 15-30 min | env friction (seed data, auth, subdomains, services) |
| Manual / browser QA | 10-20 min per user-facing flow | number of flows × happy path + edge cases |
| Lint, typecheck, tests, CI wait + one fix | 20-40 min | CI length, flakiness |
| PR write-up + one round of review feedback | 20-40 min | reviewer count, how contested |
| Migration / deploy verification | +30 min | only if schema or infra changes |
| PM / stakeholder back-and-forth | 0-30 min | open questions left after step 1 |

These are defaults for someone reviewing seriously, not skimming. Adjust from what you know about the person's environment (e.g., a dev server that's slow to boot, a staging deploy that needs verification) and say what you adjusted.

### 5. Total, range, and a sanity check

- **AI-assisted total** = agent wallclock + human layer. Give a range, low to high, rounded to the nearest half hour above 1h. A range is honest; a point estimate implies precision you don't have.
- **Sanity check against anything already quoted.** If you or the person already posted a number for this work (or a bigger/smaller variant of it), check the new one is consistent. For example, the "basic" option should be clearly under the "full" option. If it isn't, fix it or explain the gap before anyone reads it. A quote that contradicts a previous one gets questioned.
- **Don't quote a manual-dev equivalent** unless asked. If you mention one, label it clearly so it's never confused with the real number.

## Output

Give the person two things: the breakdown they check, and the line they can post.

```markdown
### Estimate: <task>

**Scope:** <in> · **Out:** <out, per the agreed decision>
**Grounded in:** <n files read; the key file:line refs> (or: UNVERIFIED — <why>)

| # | Module | Rounds | Risk | Eff. | Where |
|---|--------|--------|------|------|-------|
| 1 | ...    | 2      | 1.0  | 2    | path:line |

Agent: <X> rounds ≈ <A-B> min

| Human | Time |
|-------|------|
| Review | ... |
| Local run | ... |
| QA (<n> flows) | ... |
| CI + PR | ... |

**AI-assisted total: <L-H>h**
Separate options (not in the total): <option — +Nh — why>
Biggest risks: <what would blow this up>

Quotable: "<one or two sentences with the range, whether design is needed, and any caveat the reader must know>"
```

The quotable line is a starting point. If the person has a voice or brevity skill for outward messages, run it through that before they post.

## Anti-patterns

- **Number first, code later.** Every miss in this skill's origin story started there.
- **Human-time anchoring.** "A dev would need a day" — start from rounds.
- **Agent-only totals.** 40 minutes of agent work is not a 40-minute task.
- **Scope creep inside the number.** Extras you think are wise go in "separate options", priced, with a reason.
- **One copy of a duplicated surface.** Add and edit are often two implementations; so are admin and self-service views.
- **Padding by vibes.** Risk goes in the coefficient with a reason, not a silent +50%.
- **Inconsistent quotes.** A new number that doesn't square with one already posted.

## Calibration

`references/calibration.md` has worked examples with both layers, including a real one. Read it when the task resembles one of them or when you're unsure how big the human layer should be.

Credits: the round-based agent layer is adapted from [agent-estimation](https://github.com/ZhangHanDong/agent-estimation) (MIT, see `LICENSE`).
