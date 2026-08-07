# cv-master.md schema

The master CV lives at `<dir>/cv-master.md` where `<dir>` is the user's CV directory (resolved via the [Path resolution](SKILL.md#path-resolution) flow in `SKILL.md`). Use this schema when bootstrapping or syncing. The master is **complete** — it includes everything the user has shipped. Tailoring trims it down later.

## Schema

```markdown
# {Full Name}

{Headline — e.g. "Full-stack Developer" or "Senior Backend Engineer"}

**Location:** {City, Country}
**Email:** {email}
**Phone:** {phone}
**LinkedIn:** {url}
**Portfolio / GitHub:** {url}
**Work authorization:** {e.g. "Brazil citizen — open to remote / contractor"}

## Summary

{3–4 sentences. Opens with role + years experience. Names primary stack. Names one or two distinctive angles or domain strengths.}

## Skills

**Proficient:** {comma-separated}

**Intermediate:** {comma-separated}

**Beginner:** {comma-separated}

> Note: blank lines between the three skill levels are required. Single newlines collapse to spaces in CommonMark and most PDF renderers, producing one run-on paragraph. Always use blank lines OR a `<br>` tag.

## Professional Experience

### {Job Title}
**{Company}**, {Location} — {Remote | Hybrid | On-site}
{MM/YYYY} – {MM/YYYY or Present}

- {Bullet — action verb, concrete output, metric where credible}
- {Bullet}
- {Bullet}

**Stack:** {comma-separated tech used in this role}

### {Next role…}
…

## Side Projects

### {Project Name} — {one-line descriptor}
**Stack:** {tech}
**Link:** {repo or live URL, optional}

- {Bullet — concrete capability or architectural choice}
- {Bullet}

## Education

### {Degree}
**{Institution}**, {Location} — {MM/YYYY} – {MM/YYYY}

- {Relevant coursework, thesis, awards}

## Languages

- {Language}: {Native | Fluent | Conversational | Basic}

## Certifications  *(optional, omit section if empty)*

- {Cert} — {Issuer, Year}

## Awards / Speaking  *(optional, omit section if empty)*

- {Item — venue, year}
```

## Field rules

- **Dates** in `MM/YYYY` format. Use `Present` for current role.
- **Bullets follow the XYZ method:** `Accomplished [X], as measured by [Y], by doing [Z]`.
  - **X = result/impact**, **Y = metric/scope**, **Z = action/how**. Example: *"Cut checkout p95 from 800ms to 180ms by replacing N+1 Stripe calls with batched payment intents."* Full guidance in [REFERENCE.md — Bullet rules](REFERENCE.md#bullet-rules--xyz-method).
  - If Y is genuinely unknown at master-time, write the X+Z bullet and append the literal tag `[no-metric]` so a later pass can fill the metric. Never invent a metric.
- **Bullets start with action verbs** — Built, Architected, Migrated, Reduced, Shipped, Owned, Led, Cut, Tripled, Unblocked, Replaced, Consolidated. Avoid weak verbs (Worked on, Helped with, Was responsible for, Assisted in, Participated in).
- **Numbers beat adjectives** — "cut p95 from 800ms to 180ms" beats "improved performance significantly".
- **One bullet, one outcome.** Do not chain unrelated work with "and".
- **No em-dashes (—) and no AI-tell vocabulary** (`leverage`, `delve`, `seamless`, `robust`, `spearhead`, `foster`, etc. — full list in [REFERENCE.md — Bullet anti-patterns](REFERENCE.md#bullet-anti-patterns-rewrite-if-you-see-these)).
- **Stack line per role** — pulls double duty for ATS keyword matching and human readability.
- **Master keeps everything.** Never delete past roles or projects from the master. Tailored outputs do the trimming.
- **Honest skill levels.** Proficient = can lead, debug, and teach. Intermediate = ship features unsupervised. Beginner = used in side projects or learning. Mismatches between skill level and bullet evidence are a red flag in screens.

## Bootstrapping prompts (for the assistant)

When interviewing a new user in bootstrap mode, use prompts like:

- "What is your current or most recent role title?"
- "List the technologies you would be comfortable being asked deep questions about in an interview."
- "For your most recent role: what is one thing you built end-to-end that you are proud of? What was the measurable outcome?"
- "Any side project that demonstrates skill the day-job does not?"

Save after each section. Do not push the user through all eight at once — interview rhythm produces better content.
