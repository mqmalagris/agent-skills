---
name: cv-craft
description: Maintain a canonical master CV in Markdown and produce tailored, ATS-friendly resumes and recruiter-screen prep packs from job descriptions. Supports four modes — bootstrap (build master from scratch via interview), sync (import existing resume in any format into master, with optional standalone rewrite output), tailor (generate CV matched to a JD), and screen-prep (draft answers for first recruiter-call questions). Use when the user asks to update their CV/resume, rewrite an existing CV, tailor a resume to a job posting, prepare for a recruiter screen, import a resume PDF/docx into Markdown, or runs /cv-craft.
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

1. Detect mode from the user's request: `bootstrap` | `sync` | `tailor` | `screen-prep`. Ask if ambiguous.
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

### tailor — CV matched to a job description

Required inputs (ask if missing): job description (text, URL, or file), company name, role title.

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
14. Offer DOCX export (see [DOCX export](#docx-export)).

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
PDF is discouraged as primary because formatting often breaks and editing later is painful. Default to DOCX.

The user can re-render after manual edits with the same command.

## Confirmation discipline

Show a diff or preview before every write. Wait for explicit user confirmation. After writing, report what changed in one sentence — do not re-print the full file.

## Reference

- [MASTER_TEMPLATE.md](MASTER_TEMPLATE.md) — master CV schema and field rules
- [REFERENCE.md](REFERENCE.md) — ATS rules, bullet conventions, market best practices
- [EXAMPLES.md](EXAMPLES.md) — sample tailored CV and sample screen-prep pack

## Humanize the written prose (if available)

Before writing generated prose to a file, if the `humanizer` skill is installed, run it on the drafted text so the created document reads naturally and free of AI tells; skip silently if it is not available. Apply it to the human-facing document body only, never to code, frontmatter, file paths, IDs, or literal templates.
