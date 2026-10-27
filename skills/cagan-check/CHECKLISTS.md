# cagan-check — Per-mode checklists

Use the checklist for the detected mode. Each item becomes a 🟢/🟡/🔴 flag in the Flag Report.

---

## Mode: KICKOFF (new feature/project)

### Problem framing
- [ ] User problem named in one sentence? (not "we're going to do X" but "user Y can't do Z")
- [ ] Who is the specific user? (concrete persona or segment)
- [ ] Why now? (urgency, opportunity, pain)

### Outcome + metric
- [ ] Success metric defined and numeric? (not "more engagement" but "+15% conversion in flow X")
- [ ] How will we measure? Is instrumentation planned?
- [ ] Baseline known?
- [ ] Metric traces to a business result? (feature metric → team goal → revenue, retention or cost). No chain = 🟡

### 5 risks
- [ ] **Value** — Did we validate the user wants it? How?
- [ ] **Usability** — Will it be tested with users before release?
- [ ] **Feasibility** — Any unvalidated technical risk? (new API, scale, integration)
- [ ] **Viability** — Legal/compliance/contract checked? Fits the business model's lever? Build + run + support cost known, and smaller than what it moves?
- [ ] **Ethical** (Torres) — LGPD/GDPR OK? AI bias reviewed? Dark patterns absent? Automated decisions have a human appeal path?

### Business sense (fold findings into the Outcome, Value and Viability flags; no separate flag line)
- [ ] Which P&L line does it move: revenue, retention, or cost? Named, not implied?
- [ ] Business model lever identified? (subscription: retention/expansion · marketplace: transaction volume · e-commerce: conversion × order value × repeat rate · ads: engaged time · usage-based: consumption). Feature pushes a different lever = 🟡
- [ ] Rough size of the prize? (reach × expected change × value per unit; an order of magnitude is enough). Used to rank the candidate solutions on the OST?
- [ ] Differentiator or table stakes? Differentiator = invest in quality; table stakes = cheapest version that holds up, or buy (plugin, app, SaaS) instead of build
- [ ] "Competitor has it" is the only argument? That's table stakes at best, and not value evidence (see Value risk)
- [ ] Client work: do we know how the client makes money and which number the stakeholder reports up?

### Opportunity Solution Tree
- [ ] Single outcome defined at the top?
- [ ] Opportunities (problems/pains) mapped, not solutions?
- [ ] At least 2–3 candidate solutions per opportunity?
- [ ] Main assumptions listed with a planned test?
- [ ] Did you (dev) list feasibility assumptions on the tree?

### Prototype fit
- [ ] Worth a technical spike before implementing? (if feasibility uncertain)
- [ ] Worth a flow prototype before coding? (if usability uncertain)
- [ ] Does a live-data prototype make sense? (if value uncertain)

### Trio
- [ ] PM, Designer, and Eng (you) aligned on the problem?
- [ ] Do you (dev) have a voice in the solution, not just execution?

---

## Mode: PLANNING (sprint/estimation/refinement)

### Before estimating
- [ ] Expected outcome of this delivery defined?
- [ ] Success metric defined?
- [ ] Acceptance criteria include outcome validation (not just "it works")?
- [ ] Each item mapped to the P&L line it moves (revenue, retention, cost)? Items that move none of them go last or get cut

### Effort vs. prize (fold into Honest estimation or Viability; a prize-vs-hours table can replace per-item value lines)
- [ ] Estimated hours weighed against a rough value of the outcome? An 80h build for a flow few users touch needs a reason 🟡
- [ ] Is there a cheaper version (smaller scope, buy instead of build) that captures most of the prize?
- [ ] Item justified by one deal or one account? That's a revenue bet: confirm it's committed (signed, or blocking a named deal), not "they might buy" 🟡

### Honest estimation
- [ ] Technical uncertainty = high? → don't estimate, propose a spike
- [ ] Product uncertainty = high? → don't estimate, propose discovery/prototype
- [ ] Estimate covers instrumentation?
- [ ] Estimate covers user testing (if relevant)?

### Planning smells
- [ ] Backlog is a list of features with no outcome? 🔴
- [ ] Pressure to estimate without refinement? 🔴
- [ ] Estimate became a date commitment? 🔴
- [ ] Items sliced by feature, not by outcome? 🟡

### WIP check (Cutler 2025)
- [ ] How many items in parallel in the sprint? >3 per dev = 🟡, >5 = 🔴
- [ ] Does the team have a lasting mission or jumps from project to project (Team Tetris)? 🔴
- [ ] Sprint success measured in points delivered or in outcome? "Points" = 🔴

### Trio in planning
- [ ] Designer present?
- [ ] Did PM bring the problem or bring the solution?

---

## Mode: DISCOVERY (client call / research)

### Preparation
- [ ] Clear hypothesis of what we want to validate?
- [ ] Main question defined? (just one — don't fire a machine gun)
- [ ] Call type known? (problem discovery vs solution validation)

### Customer exposure
- [ ] When did the team last talk to a user? (>30 days = 🔴)
- [ ] Will you (dev) be on the call, or just the PM?
- [ ] Will the rest of the team have access to the insight?

### Torres rule — past behavior > hypothetical
- [ ] Questions start with "tell me about the last time..." or "how do you do this today?" — not "would you use X?"
- [ ] Zero hypothetical questions ("would you buy?", "what would you think of?") — guaranteed false yes
- [ ] Collecting concrete stories, not opinion
- [ ] Room to observe the real flow, not just hear a retelling?
- [ ] Weekly cadence? (Torres' keystone habit — without this, discovery is theater)

### Client-services context
- [ ] Is the client the stakeholder or the end user?
- [ ] If the client is the stakeholder, can we get access to the end user?
- [ ] Is the outcome for the client's client clear?
- [ ] Do we know how the client makes money and which number our stakeholder reports up? Ask directly; it reframes every scope conversation

### Post-call
- [ ] Will the insight be shared with the whole trio?
- [ ] Can a product decision change based on what we hear?
- [ ] If the answer is "no", the call is theater

---

## Mode: REVIEW (pull request)

### Scope vs problem
- [ ] PR description links to a problem/outcome? (not just "implements feature X")
- [ ] Scope matches the problem? (no gold-plating, no scope creep)
- [ ] Change outside the problem's scope? 🟡

### Instrumentation
- [ ] Events tracked at the critical points of the flow? 🔴 if missing
- [ ] Success query/dashboard ready or referenced?
- [ ] Baseline metric captured before release?
- [ ] Alerts/errors instrumented?

### Validatable outcome
- [ ] Can we answer "did it work?" within N days using data from this PR?
- [ ] Events reach the business lever (order placed, renewal, retained account), not only UI clicks? A click with no downstream join can't answer "did it make money?" 🟡
- [ ] Feature flag for gradual rollout / kill switch?
- [ ] A/B test wired if applicable?

### Post-release risks
- [ ] **Feasibility** — perf tested? load estimated?
- [ ] **Viability** — LGPD/GDPR/compliance/contract OK? Running cost (infra, third-party fees, support load) known? Could it cannibalize the lever it's meant to grow (e.g. pulls users out of checkout)?
- [ ] **Usability** — copy reviewed? error states covered?
- [ ] **Ethical** — data collection justified? AI feature has a human fallback? no dark patterns in the flow?

### Review smells
- [ ] Huge PR with no decomposition? 🟡
- [ ] PR adds a feature with no instrumentation? 🔴
- [ ] PR doesn't mention a metric/outcome? 🟡

---

## Flag emission rules

- **🟢 green**: item is satisfied — worth a one-line confirmation only if non-obvious
- **🟡 yellow**: risk/gap, can still ship but must be addressed — always has an action
- **🔴 red**: real blocker (money loss, guaranteed rework, compliance) — required action

Don't emit 🟢 just to emit. Focus on 🟡 and 🔴.

Max 2–3 flags per dimension. Prioritize impact.

## Next step

After the flags, suggest **one** concrete action. Not a list. Examples:

- "Before planning, ask the PM which metric will move. Without that, the estimate is a guess."
- "Run a 1-day spike on integration Y before estimating the sprint."
- "Add 2 events to the PR (`click_cta`, `complete_flow`) and link the Mixpanel query."
- "On the next call, request 15 minutes with the end user, not just the stakeholder."
- "Ask the client which number their stakeholder reports up, then write the chain from this feature to it in the ticket."
- "Ship the off-the-shelf version first; build custom only if the data says this lever matters."
