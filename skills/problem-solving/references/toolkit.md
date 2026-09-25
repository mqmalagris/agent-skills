# Toolkit: tools, worked examples, templates

The tools below are standard structured problem-solving techniques. Each comes with a worked
example; use it to show the user what "good" looks like, then apply the tool to their problem.

## Contents

1. SMART problem question
2. Problem Definition Worksheet
3. Impactful questions
4. Issue trees and MECE
5. Prioritization: 80/20 and impact x feasibility
6. Workplan Worksheet
7. Conducting analyses
8. Synthesis
9. Recommendation
10. Biases and debiasing
11. Blank templates

---

## 1. SMART problem question

| Letter | Test | Example |
|--------|------|---------|
| Specific | Is the scope narrow enough? | "Improve the product" vs. "reduce checkout abandonment" |
| Measurable | How will we know it's solved? What's the KPI? | Abandonment down 5 points or 15? |
| Actionable | Does it point to concrete actions? Often has "how" or "what actions" | "Win enterprise customers": how, exactly? |
| Relevant | Does it matter to all stakeholders, and are they aligned? | Founders, team, the customer who asked |
| Time-bound | What's the horizon? | A fix before Monday's launch vs. a 2-year platform bet |

Measurable can be qualitative ("customers stop mentioning it in support tickets") as long as
success is judgeable.

**Worked example (app rewrite).** Original: "Should we rewrite our mobile apps in a
cross-platform framework?" Specific and Actionable pass; Measurable (better how?) and
Time-bound are missing. Better: "Should we move the iOS and Android apps to a shared codebase
**over the next two quarters, with the current team of three**, if that lets us ship both
platforms on the same release cadence without lowering the crash-free rate?"

**Folding a constraint in.** A support team brainstormed hiring more agents, buying a new
helpdesk tool and adding 24/7 coverage to cut response times. Headcount and tooling budgets
were frozen, so all three were outside the solution space. New question: "**With the current
team and tools**, how do we cut first-response time in half by the end of the quarter?"

**Competing framings.** "Reduce our cloud bill" can mean cut total spend this month or lower
the cost per customer as you scale; the first says shut things down, the second says
re-architect. A SaaS outage at 2 a.m. could mean restore service, protect customer data, or
keep the biggest accounts informed; the first hour looks different for each. Name the
framings and choose.

## 2. Problem Definition Worksheet

| Field | Questions |
|-------|-----------|
| Problem question | The core question, phrased as a question, SMART |
| Context | Internal/external situation, complications, trends, money available, skill gaps |
| Criteria for success | What makes it succeed or fail? When is it implemented? How will people notice? Make these SMART too |
| Scope of solution space | What's in, what's out. Broad enough to keep good options, narrow enough to focus |
| Constraints within solution space | What can or cannot happen inside the scope (budget, deadline, rules, politics) |
| Stakeholders | Decision makers, people who can support or block, internal and external actors affecting implementation |
| Key sources of insight | Where information comes from; what already exists so you don't redo it |

Scope = which areas the problem covers. Constraints = what can or can't happen inside them.

Common mistakes: missing a stakeholder needed for the recommendation to be actionable; scope
in/out not explicit or not agreed; constraints not stated honestly, which distorts time and
resource planning.

In the moment, run it as questions. Example: your flight is cancelled the night before an
on-site client workshop. Success = the workshop happens on time in some form. Scope: rebook,
switch to remote, or have a colleague lead. Stakeholders: the client sponsor, the colleague
who could step in, the attendees who blocked their morning. That's the worksheet in a minute.

The worksheet is a living document: refine it as you learn.

## 3. Impactful questions

Questions that sharpen the definition and cut scope. A product team proposed a 10-week
research study on everything that might drive users to cancel a subscription: pricing,
onboarding, feature gaps, support quality, billing friction. The lead asked "What decision will
this feed?" (whether to build a pause-instead-of-cancel option) and "Have we answered something
like this before?" A churn project the year before had shown that the deciding factor was
whether users hit the core feature in their first week. The study narrowed to that question
plus exit-survey reasons, in 3 weeks instead of 10.

Good ones to keep handy:
- What decision will this answer feed, and who makes it?
- What would success look like, concretely, and by when?
- What's off the table?
- Have we (or anyone) solved something similar? What turned out to matter?
- What would change your mind?

## 4. Issue trees and MECE

**Building a tree:** root on the left is the problem question; first level has 3 or 4
branches; each next level asks "what drives this?"; stop when each end point can be answered
by one analysis. Sketch 2 or 3 structures and iterate; a good tree reads logically from the
first level down. In a hurry, reuse structures that worked before, but check there isn't a
simpler one.

**MECE:** mutually exclusive, collectively exhaustive. No overlaps, no gaps.
- ME failure: "frontend bugs, backend bugs and API bugs" (API bugs are backend bugs).
- CE failure: "traffic comes from paid and organic search" (forgot referral, direct, email).
- Passes: profit = revenue drivers + cost drivers.

Tips: get input from people who know the domain; aim for 80% right and iterate; make the tree
exhaustive first and prune after. Pruning early is a trap: leaving "raise prices" out of "grow
revenue" because sales will object narrows the space before you know.

**Worked example (root cause: sign-ups dropped).** Weekly sign-ups fell 30% with no launch or
campaign change. The funnel: ad and search traffic → landing page → sign-up form → email
verification → first login. Leadership wants an answer by Friday. The instinct to have every
team "look into it" in parallel is no plan at all; the tree follows the funnel so each branch
maps to one metric.

```
Why did weekly sign-ups     ┌─ 1A. Fewer people are reaching the landing page?
drop 30%? ──────────────────┤        ├─ 2A. Paid traffic fell (budget, bids, ad disapproved)?
                            │        └─ 2B. Organic traffic fell (ranking drop, indexing issue)?
                            ├─ 1B. The same people arrive, but fewer start the form?
                            ├─ 1C. People start the form, but fewer finish it?
                            └─ 1D. People finish the form, but fewer verify their email?
```

Rejected second-level candidates under 1A, and why:
- "What happened when a competitor's sign-ups dropped?" A valid inquiry, but not on this branch.
- "Did this happen last year around this time?" Useful for brainstorming level 1 (seasonality),
  not specific to traffic sources.
- "Is something in our marketing causing it?" Not MECE: overlaps 2A and 2B.

**Worked example (solution search: grow revenue).** A small B2B SaaS wants 25% more annual
recurring revenue in 12 months with the current team.

```
How can we grow ARR 25%      ┌─ New customers: which acquisition changes    ┌─ Launch a partner/referral program
in 12 months with the ───────┤   add the most revenue?                ──────┤
current team?                │                                              └─ Add a self-serve trial
                             ├─ Existing customers: how do we expand     ┌─ Introduce a higher tier
                             │   revenue per account?               ─────┤     └─ H: annual plan with 2 months free
                             │                                           └─ Usage-based add-ons
                             └─ Retention: how do we lose less revenue to churn?
```

## 5. Prioritization

**Cause vs. solution.** Root-cause problems: rank by rough likelihood. Solution problems:
impact x feasibility.

**80/20.** Roughly 20% of the work gives 80% of the insight. Reviewing pricing across 400
products, about 50 of them drove most of the revenue; reviewing those first gave the answer.
It's a guideline, not "do exactly 20%". Revisit priorities as results come in: a disproved
hypothesis kills the analyses beneath it.

Needed precision depends on the decision: deciding whether a market is worth entering needs an
order of magnitude; reconciling payments needs to be right to the cent.

**Impact x feasibility matrix** (relative sizing is fine: S/M/L):

```
 Impact
   ▲
HI │ High impact, hard: make it easier?  │ High impact, feasible: DO FIRST
   │ relax a constraint? truly needed?   │
   ├─────────────────────────────────────┼──────────────────────────────
LO │ Low impact, hard: BOTTOM            │ Low impact, feasible: quick wins
   └─────────────────────────────────────┴─────────────────────────────▶ Feasibility
```

Pitfalls: working a long list top to bottom runs out of time halfway; tackling everything at
once causes analysis paralysis; prioritizing too early cuts branches that mattered.

## 6. Workplan Worksheet

For each prioritized end point: hypothesis → rationale (what must be true) → analysis that
tests it → source of data. Then timing, owner, dependencies.

| Field | Meaning |
|-------|---------|
| Issue | An important unresolved question, phrased so it's clear what answers it (a number, yes/no) |
| Hypothesis | The likely answer + sub-hypotheses; what must be true for it to hold |
| End product | What the analysis will produce; steers work to what's needed (enables 80/20) |
| Analyses | The work that supports or rejects the hypothesis; feasible and realistic |
| Sources | Internal/external: experts, databases, past projects |
| Timing / owner | Time in hours and owner; unowned items fall on the lead |

**Burden of proof.** Learn on day 1 what evidence the decision maker needs. Too little and the
analysis gets rejected; too much and you waste time on precision nobody asked for. Sometimes no
data will change their mind: know that early.

**Worked example (annual plan).** Hypothesis: an annual plan with 2 months free will lift ARR
without cannibalizing monthly revenue. End product: a one-page model of ARR impact under low,
mid and high adoption, with the break-even adoption rate. Analyses: share of current monthly
customers with 10+ months of tenure (likely adopters); churn rate of those customers; a quick
survey or pricing-page test on willingness to prepay.

## 7. Conducting analyses

- Analysis is not the answer. Being busy isn't the point; being busy with the right thing is.
- Forest vs. trees: step back regularly and ask whether the result moves the answer.
- Precision vs. accuracy: three decimals in the wrong direction help nobody.
- Do you know enough to stop, or did a surprise mean you need to go deeper?

## 8. Synthesis

Summary = concise, chronological facts. Synthesis = the integrated "so what", taking a
position. Synthesis = insight (what we learned) + implication (what next).

Example: "CI got stuck, the staging migration failed, and QA hasn't signed off" (summary) vs.
"The release slips to Monday" (synthesis).

**Worked example (three findings).** A team is deciding what to build next for a
note-taking app. Support: the top complaint is losing work when the connection drops. Usage
data: 40% of sessions happen on mobile, often on the move. Competitor scan: most rivals offer
offline mode only on paid tiers, and none on the web. Synthesis: "Offline editing, free on
mobile, is the feature most likely to cut our top complaint and give us an edge competitors
charge for, so it goes ahead of the next integration." Every clause traces to a finding.

How to get better: step back before speaking; ask "what did we learn / what do we do next";
test it with others; redo it against the data so the most vivid finding doesn't dominate; write
it in clear, strong language. Synthesis is what separates a strategist from an analyst.

## 9. Recommendation

Synthesis answers "so what?"; the recommendation answers "what do we do?".
- Actionable: clear ownership, buy-in, implementation timeline.
- Appropriate: the right solution for this organization.

Ask: What needs to happen? Whose buy-in? What resources? Which way of doing it fits this
organization best? Aligning and mobilizing people is half the battle: the recommendation has to
fit the organization's structures, incentives and beliefs, or it won't happen. Reserve time for
this step; teams often spend it all on analysis. Watch for confirmation bias: a "so what"
formed early needs challenging, not just confirming.

## 10. Biases and debiasing

Biases are heuristics: useful shortcuts that become harmful when they make you reconfirm the
past. Everyone has them.

| Bias | What it is | Example | Technique |
|------|------------|---------|-----------|
| Confirmation | Reading new evidence as proof of the existing hypothesis | "Three users in interviews loved the idea, so the market wants it" | Key assumptions check; analysis of competing hypotheses |
| Confidence | Discounting warning signs | "This migration can't fail, we tested it once" | Pre-mortem: imagine it failed, explain why |
| Stability | Clinging to what worked before | "Same sprint setup as the last project, it worked" | Relax constraints one by one; restate the problem from 4 to 6 viewpoints |
| Groupthink | Following the leader's view | "The CTO thinks so, so it's right" | Challenge session: strongest voice argues the other side |

## 11. Blank templates

**Problem Definition Worksheet**
```
Problem question (SMART):
Context:
Criteria for success:
Scope - in:            / out:
Constraints:
Stakeholders:
Key sources of insight:
```

**Issue tree**
```
[Problem question]
├─ 1A.
│   ├─ 2A.
│   └─ 2B.
├─ 1B.
└─ 1C.
MECE check: [ ] no overlaps  [ ] no gaps  [ ] each end point = one analysis
```

**Workplan**
| Issue | Hypothesis | End product | Analyses | Sources | Timing (h) / owner |
|-------|------------|-------------|----------|---------|--------------------|

**Synthesis**
```
Insight (what we learned):
Implication (what to do):
One sentence:
```

**Problem brief (saved file)**
```
# <Problem title>
Date:
## Problem question
## Worksheet
## Issue tree
## Priorities (and what's parked)
## Workplan
## Findings
## Synthesis
## Recommendation (owner, buy-in, timeline, next action)
```
