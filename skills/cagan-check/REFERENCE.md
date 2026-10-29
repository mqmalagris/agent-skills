# cagan-check — Reference

Deep content. Load only when detail is needed.

## The 5 Risks (Cagan's 4 + Torres' Ethical)

Every feature carries 5 risks. Discovery exists to attack the unvalidated ones **before** delivery. Cagan defines the first 4; Teresa Torres expands the set to include Ethical, increasingly critical in the AI/LGPD/GDPR era.

### 1. Value risk
**Question**: Will the customer use/buy it?

Validation: interviews, prototype tested with real users, in-production A/B, usage data from analogous features.

Signs it's NOT validated: "we think they'll like it", "client asked for it" (≠ client will use it), "competitor has it".

### 2. Usability risk
**Question**: Can the customer discover and use it?

Validation: usability testing with a prototype, observed sessions, funnel metrics from similar features.

Signs it's NOT validated: never tested outside the team, copy written by dev/PM with no review, >5-step flow never tested.

### 3. Feasibility risk
**Question**: Can engineering build it with the time/skill/tech available?

Validation: technical spike, proof of concept, tech lead consultation, load analysis.

Signs it's NOT validated: new tech with no POC, integration with unknown system, scale assumed without test, external deps unconfirmed.

**This risk is your superpower as a dev.** You're the only one who can answer honestly. Raise it early.

### 4. Business Viability risk
**Question**: Does it work for the rest of the business (legal, finance, sales, marketing, support, compliance), and does it pay off for the business?

Validation: stakeholder review early, not at the end. A one-line chain from the feature metric to a P&L line.

Signs it's NOT validated: LGPD/GDPR not checked, infra cost not calculated, support not trained, client contract doesn't cover it, marketing doesn't know how to sell, nobody can say whether it moves revenue, retention or cost, the feature pushes a lever the business model doesn't run on.

**In client-services settings**: the client contract IS viability. A feature outside scope = high risk even if the client wants it. The client's business model is the other half: a feature inside scope that moves none of their numbers is still a weak bet.

See [Business sense](#business-sense-the-money-side-of-viability) below for the money side in detail.

### 5. Ethical risk (Torres)
**Question**: Should we build it? Who gets harmed?

Validation: bias/fairness review, impact analysis on vulnerable groups, legal consult (LGPD/GDPR), dark-pattern audit of the flow.

Signs it's NOT validated: AI feature with no bias review, data collection with no clear purpose, UX patterns that pressure the user (fake scarcity, forced continuity, confirmshaming).

**In the AI era**: Cagan (2025) notes that the design of programmatic interfaces (APIs, agents) is driven by the tech lead, not the designer. You (dev) carry this risk on AI features. Ask: does the agent deceive the user? Does an automated decision have a human appeal path?

---

## Business sense (the money side of viability)

Adapted from Sidwyn Koh and Hannah Stulberg, *Business Sense for Engineers: The Missing Half of Product Sense* (Path to Staff, Apr 2026), reframed for the engineering seat.

Product sense = what to build. Business sense = why it matters to the business. Strategic thinking, one of Shreyas Doshi's product-sense components, depends on it. It matters more for engineers now because AI-native teams run more engineers per PM, so calls that used to sit with a PM land in engineering.

### Four questions (one line each)

**1. How does the business make money?** The P&L and its unit economics. Vocabulary worth having ready:
- **CLV** (customer lifetime value): what a customer is worth over the whole relationship
- **CAC** (customer acquisition cost): what it costs to win one customer
- **Payback period**: months until a customer's margin covers its CAC
- **ARPU** (average revenue per user) and **churn** (share of customers lost per period)

**2. Business model, not pricing model.** The business model is how the company fundamentally earns; the pricing model is how it charges (per seat, per transaction, tiered). The business model decides which outcome a feature should push:

| Business model | Lever features should move |
|---|---|
| Subscription / SaaS | Retention, expansion, stickiness |
| Marketplace | Transaction volume, liquidity on both sides |
| E-commerce / DTC | Conversion × order value × repeat rate |
| Direct selling / distributor networks | Distributor activity, qualifying volume, reorders |
| Ads-funded | Engaged time, audience size |
| Usage-based / API | Consumption per account |
| Agency / services | Billable hours, margin, renewals |

In client-services work two rows apply at once: the client's model (what the feature should move) and your firm's (what the engagement earns). An hour that moves the client's number is the one that renews the contract.

**3. Sizing.** Applies to features and technical investments, not only to markets. Business priorities come first; sizing ranks the candidate solutions under them. Rough math beats none: `reach (users or accounts per period) × expected change × value per unit`. An order of magnitude is enough to keep or kill a branch on the OST. Watch the framing: the same opportunity looks tiny or huge depending on whether you size today's market or the one the product could create (Bill Gurley's rebuttal of an early Uber market-size estimate is the classic case).

**4. Right to win.** Who are the real competitors, where does the company win or lose, and what's the moat (switching costs, distribution, network effects, data, brand)? From the engineering seat this answers *how much to invest*: work that deepens the moat earns quality and polish; table stakes gets the cheapest version that holds up, or gets bought instead of built. "Competitor has it" makes something table stakes at most. It is never value evidence on its own.

### Worked example (made-up numbers)

B2B SaaS, 2,000 accounts, $100/month ARPU. One sprint, two candidates:

- **A: fix the sync bug support links to cancellations** (24h). If monthly churn drops from 2.0% to 1.7%, that's ~6 accounts a month kept, so ~$7k more MRR after a year, and it compounds.
- **B: custom report export three large accounts asked for** (40h). If it lands one $400/month upsell each, that's $1.2k MRR, and only if they actually upgrade.

A wins on both prize and hours. B changes category only if it's blocking a named, committed deal: then it's a revenue bet with a known payoff, not a request. The point isn't precision; it's that the team stops ranking work by who asked loudest.

### Building the muscle

- Trace your team's goals up to a P&L line once, in writing. Reuse the chain in kickoffs and PR descriptions.
- Sit in one business or leadership review as a listener. List the terms you didn't know and look them up.
- Public company: read the 10-K (business overview + risk factors). Private: ask finance or ops for a short P&L walkthrough.
- Client work: once per engagement, ask the stakeholder which number they report up.

### Business-sense questions (use in meetings)

1. "Which number does this move: revenue, retention, or cost?"
2. "Is this a differentiator for us or table stakes?"
3. "Roughly how many users or accounts does it touch, and what's one of them worth?"
4. "If we cut this to half the hours, what do we lose?"

Same rule as the Cagan questions: one per meeting is enough.

---

## Direct quotes (Cagan / SVPG)

> "Engineers are often the best source of innovation, as they know what is possible."

Reinforces: a dev in discovery isn't a courtesy — they're the primary source of viable ideas.

> "Empowered engineers are the single most important thing for being a great product organization."

Reinforces: strong-dev role > strong-PM role in Cagan's hierarchy.

> "Getting the engineer's perspective earlier not only saves wasted time, but also tends to improve the solution itself."

Direct argument for entering discovery early, not waiting for a finished spec.

> "Teams of missionaries are engaged, motivated, have deep understanding of business context, and tangible empathy for the customer. Mercenaries feel no real sense of empowerment or accountability, no passion for the problem to be solved."

Lens for diagnosing your own team.

---

## Opportunity Solution Tree (Teresa Torres)

Visual structure for continuous discovery. Use at feature kickoff or quarterly planning.

```
                Outcome (1)
                    |
        ┌───────────┼───────────┐
   Opportunity  Opportunity  Opportunity   ← user problems/pains
        |             |             |
    ┌───┴───┐         |         ┌───┴───┐
  Solution Solution  Solution Solution      ← candidate ideas
        |             |             |
   Assumption  Assumption    Assumption     ← experiments to validate
     test         test          test
```

Rules:
- **One outcome per tree** (don't turn it into a feature backlog)
- **Opportunities = problems**, not solutions
- **Solutions are candidates** — most will be killed
- **Assumptions = what must be true** for the solution to work — test cheaply before coding

Dev's role on the OST:
- Surfaces technically viable solutions PM/designer can't see
- Identifies **feasibility** assumptions (load, latency, integration) — proposes a spike
- Kills tree branches when an assumption fails

---

## Transformed — 3 axes of change (Cagan 2024)

When assessing the product maturity of a company/client, separate it into 3:

1. **How you build** (delivery) — CI/CD, quality, automation
2. **How you solve problems** (discovery) — prototypes, validation, customer touch
3. **How you decide which problems to solve** (strategy) — vision, insights, focus

**Diagnostic shortcut**: a company that has only evolved #1 is still a feature factory. Real transformation requires all 3.

**In client-services settings**: the client usually pays for #1 (delivery). Pushing toward #2 (discovery sprint) and #3 (problem before feature) is the commercial challenge. Use this lens to propose different scopes in proposals.

---

## Feature Factory Smells (catalogue)

Adapted from John Cutler ("12 Signs You're Working in a Feature Factory") + Cagan.

### Process symptoms
- 🔴 Roadmap = list of features with dates, no outcome
- 🔴 Success measured by "we shipped on time", not by impact
- 🔴 No instrumentation on what shipped
- 🔴 We never kill features even when nobody uses them
- 🔴 **High WIP** (Cutler 2025 update) — many items in parallel. "Optimizing to keep people busy" is the core of the feature factory
- 🔴 **Team Tetris** — teams shuffled rapidly between projects, no lasting mission
- 🔴 **Success theater** — celebrating "shipping" without discussing real impact
- 🟡 Data used as a "trust proxy" to control the team, not to learn

### Role symptoms
- 🔴 PM acts as a project manager (manages tickets, not the problem)
- 🔴 Designer only does the final mockup, doesn't participate in discovery
- 🔴 Eng receives a finished ticket, has no voice in the solution
- 🔴 No "trio" — roles work sequentially, not together

### Customer symptoms
- 🔴 The team never talks to the end user
- 🟡 Team talks only to internal stakeholders (not users)
- 🟡 Research outsourced to a separate "user research team"

### Discovery symptoms
- 🔴 No discovery phase — only delivery
- 🔴 Prototype = "nice screen for approval", not validation
- 🟡 Discovery exists but is "design done before dev"

### Client-services symptoms
- 🟡 Client hands over a finished backlog, team only executes
- 🟡 Project success = client signs off, not end user adoption
- 🟡 No access to the client's product metrics

### Prerequisites to escape the feature factory (Cutler 2025)
- **Trust + psychological safety** — not a consequence, a **prerequisite**. Without psychological safety, the team won't surface problems, won't experiment, won't kill bad features. A leader who punishes error kills empowered teams before they're born.
- **Collaborative decision reviews** — not adversarial, not used to rank teams
- **Shared language of value** — without it nobody agrees on what matters
- **12–18 months of practice** — transformation is gradual. "Chipping away" works better than all-or-nothing. In client-services settings, start with one pilot project.

---

## Prototype types (Cagan — 4 types)

When to suggest a spike vs full implementation.

In *Inspired*, Cagan defines **4 types** — not 3, not 5. Wizard of Oz is a subtype of hybrid, not a separate type (common mistake).

### 1. Feasibility prototype
**When**: new tech, unknown integration, performance/scale doubt
**Form**: technical spike, 1–3 days, throwaway code — "just enough code" to prove it works
**Dev does**: yes, exclusive eng task

### 2. User prototype (hi-fi)
**When**: testing flow and usability
**Form**: interactive Figma or mocked front-end
**Dev does**: sometimes, designer usually leads

### 3. Live-data prototype
**When**: needs testing with real users but the full back-end doesn't exist yet
**Form**: reduced functional version — doesn't scale, no SEO/analytics, but works with real data
**Dev does**: real frontend + minimal back-end

### 4. Hybrid prototype
**When**: validating demand/behavior before investing in real automation
**Form**: combination of real and simulated parts
**Classic subtype — Wizard of Oz**: a human manually does behind the scenes what the system will automate later. The front looks like a real product.
**Dev does**: minimal interface + tooling for the human operator

**Choice rule**:
- Technical doubt → **feasibility**
- Flow/UX doubt → **user**
- Value doubt with real data → **live-data**
- Demand doubt before coding automation → **hybrid (Wizard of Oz)**

---

## Team typology (Inspired)

| Type | Receives | Decides | Result |
|------|----------|---------|--------|
| Delivery team | Ticket | Nothing | Output |
| Feature team | Feature spec | How to code it | Output |
| **Product team (empowered)** | Problem + context | Complete solution | Outcome |

Cagan: only product teams innovate. The rest execute.

**As a dev**: identify which type you're in. If feature/delivery, use cagan-check to pull toward the product side.

---

## Cagan-style questions (use in meetings)

Drop into the call without sounding arrogant:

1. "What user problem does this solve?"
2. "How will we know it worked? Which metric will move?"
3. "Have we validated that the user wants this? How?"
4. "Is there a technical risk here we haven't attacked yet?"
5. "Does a spike/prototype before estimating make sense?"
6. "When was the last time the team talked to a real user?"
7. "If we ship this and nobody uses it, what did we learn?"

One per meeting is enough at first. Don't fire a machine gun.

## Torres rule — user interviews

**Past behavior > hypothetical**. Drop into the interview:

✅ **Do** (generates real signal):
- "Tell me about the last time you had to do X"
- "How do you do this today?"
- "What happened next?"
- "Why did you pick that path?"

❌ **Avoid** (generates false yes):
- "Would you use a feature that does Y?"
- "Would you pay for Z?"
- "What would you think of...?"
- Any hypothetical/speculative question

**Why**: users are terrible at predicting their own future behavior but reasonably good at recounting concrete past behavior. Stories reveal context, frustration, workarounds — the basis for design.

**Cadence (Torres' keystone habit)**: the whole team (trio) interviews **at least 1 user per week**. Without this, discovery is theater.

---

## Books (reading order)

1. **Inspired** (2017, 2nd ed) — fundamentals: trio, risks, discovery, team types
2. **Empowered** (2020) — leadership: how to build empowered teams, coaching
3. **Transformed** (2024) — operating model: how to migrate a company to a product company

SVPG blog: svpg.com/articles — start with "Product vs Feature Teams" and "The Most Important Thing".

Complementary: John Cutler, Teresa Torres (*Continuous Discovery Habits*), Melissa Perri (*Escaping the Build Trap*).

Business sense: Koh & Stulberg, *Business Sense for Engineers* (Path to Staff, 2026) · Bill Gurley, *How to Miss By a Mile* (market sizing) · Gibson Biddle's DHM model (Delight customers in Hard-to-copy, Margin-enhancing ways) for right to win.
