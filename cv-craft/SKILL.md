---
name: cv-craft
description: Maintain a canonical master CV in Markdown and produce tailored, ATS-friendly resumes and recruiter-screen prep packs from job descriptions. Supports four modes — bootstrap (build master from scratch via interview), sync (import existing resume in any format into master), tailor (generate CV matched to a JD), and screen-prep (draft answers for first recruiter-call questions). Use when the user asks to update their CV/resume, tailor a resume to a job posting, prepare for a recruiter screen, import a resume PDF/docx into Markdown, or runs /cv-craft.
---

# cv-craft

Maintain a master CV in Markdown and produce tailored CVs + recruiter-screen prep packs from it. Path-agnostic: the user picks where files live, the skill remembers it.

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
3. Summary (3–4 sentence pitch)
4. Skills (proficient / intermediate / beginner)
5. Professional experience (per role: company, title, dates, location, 3–6 bullets, stack)
6. Side projects worth listing
7. Education
8. Languages, certifications, awards (optional)

Use the schema in [MASTER_TEMPLATE.md](MASTER_TEMPLATE.md). Apply XYZ method to every bullet at write-time and flag bullets missing a metric with `[no-metric]` so future syncs can fill them.

After all sections collected, run a **lite audit** before final write: categories 2 (XYZ compliance), 3 (structure), 5 (voice) from the [ATS rubric](REFERENCE.md#ats-scoring-rubric). Skip categories 1 and 4 (no JD yet, length is uncapped on master). Report bullets needing a metric and any anti-pattern hits; ask before fixing.

### sync — import an existing resume

Accept any input format. Read with the `Read` tool — it handles `.md`, `.txt`, `.pdf`. For `.docx`, ask the user to paste the text or convert to PDF first.

Map the source into the master schema. Where the source omits a field, insert `<!-- TODO: ask user -->` and ask the user to fill it after the initial import.

If `cv-master.md` already exists, run a section-by-section diff: show what is new, what is updated, what is removed. Wait for confirmation per section before merging.

Run the same **lite audit** as bootstrap (categories 2, 3, 5) on the merged result before final write. Source resumes often carry weak verbs, AI-tell words, and em-dashes — surface them and offer rewrites.

### tailor — CV matched to a job description

Required inputs (ask if missing): job description (text, URL, or file), company name, role title.

Steps:
1. Extract from JD: required skills, preferred skills, responsibilities, seniority, domain, company keywords. Build the keyword set `K` for scoring.
2. From `cv-master.md`, **select and rephrase** matching experiences and bullets — never invent. Rewrite each kept bullet to the **XYZ method** (`Accomplished [X], as measured by [Y], by doing [Z]` — see [REFERENCE.md](REFERENCE.md#bullet-rules--xyz-method)).
3. Reorder the skills section to lead with JD-relevant items the user actually has. Match JD vocabulary verbatim where the user has the underlying skill.
4. Rewrite the summary as a 3-line pitch aligned to the role. Apply [voice rules](REFERENCE.md#voice-rules) — no em-dashes, no AI-tell words.
5. Length: 1 page for ≤8 years experience, 2 pages max otherwise. Drop weakest bullets first when trimming.
6. **Score the draft against the [ATS rubric](REFERENCE.md#ats-scoring-rubric).** Render the full score block (5 categories, breakdown, failing items). Auto-apply fixes for em-dashes, AI-tell words, and bullet rewrites; surface gap-skills and missing-metric bullets to the user.
7. **Hard gate:** if score < 80, do not write. Show the failing items, propose fixes, ask the user to approve fixes or override the gate.
8. After score ≥ 80 (or override): show the user JD requirements → covered master entries; remaining gaps. Wait for confirmation. Then write to the tailored output path.

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

## PDF export

After writing `cv-master.md` (in `sync` or `bootstrap`) or any tailored CV (in `tailor`), generate a paired `.pdf` next to the `.md`. Skip for `screen-prep` (internal prep doc).

Steps:

1. Verify `<dir>/cv-style.css` exists in the resolved CV directory. If missing, create it with the ATS-safe defaults from [REFERENCE.md](REFERENCE.md) (Inter/Calibri, 10.5pt body, single column, no graphics).
2. Run from `<dir>`:
   ```bash
   npx --yes md-to-pdf <file>.md --stylesheet cv-style.css --launch-options '{"args":["--no-sandbox"]}'
   ```
3. First run downloads Chromium (~170MB). Inform the user.
4. Output is `<file>.pdf` next to the source `.md`.
5. After generation, report the PDF path in one sentence. Do not open it automatically.

The user can re-render after manual edits with the same command.

## Confirmation discipline

Show a diff or preview before every write. Wait for explicit user confirmation. After writing, report what changed in one sentence — do not re-print the full file.

## Reference

- [MASTER_TEMPLATE.md](MASTER_TEMPLATE.md) — master CV schema and field rules
- [REFERENCE.md](REFERENCE.md) — ATS rules, bullet conventions, market best practices
- [EXAMPLES.md](EXAMPLES.md) — sample tailored CV and sample screen-prep pack
