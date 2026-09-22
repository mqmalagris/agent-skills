---
name: cv-craft
description: Maintain a canonical master CV in Markdown and produce tailored, ATS-friendly resumes and recruiter-screen prep packs from job descriptions. Supports five modes — bootstrap (build master from scratch via interview), sync (import existing resume in any format into master, with optional standalone rewrite output), check (assess fit against a JD before committing to an application, writing no CV), tailor (generate CV matched to a JD), and screen-prep (draft answers for first recruiter-call questions). Use when the user asks to update their CV/resume, rewrite an existing CV, tailor a resume to a job posting, check a job description or ask whether a role is worth applying to, prepare for a recruiter screen, import a resume PDF/docx into Markdown, or runs /cv-craft.
---

# cv-craft

Maintain a master CV in Markdown and produce tailored CVs + recruiter-screen prep packs from it. Path-agnostic: the user picks where files live, the skill remembers it.

## Non-negotiable rules

Read before every mode. Violating these destroys candidate credibility in interviews.

1. **Never fabricate metrics.** If the source has no number and none can be reasonably estimated from surrounding text, write the bullet qualitatively. Mark missing metrics inline with `[DADO AUSENTE: qual era X?]`. Mark inferred-but-reasonable metrics with `[ESTIMADO]`.
2. **Never delete information silently.** Anything removed from the source goes into the post-CV change log with a one-line justification. The candidate can restore it on the next pass.
3. **Never alter facts.** Job titles, employers, dates, technologies, and accomplishments must match the source exactly. Rewrite form, not content.
4. **Surface inferred target profile.** When no JD is supplied (sync standalone rewrite, bootstrap polish), infer role / seniority / specialization / company type from the source. Declare it in the post-CV section so the candidate can correct.

See [REFERENCE.md — Data integrity](REFERENCE.md#data-integrity) and [Post-CV section template](REFERENCE.md#post-cv-section-pt-br).

## Quick start

1. Detect mode from the user's request: `bootstrap` | `sync` | `check` | `tailor` | `screen-prep`. Ask if ambiguous.
   - A pasted JD with "check this", "what do you think", "should I apply", "am I a fit", or no instruction at all is `check`, not `tailor`. Do not write a CV until asked.
2. Resolve the **CV directory** (see [Path resolution](#path-resolution) below). All artifacts live there.
3. Read or create `cv-master.md` per [MASTER_TEMPLATE.md](MASTER_TEMPLATE.md).
4. Run the per-mode flow below. Always preview, wait for confirmation, then write.

## Path resolution

The skill is path-agnostic. Resolve in this order before any read or write:

1. **Check memory** for a `reference`-type entry naming the user's CV directory (look for an entry with `cv-craft` or `CV directory` in its name/description).
2. If found, derive paths from `<dir>`:
   - Master: `<dir>/cv-master.md`
   - Tailored: `<dir>/cv-{company}-{role-slug}.md`
   - Screen-prep: `<dir>/screen-prep-{company}-{role-slug}.md`
   - Stylesheet: `<dir>/cv-style.css`
   - Gap ledger: `<dir>/gap-ledger.md` (see [Gap ledger](#gap-ledger))
3. **If not in memory, ask the user**:
   - In `sync` / `tailor` / `screen-prep`: *"Where is your master CV? (paste an absolute path, or tell me the folder it lives in)"*
   - In `bootstrap`: *"Where should I create your master CV? (paste an absolute folder path; I'll put `cv-master.md` and outputs there)"*
4. After the user answers, **save a memory reference entry** so future runs do not re-prompt. Format:
   ```markdown
   ---
   name: cv-craft directory
   description: Where cv-craft stores the user's master CV, tailored CVs, screen-prep packs, and stylesheet
   type: reference
   ---

   CV directory: `<absolute-path>`
   - Master: `<dir>/cv-master.md`
   - Stylesheet: `<dir>/cv-style.css`
   - Tailored CVs: `<dir>/cv-{company}-{role-slug}.md`
   - Screen-prep: `<dir>/screen-prep-{company}-{role-slug}.md`
   - Gap ledger: `<dir>/gap-ledger.md`
   ```
   And add a one-line pointer to `MEMORY.md`.
5. If the master file does not exist at the resolved path and the user is not in `bootstrap` mode, ask whether to bootstrap or sync first — do not invent content.

## Modes

### bootstrap — new master from scratch

Interview the user one section at a time, with concrete prompts and an example answer. Save the partial draft to `cv-master.md` after each section so progress is preserved. Sections (in order):

1. Contact, location, work authorization
2. Headline (role + years experience)
3. Summary (3–5 sentence pitch — Identity / Scale / Complexity layers, see [REFERENCE.md](REFERENCE.md#summary-three-layer-structure))
4. Skills (grouped by category — Languages, Frameworks, Databases, Cloud/DevOps, Tools. **No ratings**, see [REFERENCE.md](REFERENCE.md#skills-section))
5. Professional experience (per role: company, title, dates, location, 3–6 bullets, stack; for unknown employers add company context line)
6. Education
7. Side projects worth listing (only if [Projects threshold](REFERENCE.md#projects-when-to-include) met)
8. Languages, certifications, awards (optional)

Use the schema in [MASTER_TEMPLATE.md](MASTER_TEMPLATE.md). Apply XYZ method to every bullet at write-time. For missing metrics use `[DADO AUSENTE: qual era X?]`; for reasonable inferences use `[ESTIMADO]` (see [Data integrity](REFERENCE.md#data-integrity)).

After all sections collected, run a **lite audit** before final write: categories 2 (XYZ compliance), 3 (structure), 5 (voice) from the [ATS rubric](REFERENCE.md#ats-scoring-rubric). Skip categories 1 and 4 (no JD yet, length is uncapped on master). Report bullets needing a metric and any anti-pattern hits; ask before fixing.

### sync — import an existing resume (and optional standalone rewrite)

Accept any input format. Read with the `Read` tool — it handles `.md`, `.txt`, `.pdf`. For `.docx`, ask the user to paste the text or convert to PDF first.

**Two sub-flows:**

**(a) Merge into master** (default when `cv-master.md` exists, or user wants ongoing maintenance):

Map the source into the master schema. Where the source omits a field, insert `<!-- TODO: ask user -->` and ask the user to fill it after the initial import.

Run a section-by-section diff: show what is new, what is updated, what is removed. Wait for confirmation per section before merging.

Run the **lite audit** (categories 2, 3, 5) on the merged result before final write. Source resumes often carry weak verbs, AI-tell words, and em-dashes — surface them and offer rewrites.

**(b) Standalone rewrite** (user uploads a CV and wants a polished version without a JD, or asks "rewrite my CV"):

1. **Infer target profile** from the source: most likely role, seniority (Junior / Mid / Senior / Staff / Principal), specialization, target company type (early-stage startup / scale-up / big tech). Use this internally to prioritize emphasis. See [REFERENCE.md — Inferred target profile](REFERENCE.md#inferred-target-profile).
2. **Rewrite bullets** with the formula: strong action verb + specific technical context + measurable impact. Use the [three-tier metric system](REFERENCE.md#data-integrity): existing metric → use directly; estimable → mark `[ESTIMADO]`; missing → write qualitatively and append `[DADO AUSENTE: qual era X?]`. Never invent.
3. **Rewrite summary** per [three-layer structure](REFERENCE.md#summary-three-layer-structure) (Identity / Scale / Complexity). Banned vague buzzwords list applies.
4. **Consolidate Skills** into single grouped section (Languages · Frameworks · Databases · Cloud/DevOps · Tools). Drop ratings entirely. Drop tech that appears nowhere in experience.
5. **Group small side projects under company experience** instead of separate section, unless [Projects threshold](REFERENCE.md#projects-when-to-include) met.
6. **Add context lines** for non-globally-known employers (see [REFERENCE.md — Company context](REFERENCE.md#company-context)).
7. **Group same-company promotions** under one header; flag acquisitions explicitly (see [REFERENCE.md — Career progression](REFERENCE.md#career-progression)).
8. **Strict length:** 1 page for <5 years experience; max 2 pages for 5+ years. Section order: Summary → Experience → Technical Skills → Education → Projects (if applicable).
9. **Strip `Stack:` lines per role** from output. Tech context belongs inline in bullets or in the consolidated Technical Skills section.
10. **Achievement re-pass on every bullet.** Re-read each asking *"what changed because this was built?"* If only "the feature exists", rewrite to name an outcome ([REFERENCE.md — Achievements over tasks](REFERENCE.md#achievements-over-tasks)) or tag `[DADO AUSENTE: ...]`.
11. **Prune obsolete / low-relevance tech** from Skills given the inferred profile. Log removed items in post-CV §B.
12. Run full **ATS audit**. Render score. Below 80 → list failures, propose fixes, ask before write.
13. **Write the rewritten CV** to `<dir>/cv-rewrite-{YYYYMMDD}.md` (do not overwrite master). Then append the [Post-CV section in Brazilian Portuguese](REFERENCE.md#post-cv-section-pt-br).
14. Offer DOCX export (see [DOCX export](#docx-export)).

### check — fit assessment before committing to an application

Answers "is this worth applying to, and what will they push on?" Produces **no CV file**. The only thing written is the [gap ledger](#gap-ledger). Output is a conversational assessment in the chat.

Runs before `tailor` most of the time. When the user then asks to tailor, reuse this analysis rather than redoing it.

Steps:

1. **Check eligibility first, before anything else.** Location, work authorization, employment structure (EOR, W2, contractor), timezone-overlap requirements. If the role is structurally closed to the user, say so in the first line and stop the deep analysis. Nothing else matters if they cannot be hired.
2. **Search the CV directory for prior artifacts for this company** before assessing: `cv-{company}-*`, `screen-prep-{company}-*`, `application-*{company}*`, `cover-*{company}*`, and any take-home or design doc naming them. A prior application changes the entire conversation and missing one is a serious error. If found, read it, say when it was sent, and ask what the outcome was.
3. **Extract JD signals** per [REFERENCE.md — JD signal extraction](REFERENCE.md#jd-signal-extraction).
4. **Identify the gate.** Every role has one thing that decides it. It is either:
   - **Stated** — an explicit disqualifier ("walk us through an agentic system you shipped; if you can't, this isn't the role"). Check it directly and say plainly whether the user clears it.
   - **Unstated** — implied by scale claims, customer names, or funding language ("millions of requests", "$35M ARR"). These are more dangerous precisely because they do not read as requirements until the interview.
   Name which kind it is. This distinction is usually the single most useful thing in the assessment.
5. **Weigh the company's own hiring process**, when the JD describes it. A process that scores an asynchronous design exercise discounts missing operating history; a process built on resume screening does not. The same gap costs different amounts at different companies, and that changes the recommendation.
6. **Map requirements to evidence** in three buckets: strong (with the specific artifact), partial (and what is actually missing), gap (zero). Pull from the master *and* the portfolio archive if one exists — strong material is often sitting outside the master.
7. **Give a verdict with a number** (x/10) and a one-line reason. Do not hedge into uselessness.
8. **Separate closeable gaps from unwinnable ones.** For closeable, name the specific move and an estimate in hours. For unwinnable by a side project (production volume at scale, GPU fleets, formal oncall), say so plainly rather than prescribing a grind.
9. **Compare against other live roles** when the user is running several, and say where the preparation hours pay off best.
10. **Name the honest answer** for each weak point, in the words the user should actually say. The deliverable is not just "you have a gap", it is what to say when asked about it.
11. **Update the [gap ledger](#gap-ledger).**
12. Offer `tailor` and `screen-prep` as next steps. Do not run them unprompted.

Flag red flags from the JD too (unpaid take-homes, vague comp, unrealistic stack breadth, pace language implying unacknowledged on-call). Surface comp guidance without inventing numbers: if no band is posted, say so and advise making them name it first.

### tailor — CV matched to a job description

Required inputs (ask if missing): job description (text, URL, or file), company name, role title.

If `check` already ran on this JD, reuse its analysis. Do not re-derive the gate, the requirement mapping, or the gaps.

Steps:
1. Extract from JD: required skills, preferred skills, responsibilities, seniority, domain, company keywords. Build the keyword set `K` for scoring.
2. From `cv-master.md`, **select and rephrase** matching experiences and bullets — never invent. Rewrite each kept bullet with strong action verb + specific technical context + measurable impact (XYZ method — see [REFERENCE.md](REFERENCE.md#bullet-rules--xyz-method)). Apply the [three-tier metric system](REFERENCE.md#data-integrity) — flag `[ESTIMADO]` or `[DADO AUSENTE: ...]` when needed.
3. **Consolidate Skills** into single section grouped by category (Languages · Frameworks · Databases · Cloud/DevOps · Tools). Lead each category with JD-relevant items the user actually has. **No ratings.** Match JD vocabulary verbatim where the user has the underlying skill.
4. Rewrite the summary per [three-layer structure](REFERENCE.md#summary-three-layer-structure) (Identity / Scale / Complexity), 3–5 lines, aligned to the role. Apply [voice rules](REFERENCE.md#voice-rules) — banned-buzzword list, no em-dashes, no AI-tell words.
5. **Strict length:** 1 page for <5 years experience; max 2 pages for 5+ years. Drop weakest bullets first when trimming.
6. **Add context lines** for non-globally-known employers. **Group promotions** under one header. Flag acquisitions explicitly. See [Company context](REFERENCE.md#company-context) and [Career progression](REFERENCE.md#career-progression).
7. **Group small side projects under company experience** instead of separate section, unless [Projects threshold](REFERENCE.md#projects-when-to-include) met.
8. **Strip `Stack:` lines per role from output.** Tech context belongs inline in the bullet or in the consolidated Technical Skills section, not duplicated under every role. Master keeps Stack lines; tailored output does not.
9. **Achievement re-pass on every bullet.** Re-read each kept bullet asking *"what changed because this was built?"* If the answer is only "the feature exists", rewrite to name an outcome (see [REFERENCE.md — Achievements over tasks](REFERENCE.md#achievements-over-tasks)) or tag `[DADO AUSENTE: ...]`.
10. **Prune obsolete / low-relevance tech** from Skills given the inferred profile. Log removed items in the post-CV §B change log so the candidate can restore.
11. **Score the draft against the [ATS rubric](REFERENCE.md#ats-scoring-rubric).** Render the full score block (5 categories, breakdown, failing items). Auto-apply fixes for em-dashes, AI-tell words, and bullet rewrites; surface gap-skills and missing-metric bullets to the user.
12. **Hard gate:** if score < 80, do not write. Show the failing items, propose fixes, ask the user to approve fixes or override the gate.
13. After score ≥ 80 (or override): show the user JD requirements → covered master entries; remaining gaps. Wait for confirmation. Write to the tailored output path. Append the [Post-CV section in Brazilian Portuguese](REFERENCE.md#post-cv-section-pt-br).
14. **Update the [gap ledger](#gap-ledger)** with every requirement the master could not support, including the ones deliberately left off the CV. Same turn, not a follow-up offer.
15. Offer DOCX export (see [DOCX export](#docx-export)).

ATS-safe formatting rules in [REFERENCE.md](REFERENCE.md).

### screen-prep — recruiter-call Q&A pack

Required inputs: JD, company name, role title.

Output sections:
- **30-second intro pitch** — first-person, aligned to the role.
- **Why this company / role** — 3 sentences from JD signals; ask the user for any personal angle.
- **Top 8 likely first-call questions** with draft answers in the user's voice, each ≤ 120 words.
- **Salary expectation** — ask the user for their range; never guess.
- **Gaps and risks** — JD requirements the master does not cover, with honest framings.
- **Questions to ask the recruiter** — 4 thoughtful, non-generic.

Always confirm before writing. Recruiter prep is high-stakes — never invent experience.

After writing, update the [gap ledger](#gap-ledger) with anything from the "Gaps and risks" section.

## Gap ledger

`<dir>/gap-ledger.md` is a running, cross-JD record of requirements the master cannot support. It exists because a gap named once is noise and a gap named in four job descriptions is quietly deciding outcomes — and that pattern is invisible if gaps only ever live in the post-CV section of individual tailored CVs.

**When to update it:** any time a JD is assessed. That includes `tailor`, `screen-prep`, and a bare fit check (user pastes a JD and asks "check this" without naming a mode). Update it as part of the same turn, not as a follow-up offer.

**How to update:**

- Gap already in the ledger → append the company to its **Seen in** line and re-rank if its count changed. Do not duplicate the entry.
- New gap → add an entry in the format below.
- Gap that has closed (user shipped the thing) → move it to the `## Closed` section with the date and what closed it. Never delete.
- Bump `Last updated` to today's date.

**Organize by gap, never by company.** Recurrence is the whole point of the file.

**Entry format:**

```markdown
### N. {Gap name}
**Seen in:** {Company A, Company B, ...}
**They ask for:** {the requirement in their words}
**You have:** {the honest current state, including the closest analogue}
**Closing move:** {the specific, concrete thing that would close it}
**Estimate:** {N to M hours}
```

**Rules:**

- **Estimates in hours, never days.**
- **Never soften the "You have" line.** The ledger is the one document where the gap is stated plainly; tailored CVs handle presentation, this handles truth.
- **Mark gaps that are not closeable by a side project** as such (production volume at scale, GPU fleets, formal oncall). Telling the user to grind at something unwinnable is worse than naming it honestly.
- Maintain a short **"projects that close the most"** section. Prefer one project that closes four gaps over four projects that close one each, and say which single project has the best ratio.
- Single-occurrence gaps can live in a compact table rather than full entries, and get promoted to a full entry on their second sighting.

## DOCX export

After writing `cv-master.md` (`sync` / `bootstrap`), any tailored CV (`tailor`), or any standalone rewrite (`sync` (b)), offer to generate a paired `.docx` next to the `.md`. DOCX is the preferred output for international tech-market submissions — easier to edit, no font breakage. Skip for `screen-prep` (internal prep doc).

**Critical:** the rendered output (DOCX or PDF) must contain **only the CV body in English with no review markers**. Three things get stripped before rendering:

1. **Post-CV PT-BR section** — everything from the first `---` separator onward (review notes for the candidate).
2. **`[DADO AUSENTE: ...]` markers** — entire bracketed phrase, including any preceding space and the period before it if it terminates the sentence.
3. **`[ESTIMADO]` markers** — entire bracketed phrase, including any preceding space.

Markers live in the `.md` source as review notes; they never appear in the submitted document.

Steps:

1. Check pandoc is available: `pandoc --version`. If missing, instruct the user to install (`winget install --id JohnMacFarlane.Pandoc` on Windows, `brew install pandoc` on macOS, `apt install pandoc` on Linux) and stop.
2. Strip the post-CV PT-BR section AND all review markers into a temp file, then render. Run from `<dir>`:
   ```bash
   awk '/^---$/{exit} {print}' <file>.md | sed -E 's/ *\[DADO AUSENTE:[^]]*\]//g; s/ *\[ESTIMADO\]//g' > <file>.cv-only.md
   pandoc <file>.cv-only.md -o <file>.docx --reference-doc=cv-reference.docx
   rm <file>.cv-only.md
   ```
   The `--reference-doc` is optional. If `<dir>/cv-reference.docx` does not exist, drop the flag — pandoc uses its sensible defaults (single column, Calibri, ATS-safe).
3. Suggested filename for final submission: `FirstName_LastName_Resume.docx`.
4. Output is `<file>.docx` next to the source `.md`.
5. Report the DOCX path in one sentence. Do not open it automatically.

**PDF (secondary):** If the user explicitly asks for PDF instead of DOCX, run the same strip-then-render pattern:
```bash
awk '/^---$/{exit} {print}' <file>.md | sed -E 's/ *\[DADO AUSENTE:[^]]*\]//g; s/ *\[ESTIMADO\]//g' > <file>.cv-only.md
npx --yes md-to-pdf <file>.cv-only.md --stylesheet cv-style.css --launch-options '{"args":["--no-sandbox"]}'
mv <file>.cv-only.pdf <file>.pdf
rm <file>.cv-only.md
```
Then **verify the PDF actually extracts as text**, every time. A CV can look perfect and still parse as gibberish, and the failure is invisible on screen:

```bash
py -3 "<skill-dir>/verify-pdf.py" <file>.pdf
```

where `<skill-dir>` is this skill's own directory, reported as its base directory when the skill loads (`~/.claude/skills/cv-craft` on a Claude install, `~/.agents/skills/cv-craft` under pi). Do not hardcode either path.

It prints `SEND IT` or `FIX BEFORE SENDING` and exits non-zero on a problem, naming the exact words an ATS would fail to match. Use `python3` instead of `py -3` off Windows; if `pypdf` is missing, `pip install pypdf`. Do **not** hand-check with `pdftotext` — it silently normalises ligatures and reports a broken file as clean.

What each failure means:

| Check | Failure means |
|-------|---------------|
| ligature glyphs | `cv-style.css` is missing the `font-variant-ligatures: none` rule. `Cloudflare` will not match an ATS keyword search. |
| leaked markers | The strip step did not run or the `---` separator is missing. The PDF contains PT-BR review notes. Do not send it. |
| glued words | Font embedding dropped spaces. Re-render, and if it persists switch the `font-family` to a plain `Arial, sans-serif`. |

DOCX is not affected by the ligature problem: it stores literal characters, so extraction is exact. That is one more reason to default to it.

PDF is discouraged as primary because formatting often breaks and editing later is painful. Default to DOCX.

The user can re-render after manual edits with the same command.

## Confirmation discipline

Show a diff or preview before every write. Wait for explicit user confirmation. After writing, report what changed in one sentence — do not re-print the full file.

## Reference

- [MASTER_TEMPLATE.md](MASTER_TEMPLATE.md) — master CV schema and field rules
- [REFERENCE.md](REFERENCE.md) — ATS rules, bullet conventions, market best practices
- [EXAMPLES.md](EXAMPLES.md) — sample tailored CV and sample screen-prep pack
- [verify-pdf.py](verify-pdf.py) — post-render check that a PDF extracts as text (ligatures, leaked review markers, glued words)

## Humanize the written prose (if available)

Before writing generated prose to a file, if the `humanizer` skill is installed, run it on the drafted text so the created document reads naturally and free of AI tells; skip silently if it is not available. Apply it to the human-facing document body only, never to code, frontmatter, file paths, IDs, or literal templates.
