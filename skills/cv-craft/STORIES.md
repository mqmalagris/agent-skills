# cv-craft: career evidence and interview stories

The method behind `evidence` mode. It came from a post-rejection audit (November 2026) where the interviewer's feedback was: personal ownership unclear, no concrete "the agent was wrong and I caught it" case, answers long and indirect. None of those were missing experience. They were claims broader than the evidence, numbers stated more firmly than they were measured, and stories that started with the system instead of the candidate. This file is how to prevent all three before an interview does it for you.

Read it before `evidence` mode, and whenever `tailor` or `screen-prep` finds a `career-evidence/` folder.

## Contents

- [Ground rules](#ground-rules)
- [Folder layout](#folder-layout)
- [Step 1: identity and sources](#step-1-identity-and-sources)
- [Step 2: evidence catalog](#step-2-evidence-catalog)
- [Step 3: ownership audit](#step-3-ownership-audit)
- [Step 4: metric provenance](#step-4-metric-provenance)
- [Step 5: status as of a date](#step-5-status-as-of-a-date)
- [Step 6: story bank](#step-6-story-bank)
- [Step 7: question map and answer framework](#step-7-question-map-and-answer-framework)
- [Step 8: CV audit and correction propagation](#step-8-cv-audit-and-correction-propagation)
- [Step 9: open questions](#step-9-open-questions)
- [Keeping it current](#keeping-it-current)

## Ground rules

1. **Read-only on every source.** Never commit, push, comment, or edit a repo, ticket or PR while gathering evidence. The only writes are inside `<dir>/career-evidence/`.
2. **Never invent** metrics, personal contributions, customer outcomes, AI mistakes, or decisions. A gap stays a gap and goes to `open-questions.md`.
3. **Confidential material stays out.** No secrets, tokens, credentials, customer personal data, or private implementation details in interview material. Anonymize ("a direct-selling coffee brand", "the client's compliance team"). If a credential turns up in a source, say so to the user separately and keep it out of every file.
4. **The CV is never edited by this mode.** Proposed CV changes go in `cv-audit.md` and a diff file; the user applies them or asks you to.

## Folder layout

`<dir>/career-evidence/`, created on first run:

| File | Holds |
|---|---|
| `README.md` | Index, last-updated date, and the "what each live process has seen" table |
| `evidence-catalog.md` | One entry per piece of work (E-01, E-02...), every claim labeled VF / RI / UR with a reference |
| `ownership-audit.md` | Per project: existed before you, decided by others, yours, caught by others; the defensible ownership sentence |
| `interview-story-bank.md` | Story cards (S1, S2...) in the A to H format, plus a competency coverage table |
| `interview-question-map.md` | The answer framework, question to story map, honest-boundary lines, follow-up drills |
| `agent-verification-cases.md` | Only for AI-native targets: every "agent was wrong" candidate, graded |
| `cv-audit.md` | Each CV claim: OK / Tighten / Fix, with claim, evidence and replacement |
| `open-questions.md` | What only the user can answer, with an Answered table |
| `readiness-assessment.md` | Per competency area: strongest evidence, weakest point, what to do, in hours |
| `<topic>-corrections.md` | One per corrected claim that has spread across files (see Step 8) |

Smaller targets can skip files; the catalog, ownership audit, story bank and question map are the core.

## Step 1: identity and sources

**Identity first.** Collect the user's verified git identities (author names and emails from `git config`, past commits the user confirms, GitHub login). Attribute a commit only when the author email or login matches. A shared first name, a co-author trailer, or "the PR was merged by him" is not authorship. List the identities at the top of the catalog.

**Sources, strongest first:**

| Source | Proves | Watch for |
|---|---|---|
| Commits, diffs, PR bodies, review threads | What changed, who authored, who merged, who caught what | Authored ≠ merged ≠ reviewed. Squash merges can hide authors. |
| ADRs, PRDs, plans in the repo | What was decided and the alternatives | The author of the doc may not be the decider |
| PM tool threads (tickets, discussions) | Who asked, who decided, what the client said | Often only in cached tool results or exports; search those too |
| Production data (ledgers, DB tables, logs, metrics dashboards) | Real numbers | Environment (prod vs staging vs dev), time window, sample size |
| Coding-agent transcripts | What the agent proposed and what the user rejected | Proves the user's judgment, not the code's origin |
| Brag doc | What the user thought mattered at the time | A recollection, not proof, unless it cites a source |
| The user's memory | Context nobody wrote down | Label UR until confirmed |

**Claim labels**, used on every line of the catalog:

- **VF (verified fact):** read directly in a commit, diff, PR, thread, doc, or query result, with the reference.
- **RI (reasonable interpretation):** follows from the evidence but isn't stated in it.
- **UR (unverified recollection):** from the CV, brag doc or memory only. Needs the user's confirmation before it's said in an interview.

## Step 2: evidence catalog

One entry per piece of work worth talking about, not per commit. Each entry:

```markdown
## E-NN. {What happened, in plain words}
**Where:** {project, repo, dates}
**Trigger:** {who noticed what, and how}  (VF/RI/UR + ref)
**What the user did:** {verbs they can defend}  (VF + commits/PRs)
**What others did:** {decided, built, reviewed, caught}  (VF + ref)
**Outcome:** {measured, or "not measured"}  (VF + source, or UR)
**Status as of {date}:** {production / staging / PR open / ...}
**Story potential:** {which competency it proves}
```

Look past the obvious. Some of the strongest material in the audit came from places nobody had listed: a PM thread where the user tested the lead's plan with a real order before estimating it (a disagreement story), a discovery spike scored against a golden set (an end-to-end product story), the user's own early design they later replaced (a "decision I'd make differently" story), a bug that shipped through every test and was caught by the user, not a bot.

## Step 3: ownership audit

The question every senior interview asks is "what was yours?" Answer it per project with four columns:

| Existed before you | Decided by others | Yours | Reviewed or caught by others |
|---|---|---|---|

Then write **one ownership sentence** per project that survives a follow-up on any line. Measure it against git:

- Compare the user's commit counts with the top contributors per repo and per key file. If someone else leads, "I own X end to end" is false even if the user worked on everything. "One of two lead engineers" or "largest contributor (1,928 of 3,021 commits)" is true and stronger, because it can't be knocked down.
- List the domains the user does own end to end by name. A specific list beats a broad claim.
- Name what was already there ("the flag system existed; I gated the feature behind it"). Using existing infrastructure well is a fine story; implying you built it is a trap.
- Small contributions to a client project are "contributions to", never "shipped the integration".

**Ownership verb ladder**, strongest to weakest, each needing the matching evidence:

| Verb | Requires |
|---|---|
| Designed / decided | An ADR, design doc or thread where the user made the call |
| Built / rebuilt | Authored most of the commits for it |
| Led | Coordinated others' work on it, visible in tickets or PRs |
| Owned | Ongoing responsibility, not one PR |
| Found / traced / caught | The user's own report, commit or comment came first |
| Contributed to | Some authored commits |
| Reviewed / merged | Only that |

Product decisions usually belong to a PM or the client. Say so, then say what the user owned inside the decision.

## Step 4: metric provenance

Every number gets a provenance line before it goes on any CV or into any answer:

> {number} = {unit} measured by {source} over {sample} in {environment}, {window}, {date}. User's share: {what part was theirs}.

Rules:

- **A smoke test is not a result.** One query, one run, or "it looked about 5x cheaper" is a hypothesis. Before a ratio goes on a CV, re-derive it from the system of record (a billing ledger, a cost table, logs) on a matched sample, and report the unit the claim names. In the audit, "5x fewer credits per request" from an early single-query test became 2.5x on a 48-request before/after from the credit ledger. Model cost was 2.8x; input tokens 1.6x. The CV says 2.5x because the claim is about credits.
- **Report adjacent ratios.** When one number moves, say what the neighbors did, so the strongest one isn't cherry-picked.
- **Name the environment.** A dev or staging measurement is still a measurement, but say "in testing" or "before/after test", never imply production traffic.
- **Two different numbers with the same shape need separate defenses** ("5x startup CPU" measured with a profiler is fine even after "5x credits" was corrected). Check which claim a line is before editing it.
- **Tech claims are numbers too.** "Runs on OpenAI and Anthropic" must match the imports in the current code, not an earlier version.
- **Write the query down.** Save the SQL or command next to the result (`<metric>-query.sql`) so the number can be re-checked before each interview.

## Step 5: status as of a date

Use exactly one of these per item, with the date checked:

`in production since {date}` · `on staging` · `merged to dev, not released` · `PR open, review requested` · `behind a flag, off for live users` · `in beta with {N} users at {M} customers (as of {month})` · `in progress, decision with {who}` · `not shipped`

Never round staging up to "shipped". Re-check anything that can change (open PRs, release status, a pending client decision) before each interview, and keep a "re-check before each interview" list in `open-questions.md`.

## Step 6: story bank

Pick 12 to 20 stories from the catalog for evidence strength and competency coverage. Each card:

```markdown
## SN. {Short title}

**A. Headline:** one sentence that answers "what happened and what did you do".
**B. 20 seconds:** the spoken version for a recruiter call.
**C. 60 to 90 seconds:** the interview version, in the user's spoken English.
**D. Deep dive:** what to say only if they dig.
**E. Follow-ups:** 3 to 5 likely questions, each with a short answer.
**F. Ownership:** what was the user's, what was others'. Names roles, not people, if the doc might be shared.
**G. Evidence:** commit, PR, thread, query, E-NN.
**H. Status:** as of {date}; what's still unconfirmed.
```

**Rules for every card:**

1. The first sentence answers the question. The second says what the user did, with a verb from the ladder.
2. Context in one sentence, never three.
3. Say the check out loud ("I re-ran the 318 questions", "I placed a real order"), even if not asked. It's what separates engineers who verify from those who don't.
4. Stop after the result. Let them pull the deep dive.
5. Include the user's own mistake when the story has one ("I'd said tax was per cart; it's per item, and I corrected it before the call"). It makes the rest believable.
6. An in-progress story stays in progress. Don't invent a resolution.

**Story types the bank must cover**, because interviewers ask for them by name:

| Type | What makes it strong |
|---|---|
| The agent was wrong and I caught it | AI origin provable (trailer, transcript), the user caught it (not a bot or QA), tests passed |
| A disagreement | With a person, settled with evidence (a test, a measurement), not seniority |
| A mistake of my own | The user's code, the user's catch, what changed after |
| A decision I'd make differently | Preferably replacing the user's own earlier design |
| Pushback on a requirement | A cheaper or safer alternative the stakeholder accepted |
| A feature from discovery to rollout | Evidence before the build (prototype, eval, test), a gated rollout |
| A production incident | Diagnosis steps, the fix, the guard that stops a repeat |
| Cost or performance | A measured before/after with provenance |

Keep a **coverage table** at the top of the story bank (competency to story IDs) and update it whenever a card is added. A competency with no story is an item for `readiness-assessment.md`.

**Grading "agent was wrong" cases** (`agent-verification-cases.md`): for each candidate, answer separately (1) is the AI origin proven, and how; (2) who caught it, the user or a bot/QA; (3) did tests miss it. If the user strips AI trailers from commits, no defect in their own code can be proven agent-written from git. Say so plainly, and lean on cases with a trailer or a transcript.

## Step 7: question map and answer framework

**The framework: answer, me, context, decision, check, result.**

1. **Answer** the exact question in one sentence. If they ask "what was your role", the first word is about you.
2. **Me:** what the user did, with a verb they can defend.
3. **Context:** one sentence, the minimum for step 4 to make sense.
4. **Decision:** the choice, and the alternative not taken.
5. **Check:** how they knew it worked.
6. **Result or lesson,** then stop. 60 to 90 seconds.

Include one before/after rewrite of a real answer that went wrong, if the user has one; it teaches faster than the rules.

Then:

- **Question map:** a table of common questions (agent wrong, incident, disagreement, mistake, ownership, trade-off, ambiguous requirement, end to end, cost, observability, async communication, security) to a lead story and a backup.
- **Honest-boundary lines:** short sentences for the true limits ("that system was already there", "the AI reviewer caught that, not me", "that was dev, not production", "that's still waiting on review"). Use them when they're true, not as a default; overused, they sound like the user did nothing.
- **Follow-up drills:** the likely second question on the weakest claims, with the answer that stays inside the story.
- **Correction lines:** for any number that was sent in an earlier, wrong form, the exact sentence to say (Step 8).

## Step 8: CV audit and correction propagation

**Audit every claim** in the master and in each CV a live process has seen:

```markdown
### F1. {short name}
- **Claim ({file}:{line}):** "..."
- **Evidence:** {ref}. {what it shows}
- **Replace:** "..."
```

Verdicts: **Fix** (contradicted by evidence), **Tighten** (true, but a follow-up exposes a gap), **OK** (verified). Also list **overlooked accomplishments** the catalog found that no CV mentions; under-claiming is a finding too.

**When a claim is corrected, it has usually spread.** Search the whole CV directory for every form of it (the number, the percent form, the pt-BR form, the spoken form) and sort the hits:

| Priority | Files | Action |
|---|---|---|
| 1 | Master, LinkedIn text, anything public or reused | Fix now |
| 2 | Live processes (applied, interviewing, offer) | Fix the source file for the next touchpoint; leave sent PDFs as the record of what went out |
| 3 | Archive (closed or never sent) | Leave; list in a table; fix only if reused |

Then write the **correction line** for processes that saw the old form, and add the process to the "what each live process has seen" table in `README.md`. Correcting your own number unprompted, before a final round, is a credibility point. Being caught on it is not.

Check each hit is the same claim before editing (two different "5x" claims can sit in one CV).

## Step 9: open questions

Questions only the user can answer go in `open-questions.md`. Ask them **one at a time**, each with the context the user needs to answer (the PR, the date, what the evidence shows so far) and a suggested answer when one is likely. Clarify before assuming; the user's first answer often refines the question. Record every answer in an **Answered** table with the date, then update the catalog, stories and CV audit in the same turn.

## Keeping it current

- When an application goes out, add a row to the README's "what each live process has seen" table: the numbers, ownership wording and stories in what they read. Interview answers must match it, or carry the correction line.
- When a status changes (a PR merges, a beta grows, a client decides), update the story card's H line and the catalog entry together.
- Monthly brag-doc entries are the intake. `brag-doc compile stories` produces story seeds in this card format; turn the good ones into cards.
- Re-run the metric queries before a final round.

### Short outreach is not a CV

A recruiter message or a 300-character connection note keeps the outcome and drops the method: "cut AI credits per request about 2.5x" reads well; "on the same 48 test requests" reads odd in a two-paragraph note. The method belongs in the CV bullet, the defense line, a written "hardest problem" answer, and the interview.
