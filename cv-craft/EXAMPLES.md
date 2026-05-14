# cv-craft — examples

Concrete reference output for `tailor` and `screen-prep` modes. Loaded only when drafting either.

## Sample tailored CV

**Inputs:**
- Master: full-stack engineer, 8 years experience, stack covers Next.js, Node, AWS, Stripe, Shopify, Angular, Ionic, Cloudflare Workers, MongoDB.
- JD: *Senior Full-stack Engineer at Acme — Next.js + AWS + Stripe.*

**Tailored output (single page):**

```markdown
# Matheus Malagris

Senior Full-stack Engineer

**Location:** Rio de Janeiro, Brazil — Remote
**Email:** malagrismatheus@gmail.com
**LinkedIn:** linkedin.com/in/matheus-malagris
**GitHub:** github.com/mqmalagris

## Summary

Full-stack engineer with 8+ years of programming and 5 years building production web apps on Next.js, Node.js, and AWS. Track record shipping Stripe-integrated commerce middleware and scalable Lambda-driven backends. Comfortable owning a feature end-to-end from API design through deployment.

## Skills

**Proficient:** TypeScript, Next.js, Node.js, AWS (Lambda, S3, CloudFormation, RDS/Aurora, SQS, SES, EventBridge), Stripe, Shopify Admin GraphQL, MongoDB, SQL

**Intermediate:** React, Angular, Cloudflare Workers, Astro

**Beginner:** Svelte, Remix, Flutter

## Experience

### Full-stack Developer
**Arctic Leaf**, Meridian, US — Remote
01/2022 – Present

- Architected Lambda + EventBridge middleware integrating Shopify, Stripe, Recharge, and Aftership for a multi-store commerce client.
- Designed CloudFormation stacks and Aurora schemas powering scalable e-commerce integrations.
- Built Next.js storefronts with Cloudflare Workers edge handlers for sub-100ms personalization.

**Stack:** TypeScript, Next.js, Node.js, AWS, Stripe, Shopify GraphQL, MongoDB
```

**Notes on the diff from master to tailored:**

- Headline `Full-stack Developer` → `Senior Full-stack Engineer` (matches JD's role title and seniority).
- Skills section reordered: TypeScript / Next.js / AWS / Stripe pulled to the front of `Proficient`.
- Older Daydream / Kosher GPS role dropped — Angular/Ionic not aligned with JD; master keeps it.
- Bachelor of Electrical Engineering omitted on the one-page version; reinstate if the JD weights education.
- Summary rewritten — same facts, ordered around JD priorities.

## XYZ bullet rewrites (before / after)

The tailor pass converts master bullets into the XYZ formula. Concrete cases:

| Before (master) | After (tailored, XYZ) |
|---|---|
| Worked on Shopify integrations for multiple stores. | Unblocked weekly Shopify sync across 12 stores and 40k SKUs by rebuilding the importer on EventBridge with idempotency keys. |
| Responsible for backend performance improvements. | Cut checkout p95 latency from 800ms to 180ms by replacing N+1 Stripe calls with batched payment intents. |
| Helped migrate the team from REST to GraphQL. | Migrated 14 internal endpoints from REST to Shopify Admin GraphQL, eliminating 6 round-trips per checkout and dropping average response time by 38%. |
| Built a robust serverless architecture for ingestion. | Designed an SQS + Lambda ingestion pipeline processing 2M events/day with a 99.95% delivery rate and DLQ-based replay. |
| Spearheaded the move to TypeScript across the codebase. | Led the TypeScript migration of 80k LoC across 4 services, eliminating ~120 prod runtime errors per month traced to type drift. |

Anti-patterns flagged: `worked on`, `responsible for`, `helped`, `robust` (empty modifier), `spearheaded` (AI-tell). Each rewrite supplies an explicit X (impact), Y (metric/scope), and Z (action).

## Sample ATS score report

Rendered in `tailor` mode after step 5, before any write. Score must be ≥ 80 to proceed without an explicit override.

```
ATS Score: 84/100  [PASS]

  Keyword match       18/20  ✓  (9/10 JD skills present)
                                 missing: "Kubernetes"
  XYZ bullet quality  14/20  ⚠  (8/10 full-XYZ, 1 partial, 1 weak)
                                 weak: L41 "Built internal admin tools."
  Structure           20/20  ✓
  Length / density    16/20  ✓  (1 page; 7/10 bullets carry a number)
  Voice               16/20  ⚠  (em-dash on L14; "leverage" on L22)

Fixes before write (auto-applied unless you object):
  - L14: replace em-dash with comma
  - L22: rewrite "leverage AWS Lambda" → "use AWS Lambda"
  - L41: rewrite to XYZ — propose:
      "Built an internal admin tool that cut customer-support
       resolution time from 8min to 2min by exposing order +
       refund actions over a single Shopify-Stripe view."
  - Surface "Kubernetes" gap in screen-prep (no master coverage)

Confirm fixes? (y / edit / override)
```

A `[FAIL]` example (score < 80) lists every category below threshold and blocks the write until either fixes are applied or the user explicitly overrides the gate.

## Sample screen-prep pack

**Output file:** `screen-prep-acme-senior-fullstack.md`

```markdown
# Screen Prep — Acme — Senior Full-stack

## 30-second intro pitch

"I'm a full-stack engineer based in Rio with eight years of programming experience, the last five focused on Next.js, Node, and AWS. At Arctic Leaf I've architected Lambda-based commerce middleware integrating Shopify, Stripe, and Recharge for multi-store retailers. I'm looking for a senior role where I can own scalable backend integrations end-to-end."

## Why Acme

1. The JD emphasizes Stripe + AWS — directly aligned with my last two years of work.
2. Remote-first culture matches how I have shipped most of my career.
3. {ASK USER: any product or mission angle to add — answer is stronger when personal}

## Salary expectation

{ASK USER for range. Suggested phrasing once provided: "Based on my eight years of experience and the senior IC level, I'm targeting USD {X}–{Y}. Happy to discuss the full package."}

## Top 8 likely first-call questions

1. **Walk me through your background.** *(use the 30-second pitch above)*
2. **Tell me about a project you owned end-to-end.** *(Lambda + EventBridge middleware, Arctic Leaf — name the integrations and the outcome)*
3. **How do you approach scaling Lambda-based integrations?** *(idempotency, SQS dead-letter handling, EventBridge for fan-out, observability via CloudWatch)*
4. **Tell me about a time you debugged a hard production issue.** *(pick a real incident from master's bullets — name the symptom, the root cause, the fix, the prevention)*
5. **Why are you looking to leave Arctic Leaf?** *(growth-framed, not negative — "I am ready for senior-IC scope, and the projects I want to own are not on my current team's roadmap")*
6. **What is your experience with Stripe specifically?** *(billing flows, webhooks, idempotency keys, Recharge subscription orchestration)*
7. **How do you balance shipping speed and code quality?** *(test pyramid, what you skip on a prototype vs production, when you take on tech debt deliberately)*
8. **What questions do you have for us?** *(see below)*

Each answer ≤ 120 words.

## Gaps and risks

- **Kubernetes** — JD lists it; master shows light exposure only. Honest framing: "I have run containerized workloads on Lambda and ECS in production. My Kubernetes exposure has been research and side projects; I would ramp quickly given my AWS background."
- **Years on Stripe** — master shows ~2 years on Stripe directly. If the JD wants 4+, frame around the depth of the work, not the duration.

## Questions to ask the recruiter

1. What does the first 60 days look like for this role?
2. How does the team measure success six months in?
3. What is the on-call rotation, and how often does it page?
4. What is the biggest engineering challenge the team is working through right now?
```

## When to deviate from these examples

- **Non-engineering roles** — strip the `Stack:` lines, replace with domain artifacts (campaigns shipped, papers published, deals closed).
- **Career-change CV** — lead with a "Selected Projects" or "Transferable Skills" section before Experience.
- **Academic CV** — extend to 2–3 pages, include Publications and Teaching sections (omit ATS rules — academic search is human-driven).
- **Two-page CVs** — keep the summary, current role bullets, and skills tight on page 1; let older roles and education fall to page 2.
