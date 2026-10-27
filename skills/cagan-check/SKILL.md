---
name: cagan-check
description: >-
  Apply Marty Cagan product principles (Inspired, Empowered, Transformed) plus Teresa Torres' Continuous Discovery to a software dev's workflow from the Product Trio's engineering seat. Runs structured reviews for feature kickoff, sprint planning/estimation, client discovery calls, and pull requests — checking problem framing, outcome metrics, the five big risks (value/usability/feasibility/viability/ethical), business sense (does the outcome trace to revenue, retention or cost, fit the business model's lever, and justify its build cost), feature-factory smells (incl. Cutler 2025 updates: high WIP, Team Tetris, success theater), prototyping fit, instrumentation, customer touchpoint cadence. Outputs green/yellow/red flags per dimension with concrete next actions. Use when user says /cagan-check, "starting a feature", "vou começar feature", "kickoff", "planning", "estimativa", "estimation", "discovery", "review this PR" with feature context, "is this feature worth building", or asks to apply Cagan/SVPG/Torres/product-trio thinking. Adapts to the reader's employment context — in-house product team, or client-services work (agency, consultancy, contractor) where a paying stakeholder sits between the team and the end user. Output language: mirror the language of the user's current turn (detect per invocation — pt-BR if user wrote in Portuguese, EN if in English, etc).
---

# cagan-check

Applies Marty Cagan product principles through the lens of the **dev in the Product Trio**. Not a PM coach — it's a strong-engineer checklist that pushes the team out of feature factory mode.

## Modes

Detect mode from context. If ambiguous, ask.

| Mode | Triggers | Focus |
|------|----------|-------|
| **kickoff** | "starting a feature", "vou começar feature", "new project", "kickoff" | Problem, outcome, unvalidated risks, prototype fit, Opportunity Solution Tree |
| **planning** | "planning", "estimation", "estimativa", "refinement", "sprint" | Outcome + metric before estimating, smells, WIP check |
| **discovery** | "discovery", "client call", "user interview", "reunião cliente" | Past-behavior questions, customer exposure cadence, 5 risks |
| **review** | "review this PR", "code review" + feature context | Instrumentation, metric wired, scope vs problem, ethical |

## Workflow

1. **Confirm mode** (1 line) — "Mode: kickoff. Checking X dimensions."
2. **Gather minimum context** — if critical info missing (which feature, which client, which problem), ask before assessing
3. **Run the mode's dimensions** (see `CHECKLISTS.md`)
4. **Emit Flag Report** — fixed format below
5. **Suggest one concrete next step** — single action, not a list

## Flag Report (output format)

```
## Cagan check — [mode] — [feature/project]

🟢 [Dimension] — [1 line: what's good]
🟡 [Dimension] — [risk/gap] → [suggested action]
🔴 [Dimension] — [critical problem] → [required action]

## Next step
[1 concrete action, 1-2 lines]
```

Rule: **every yellow/red flag requires an action**. Never emit a flag without a fix.

## Core dimensions (always checked)

1. **Problem framing** — Is there a named user/business problem? Or just a requested feature?
2. **Outcome + metric** — How will we know it worked? Defined, measurable metric? Can you trace it up to a business result (revenue, retention, or cost)?
3. **5 risks** — Value, Usability, Feasibility, Business Viability + **Ethical** (Torres). Which are validated? Viability includes the money side: does it fit how this business earns, and is it worth its build and run cost? Ethical covers LGPD/GDPR, AI bias, dark patterns.
4. **Feature factory smells** — see `REFERENCE.md`. Shortcuts: high WIP, Team Tetris, success theater.
5. **Customer touchpoint** — did the current week include real user contact? (Torres: keystone habit is a weekly interview by the full trio)

## Dev's formal role in the trio

Per Cagan/SVPG: **Tech Lead is the formal owner of feasibility risk and co-accountable for product delivery**. Not "executor with an opinion" — accountability is shared with PM and Designer. The skill operates from this premise: speak as tech lead, not passive dev.

## Business sense (the money side of viability)

Product sense says what to build; business sense says why it matters to the business. Cagan already puts business-model fit inside viability, but engineers tend to stop at legal and infra cost. With fewer PMs per engineer on AI-native teams, more of these calls land in engineering, so the tech lead should be able to answer three things, one line each:

- **Which P&L line moves?** Revenue, retention, or cost. Trace feature metric → team goal → that line. Nobody can draw the chain = 🟡 on Outcome.
- **Which lever does this business model run on?** Subscription lives on retention and expansion, a marketplace on transaction volume, e-commerce on conversion × order value × repeat rate. A feature that pushes the wrong lever is busywork with a good demo.
- **Is the prize bigger than the build?** Rough reach × impact against build + run + support hours. Differentiators earn the polish; table stakes get the cheapest version that holds up, or get bought instead of built.

This is a lens on the existing dimensions, not a new one, so it adds no flag lines of its own. The P&L chain goes in the **Outcome** flag, lever and prize vs. build go in the **Viability** flag, and "competitor has it" goes in **Value**. Raise it only where the gap changes a decision (what to build, how much to invest, what to measure), phrased as a question the team can answer, not a finance lecture. When planning ranks several items, one compact prize-vs-hours table can stand in for the per-item value lines; don't repeat the numbers in both. Lever table, sizing math and a worked example in [REFERENCE.md](REFERENCE.md#business-sense-the-money-side-of-viability).

## Per-mode dimensions

- **kickoff**: + Prototype fit (worth a spike before implementing?) + Opportunity Solution Tree (map outcome → opportunities → solutions → assumptions; rank the candidate solutions by rough size of the prize, and let differentiator vs. table stakes set how much engineering each deserves)
- **planning**: + Honest estimation (high uncertainty = discovery, not delivery; weigh estimated hours against what the outcome is worth) + **WIP check** (high WIP = feature factory)
- **discovery**: + Past-behavior questions (Torres: "How do you do this today?" beats "Would you use X?" — hypotheticals produce false yeses); in client work, ask how the client makes money
- **review**: + Instrumentation (events, success query ready in the PR? events tied to the business lever, not only clicks) + Ethical check (LGPD/GDPR, bias, dark patterns)

Details in [CHECKLISTS.md](CHECKLISTS.md).

## Client-services context

Applies when a paying stakeholder sits between the team and the end user — agency, consultancy, contractor, or an internal team serving another business unit. Skip if you build for your own end users. Adapt when relevant:
- Client pays for delivery ≠ client pays for outcome. Try to align around the **end user's outcome**, not just the contracting stakeholder's.
- Fixed contract scope makes discovery hard. Propose a **discovery sprint** before the delivery sprint when possible.
- The client's roadmap may itself be a feature factory. Don't copy blindly — challenge with Cagan-style questions.
- Two business models are in play: the client's (what the feature should move) and your firm's (billable hours, renewals). Learn the client's: how they make money and which number your stakeholder reports up. Work that moves that number is easy to defend and is what renews the engagement; work that moves none of it is a weak bet even inside the contract.

## Tone

- Direct, no filler
- Fragments OK
- **Mirror the language of the user's current message** — detect per invocation. If user wrote in pt-BR, respond pt-BR. If EN, EN. If they switch, switch. Never hardcode a default.
- Cite book/SVPG when it adds weight (`(Inspired, ch. Engineers)`, `(Torres, Continuous Discovery Habits)`) — keep proper nouns and quotes in original EN regardless of output language
- Don't turn into a lecture — flags + action

## References

- [REFERENCE.md](REFERENCE.md) — 5 risks detailed, business sense (levers, sizing, right to win, worked example), feature factory smells, prototype types, OST, quotes
- [CHECKLISTS.md](CHECKLISTS.md) — full per-mode checklist
