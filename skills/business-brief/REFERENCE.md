# business-brief reference

Read the section you need; nothing here has to be loaded up front.

1. [Sources by question](#1-sources-by-question)
2. [Business models, levers and where engineering moves them](#2-business-models-levers-and-where-engineering-moves-them)
3. [Unit economics: vocabulary and rules of thumb](#3-unit-economics-vocabulary-and-rules-of-thumb)
4. [Sizing](#4-sizing)
5. [Moats and right to win](#5-moats-and-right-to-win)
6. [Health and red flags](#6-health-and-red-flags)
7. [Side jobs: can they pay?](#7-side-jobs-can-they-pay)
8. [Question bank](#8-question-bank)
9. [Worked example (fictional)](#9-worked-example-fictional)

---

## 1. Sources by question

| Question | Best sources | Watch out for |
|----------|--------------|---------------|
| How they make money | Pricing page, product pages, annual report "Business" section, investor deck, earnings call | List prices; enterprise deals are negotiated well below them |
| Model and lever | Pricing unit (seat, order, transaction, GB, request), how case studies describe customers, JD wording ("own checkout", "drive activation") | Companies blending models; name the main one and the secondary |
| Market | Customer-count claims, case-study segments, how many businesses of that type exist (government statistics, industry associations), competitors' customer counts | Research-firm TAM headlines: top-down and written to sell reports |
| Competition | "<company> alternatives", "<company> vs", their own comparison pages, review-site category pages, reviews that mention switching | Comparison pages are biased by design |
| Health | Funding announcements, filings, layoff news and trackers, headcount trend in search snippets, job-post volume over time, Glassdoor/Blind | Press revenue figures are secondhand unless the company said them; crowd reviews are noisy, present ranges |
| Open roles | Public job-board APIs return the full list and descriptions when the careers page renders them with JavaScript: Ashby `api.ashbyhq.com/posting-api/job-board/<slug>?includeCompensation=true`, Greenhouse `boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true`, Lever `api.lever.co/v0/postings/<slug>?mode=json` | Check the posting date; an old date can be an evergreen listing rather than a role nobody can fill |
| Size and age (any company) | Company registries: Brazil CNPJ lookup (opening date, status, legal size band), US state registries and SEC EDGAR (filings; Form D shows private raises), UK Companies House (filed accounts), Canadian corporate registries | Registered capital is not revenue |

**Brazil specifics.** The CNPJ size band is a legal revenue ceiling: MEI and ME cap annual
gross revenue low, EPP caps it at a few million reais (LC 123/2006; check current limits). A
client registered as ME is a small business whatever its website looks like. Reclame Aqui shows
how they treat customers, and Jusbrasil shows lawsuits, including unpaid-supplier cases.

## 2. Business models, levers and where engineering moves them

| Business model | Lever revenue depends on | Where engineering moves it |
|---|---|---|
| Subscription / SaaS | Retention, expansion (seats, tiers), activation | Time to value in onboarding; reliability and data integrity (top churn drivers); integrations (switching cost); upgrade and billing flows; enterprise unlocks (SSO, audit logs, compliance) that open bigger deals |
| Freemium / product-led | Free-to-paid conversion, activation | Instrumented activation funnel, paywall and limit placement, cheap-to-serve free tier |
| Marketplace | Transaction volume (GMV) × take rate, liquidity on both sides | Search and matching relevance, trust and safety, payments and payouts, supply-side onboarding |
| E-commerce / DTC | Conversion × average order value × repeat rate | Page speed and checkout conversion, uptime on campaign days, reorder and subscription flows, recommendations and bundles, inventory and fulfillment integrations (cost) |
| Direct selling / distributor networks | Active distributors, qualifying volume, reorders (autoship) | Distributor back office and volume visibility, enrollment and autoship flows, commission accuracy, compliance in what the site claims |
| Ads-funded / media | Engaged time × audience × ad yield | Feed and content performance, ad stack latency and viewability, measurement |
| Usage-based / API / infra | Consumption per account, time to first use | Time to first call or deploy, reliability and SLAs, unit cost of serving (gross margin), metering and billing accuracy |
| Fintech / payments | Volume × take (fees, interchange, interest) minus losses | Approval rates, fraud and credit losses, KYC throughput, uptime |
| Agency / services / consultancy | Billable utilization × rate, margin, renewals | Reuse and delivery speed (margin on fixed bids), estimation accuracy, client-visible quality that drives renewals |
| Licensed / on-prem software | New licenses, maintenance renewals | Upgrade path, support cost, ease of deployment |

Business model vs pricing model: two companies can both charge per seat while one lives on
retention (SaaS) and the other on new licenses (on-prem). The lever comes from the business
model, not from the price tag.

## 3. Unit economics: vocabulary and rules of thumb

**Vocabulary**

- **ARPU / ARPA**: average revenue per user / per account, per month or year
- **AOV**: average order value (e-commerce)
- **GMV** and **take rate**: total value transacted on a marketplace, and the share it keeps as revenue
- **Gross margin**: revenue minus the direct cost of delivering it, as a share of revenue
- **CAC**: cost to win one customer; **payback**: months of gross margin to earn CAC back
- **LTV / CLV**: what a customer is worth over the relationship
- **Churn**: logo churn (customers lost) vs revenue churn; **NRR**: revenue kept from last
  year's customers including expansion; above 100% means the base grows on its own
- **Burn** and **runway**: net cash spent per month, and months until the money runs out

**Rules of thumb.** Rough, they vary by segment and year. Use them to sanity-check an estimate,
never as the company's numbers.

- Software gross margins usually sit around 70-80%. Usage-based infra runs lower, since
  compute is a direct cost. A marketplace books only its take rate as revenue, so its
  "revenue" is a slice of GMV. E-commerce and services margins vary widely by category; in
  services the margin lives in utilization and rate, and fixed-price overruns come straight
  out of it.
- Marketplace take rates commonly fall between 10% and 30% of GMV: lower for high-ticket and
  B2B, higher for managed marketplaces.
- SaaS: small-business customers churn a few percent a month; enterprise churn is measured
  per year. LTV:CAC around 3:1 and CAC payback under 12-18 months are the usual "healthy"
  bars.
- Revenue per employee, as an order-of-magnitude check: venture-backed SaaS often lands
  around $100-250k per employee, services firms lower, and much lower where salaries are
  lower (Brazil, most of LATAM). Present the result as a range with the method, never as
  their revenue.
- Burn: for a software startup, headcount × fully loaded cost per head is most of it. Runway
  ≈ last raise ÷ monthly burn, minus the months since the raise. A startup that raised $5M two
  years ago with 40 people is almost certainly raising again, cutting, or already profitable;
  find out which.

## 4. Sizing

- **Bottom-up**: potential buyers × realistic price per year, then × a plausible share.
  Example (made-up): 30,000 independent clinics × $1,200/year = $36M/year if every clinic
  bought; at a 5-10% share, a $2-4M ARR ceiling for one player in its early years.
- **Top-down** figures (a share of a research-firm market) only as a cross-check.
- **Framing**: today's market vs the one the product could create. Aswath Damodaran valued
  Uber in 2014 by sizing the taxi market; Bill Gurley's "How to Miss By a Mile" argued the
  product would expand that market many times over. Ask which kind of company this is.
- For an engineer, market size mostly answers "is there room to grow, so will there be
  budget for engineering?" Precision isn't the point.

## 5. Moats and right to win

| Moat | Sign of it | Engineering angle |
|------|-----------|-------------------|
| Network effects | Product gets better as more people use it; two-sided liquidity | Matching, trust, performance at scale |
| Switching costs | Customer data, integrations, trained staff, embedded workflows | Integrations, data model depth, migration tools (their own and the competitor's) |
| Scale economies | Unit cost falls with volume | Infra efficiency, automation |
| Brand | Customers name it unprompted; premium pricing holds | Quality and reliability that protect it |
| Distribution | Channel, partners, app-store rank, sales team | Partner APIs, SEO and performance, sales-enablement tooling |
| Proprietary data | Data competitors can't get | Pipelines, data quality, privacy compliance |
| Regulation / licenses | Licensed activity, certifications | Compliance work as a feature |
| None yet | Early stage | Speed and focus; say so plainly |

From the engineering seat: work that deepens the moat earns polish and quality; table stakes
get the cheapest version that holds up, or get bought instead of built. "A competitor has it"
makes something table stakes at most.

## 6. Health and red flags

**Good signs**: a recent raise that fits the headcount, hiring in core product and
engineering teams, growing public customer list, transparent pricing, reviews that praise
reliability.

**Yellow to red**:

- Last raise 18-24+ months ago, small relative to headcount, and no profitability signal:
  raising or cutting soon
- Layoffs in the last 12 months, especially more than one round
- Concentration: one client, one channel, or one platform (marketplace seller, app-store
  dependent, built on a single partner's API)
- Leadership churn (CEO or CTO changes), or a pivot in the last year
- Reviews about billing problems, support that disappeared, or repeated outages
- The same specific role reposted again and again, or "urgent" for months. Evergreen
  "we always hire for this" posts at remote-first companies are normal and not a flag
- Lawsuits or regulator actions

**Offers**: options are worth what the exit path makes them worth. Weak health turns equity
into a lottery ticket; price the offer on cash and treat equity as upside.

## 7. Side jobs: can they pay?

- **Age and size**: registry opening date and size band, headcount, funding
- **Who signs**: is the contact the budget holder or an intermediary? Who else has to say yes?
- **Payment signals**: complaints about late payment (Reclame Aqui, Glassdoor, freelancer
  communities), procurement terms at big companies (net 60 or 90 days), currency and
  invoicing for international clients
- **Scope signals**: urgent + vague + fixed-price is where margin goes to die
- **Protection**: a deposit or milestone billing covers most of the above
- **Your side**: does your employment contract allow it (moonlighting clause, non-compete, IP
  assignment, a conflict with your employer's clients)? Do the hours fit around the day job
  before the client's deadline? Both are cheaper to check before the call than after the
  proposal

## 8. Question bank

**Job**

- "Which number does this team own, and how did it move last quarter?"
- "What's the main reason customers leave?"
- "Where does growth come from right now: new customers, expansion, or price?"
- "Which engineering investment changed the business most in the last year?"
- Offer stage: "What's the plan to the next raise or to profitability?" and "How concentrated
  is revenue across customers?"

**Side job**

- "What number do you report to your boss or investors each month?"
- "What happens to the business if this isn't fixed this quarter?"
- "What did you try before, and why didn't it stick?"
- "Who else needs to say yes before we start?"
- "How do you usually pay vendors: terms, deposit, milestones?"

## 9. Worked example (fictional)

Shows the tagging, the lever, and the value anchor. Company and numbers are made up.

> **Clinicflow: business brief (2026-11-03)**
> side job · prospect · performance audit pitch · quick
>
> **In short:** Scheduling and billing SaaS for independent dental clinics in Brazil, R$290
> per clinic per month ([pricing page](https://example.com/pricing)). Revenue lives on
> retention: a clinic that leaves takes ~R$3.5k/year with it. Their reviews complain about
> the agenda freezing on Monday mornings, so reliability is the pitch, not new features.
>
> **How they make money:** subscription, priced per clinic. Lever = retention, then expansion
> to multi-chair plans.
>
> **Market and competition:** independent dental clinics in Brazil, a large but price-sensitive
> segment `[unknown: clinic count]`. Alternatives are generic clinic ERPs, a paper agenda plus
> WhatsApp, or doing nothing; their edge is dental-specific billing.
>
> **Health:** CNPJ opened 2019, EPP size band ([registry](https://example.com/cnpj)); 25 people
> on LinkedIn `[inferred: search snippet]`; no public raise `[unknown]`.
>
> **Where engineering moves the number:** (1) agenda load time and uptime at peak hours, the
> top churn complaint ([reviews](https://example.com/reviews)); (2) billing integration
> errors, which create support load and churn.
>
> **Your angle (pitch):** a 20-hour audit of the agenda's peak-hour performance, framed as
> churn risk. Value anchor: at ~1,500 clinics `[inferred: "1.500 clínicas" on homepage]`, each
> point of monthly churn avoided keeps ~15 clinics a month; after a year that's ~180 clinics,
> ~R$52k/month in MRR `[inferred]`. Don't pitch a
> redesign; it's table stakes for them.
>
> **Questions to ask:** "How many clinics cancelled last quarter, and what did they say?"
> (founder) · "Who signs vendor contracts, and how do you usually pay?" (founder)
>
> Sources: [pricing](https://example.com/pricing) · [registry](https://example.com/cnpj) ·
> [reviews](https://example.com/reviews)
