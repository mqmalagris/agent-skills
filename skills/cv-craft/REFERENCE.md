# cv-craft — reference

Loaded when drafting tailored CVs, applying market best practices, or preparing recruiter-screen answers.

## ATS-safe formatting

Tailored CVs must parse cleanly through Applicant Tracking Systems:

- Plain Markdown only. No tables, no columns, no text boxes.
- Standard section headers — `Summary`, `Skills`, `Experience`, `Education`. ATS keyword-matches these.
- One column. Left-aligned. No headers/footers carrying key info.
- When exporting to PDF: sans-serif body (Calibri, Arial, Inter). 10–11pt body, 14–16pt name.
- No images, icons, charts, or graphics — even tasteful ones break parsers.
- Date format `MM/YYYY – Present`. Avoid "current" or "ongoing".
- File name on export: `Firstname-Lastname-Role.pdf`.

## Bullet rules — XYZ method

Default formula (Google's resume guidance, validated by recruiter studies):

> **Accomplished [X], as measured by [Y], by doing [Z].**

- **X = the result / impact** (what improved, shipped, unblocked).
- **Y = the metric / scope** (number, %, latency, $, users, count).
- **Z = the action / how** (the system, integration, technique, decision).

Order can be inverted for rhythm — `[Z], [X], [Y]` reads well too. The three slots must all be present.

**Examples**

| Slot | Example A | Example B |
|------|-----------|-----------|
| X (impact) | cut checkout latency | unblocked weekly Shopify sync |
| Y (metric) | from 800ms p95 to 180ms | for 12 stores, 40k SKUs |
| Z (action) | by replacing N+1 Stripe calls with batched intents | by rebuilding the importer on EventBridge + idempotency keys |

→ *"Cut checkout p95 from 800ms to 180ms by replacing N+1 Stripe calls with batched payment intents."*
→ *"Unblocked weekly Shopify sync across 12 stores and 40k SKUs by rebuilding the importer on EventBridge with idempotency keys."*

**When Y is genuinely unknown:** keep X and Z, drop Y, but flag the bullet as `[no-metric]` in the master so future syncs can fill it. Target ≥ 60% of tailored bullets carrying a real Y.

**Other rules**
- **Action verb first** — Built, Architected, Migrated, Shipped, Cut, Owned, Led, Designed, Reduced, Tripled, Unblocked, Replaced, Consolidated.
- **One bullet, one outcome.** Do not "and-chain" unrelated work.
- **Past tense for past roles, present tense for current.**
- **Senior bullets emphasize scope and ownership.** Junior bullets emphasize delivery and learning.

## Bullet anti-patterns (rewrite if you see these)

**Weak verbs / framing**
- "Responsible for X" → "Owned X" or "Built X"
- "Worked on X" → "Built X" or "Shipped X"
- "Helped with X" → name the actual contribution
- "Assisted in X" → name the contribution
- "Participated in X" → name the contribution
- "Involved in X" → name the contribution
- "Contributed to X" → name the specific piece
- "Strong knowledge of X" → demonstrate via output, not assertion
- "Familiar with X" → drop or move to Skills (Beginner)

**Empty modifiers** (adjective without a system named)
- "scalable", "robust", "dynamic", "innovative", "cutting-edge", "state-of-the-art", "best-in-class", "world-class", "next-gen"

**AI-tell vocabulary** (recruiters and hiring managers screen these out as ChatGPT-generated)
- leverage, leveraging, leveraged → use, used
- delve, delved → cover, dig into
- seamlessly, seamless → drop
- robust, robustly → drop or replace with concrete property
- navigate, navigating (metaphorical) → drop
- spearhead, spearheaded → led, drove
- foster, fostered → built, grew
- meticulous, meticulously → drop
- harness, harnessing → use, used
- in the realm of, in the landscape of → drop
- multifaceted, holistic, comprehensive → drop unless literally true
- "It's worth noting that", "Notably", "Importantly" → drop
- "a testament to" → drop

**Punctuation**
- **No em-dashes (—) anywhere in CV or screen-prep.** Em-dashes are a strong AI-tell on LinkedIn and recruiter screens. Use a comma, period, or parenthesis instead. (Note: section headers in this skill's own markdown files use em-dashes for readability; CV output must not.)
- No ellipses (…). Trailing-off reads as uncertain.
- No exclamation marks.

## Skills section

- Lead with the JD's required skills the user actually has.
- Group: `Proficient`, `Intermediate`, `Beginner`. Be honest — recruiters notice mismatches between depth and bullet evidence.
- Do not stuff keywords. Listing a tech the user cannot speak to is a fast-track to a failed screen.
- Include both spelled-out and acronym forms once if both appear in JDs (e.g. "TypeScript / TS", "AWS Lambda").

## Length

- ≤ 8 years experience: 1 page.
- 8–15 years: 1–2 pages.
- 15+ years or academic / consulting: up to 3 pages, only if every page earns its space.
- Trim weakest bullets first, then oldest roles, then certifications/awards. Never trim the summary or the current role.

## Tailoring rules

- **Never invent.** Only select, reorder, and rephrase what the master already contains.
- **Match JD vocabulary** where the user has the underlying skill — say "Vercel" not "deploy platform" if the JD says Vercel.
- **Drop bullets and entire roles** that do not move the needle for this JD. The master keeps the full record.
- **Keep the summary aligned** to the role title in the JD.

## ATS scoring rubric

Run before writing any tailored CV. Score across five categories, each 0–20, total 0–100. Report the score, the per-category breakdown, and the failing items. **Hard gate: do not write below 80 without explicit user override.**

### Categories

**1. Keyword match (0–20)**
- Extract required + preferred skills from JD as a set `K`.
- Count `H` = JD keywords that appear verbatim in the tailored CV (case-insensitive, allow declared synonyms like "Postgres ↔ PostgreSQL").
- Score = round(20 × H / |K|), capped at 20.
- **Pass ≥ 16** (≥ 80% coverage). **Warn 12–15.** **Fail < 12.**

**2. Bullet quality / XYZ compliance (0–20)**
- For each experience bullet, classify: `full-XYZ` (X+Y+Z all present), `partial` (XZ or XY), `weak` (verb-only or descriptive).
- Score = round(20 × (full-XYZ × 1.0 + partial × 0.5) / total bullets).
- **Pass ≥ 16.** **Warn 12–15.** **Fail < 12.**

**3. Structure / ATS parseability (0–20)**
- 4 points each: standard section headers (`Summary`, `Skills`, `Experience`, `Education`); single-column plain Markdown (no tables/columns/text-boxes/images); `MM/YYYY – MM/YYYY` dates throughout; `Stack:` line per role; one bullet per outcome.
- **Pass = 20.** **Warn 16.** **Fail < 16** (any structural break is a parser risk).

**4. Length / density (0–20)**
- Within target page count (see [Length](#length)): 12 pts.
- ≥ 60% of bullets carry a number: 4 pts.
- Summary ≤ 4 sentences: 2 pts.
- No empty sections: 2 pts.
- **Pass ≥ 16.** **Warn 12–15.** **Fail < 12.**

**5. Voice / anti-AI-tell (0–20)**
- Start at 20. Subtract 2 per AI-tell word hit (`leverage`, `delve`, `seamless`, `robust`, `spearhead`, `foster`, etc. — see anti-patterns list). Subtract 2 per em-dash. Subtract 2 per empty modifier (`scalable`, `cutting-edge`). Floor at 0.
- **Pass ≥ 16.** **Warn 12–15.** **Fail < 12.**

### Report format

Always render the score as:

```
ATS Score: 84/100  [PASS]

  Keyword match       18/20  ✓  (9/10 JD skills present; missing: "Kubernetes")
  XYZ bullet quality  14/20  ⚠  (3 bullets missing a metric — flagged below)
  Structure           20/20  ✓
  Length / density    16/20  ✓
  Voice               16/20  ⚠  (em-dash in line 14; "leverage" in line 22)

Fixes before write:
  - Bullet L14: replace em-dash with comma.
  - Bullet L22: rewrite "leverage AWS" → "use AWS".
  - Bullets L31, L36, L41: add a metric (Y) or mark [no-metric] in master.
```

Below 80: list every failing item, then ask the user to confirm fixes (auto-applied) or override.

## Voice rules

The CV and screen-prep must sound like the user, not a template.

- **No em-dashes.** Use commas, periods, or parentheses.
- **No AI-tell words.** See anti-patterns above. If a word is technically correct in context (e.g. "robust" in `robust to retries`), keep it; otherwise replace.
- **Prose over bullet-stuffing in Summary and screen-prep narrative answers.** Bullets are for Experience/Skills/Projects.
- **Concrete nouns over adjectives.** "Lambda + EventBridge middleware" not "scalable serverless architecture".
- **First-person in screen-prep, third-person-implied in CV body.** CV bullets drop "I" — start with the verb.
- **Match the user's existing tone.** Read the master Summary first; mirror cadence, sentence length, and lexicon.
- ≤ 120 words per draft answer. Recruiter calls run on rhythm, not paragraphs.
- **Salary:** ask the user for their range. Never invent a number.
- **Gaps:** address openly. Pattern: *"I have not used X in production. I have used the closest analogue Y, and have read the Z docs / built a side project."*
- **Questions to ask the recruiter:** focus on team, ramp, success metrics, on-call, growth — not benefits / vacation.

## JD signal extraction

When parsing a JD, pull:

- Required skills (must-have)
- Preferred / nice-to-have
- Years of experience required
- Seniority level (IC / Lead / Manager)
- Domain (fintech / e-commerce / health / etc.)
- Stack and infrastructure
- Soft signals (startup vs enterprise, async vs in-office, leadership vs IC)
- Red flags (unpaid take-homes, vague comp, recent layoffs, unrealistic stack breadth)

## PDF stylesheet (default `cv-style.css`)

If `cv-style.css` does not exist alongside the master, create it with this content. ATS-safe: single column, sans-serif, no graphics, neutral hierarchy.

```css
body {
  font-family: 'Inter', 'Calibri', 'Arial', sans-serif;
  font-size: 10.5pt;
  color: #111;
  max-width: 7.2in;
  margin: 0 auto;
  line-height: 1.4;
}

h1 { font-size: 22pt; margin: 0 0 0.1em 0; font-weight: 700; }
h1 + p { margin-top: 0; font-size: 12pt; color: #333; margin-bottom: 0.6em; }
h2 {
  font-size: 13pt;
  font-weight: 700;
  border-bottom: 1px solid #444;
  padding-bottom: 2px;
  margin-top: 1.1em;
  margin-bottom: 0.4em;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
h3 { font-size: 11.5pt; font-weight: 700; margin-top: 0.8em; margin-bottom: 0.15em; }

p, li { margin: 0.25em 0; }
ul { padding-left: 1.2em; margin: 0.3em 0 0.6em 0; }
strong { font-weight: 600; }
a { color: #111; text-decoration: none; }
code { background: #f4f4f4; padding: 1px 4px; border-radius: 3px; font-size: 0.92em; font-family: 'Consolas', 'Menlo', monospace; }
hr { border: none; border-top: 1px solid #ddd; margin: 1em 0; }
```

## Common JD-to-master mismatches and how to handle them

| Situation | Handling |
|-----------|----------|
| JD requires skill the master does not have | Flag as a gap. Do not list. Surface in screen-prep. |
| JD requires skill the master lists as Beginner | List it, with honest framing in screen-prep. |
| JD lists 12 stacks and asks for 5+ years in each | Treat as wishlist. Show the user. Tailor to the strongest matches. |
| Master has skill JD does not mention | Drop unless it strengthens an adjacent bullet. |
| JD vocabulary differs from master ("Postgres" vs "PostgreSQL") | Match the JD spelling. |
