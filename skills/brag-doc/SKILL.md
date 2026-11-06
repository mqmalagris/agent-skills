---
name: brag-doc
description: >-
  Maintain a monthly brag document (accomplishment log) and roll it up into a promo packet, self-review, CV material or interview story seeds. Blends Lucas Faria's 4-field monthly template with Julia Evans' impact-first categories, and records ownership, status, evidence and story seeds as it goes. Use when the user wants to log what they shipped, prep for a performance or promotion cycle, write a self-review, remember work from months ago, collect interview stories, feed achievements to cv-craft, or runs /brag-doc. Modes: draft, example, review, compile. Targets: work (employment, any employer), side (public / side-project work).
---

# Brag Doc

Two living docs the user maintains:
- `projects/side/brag/<employer>.md` — employment, one file per employer (e.g. `acme.md`). For perf/promo cycles; shared with the manager.
- `projects/side/brag/side-projects.md` — public work (OSS, content, shipped apps). Feeds the 2026 job search and cv-craft.

Invocation: `/brag-doc <mode> [target]`. `target` is `work` or `side` — ask if the mode needs one and it's unclear. For `work`, resolve to the employer file in `projects/side/brag/`; ask which if more than one exists. (Personal skills take space-separated args, so `/brag-doc draft work`, not `:draft`.)

## Why the extra fields

A brag doc written only as "shipped + impact" is enough for a perf review and not enough for an interview. A 2026 post-rejection audit had to dig through git, PR threads, a PM tool and a billing ledger to answer three questions the monthly entries never recorded: what exactly was mine, is it live or on staging, and how was that number measured. Each answer was cheap at the time and expensive months later. The fields below capture them while the evidence is still fresh. The full interview method lives in cv-craft's `STORIES.md`.

## Modes

### draft
Add this month's entry to the target doc. **Pull real signal first — never invent accomplishments.**
1. Gather evidence: `git log --author=<user> --since="1 month ago"`, recent PRs/tickets, this conversation, and for `side` the career plan at `projects/side/career-plan-90d.md`.
   **Attribute by verified identity only.** Use the user's author emails and GitHub login, not a name match. Note who merged and who reviewed: authored, merged and reviewed are three different claims.
   **Also read `~/.claude/state/periscope/contributions.log.md` when it exists.** One line per approved contribution: `- <date> | <lens> | <link> | <what changed> | mandate: <behavior>`. These are *influence* entries — weighing in on someone else's PR, unblocking a stalled decision, proposing a convention across teams. **They have no commit behind them by design**, so `git log` cannot see them. Do not try to reconcile them against git history: nothing will match, and dropping them removes the highest-leverage work in the month. The approval gate that wrote each line already vetted it, so take it at face value and convert it to impact like any other item.
   **Look for story material, not just output:** PM or review threads where the user pushed back, tested an assumption, or changed a plan; agent proposals the user rejected; bugs the user caught that tests or AI reviewers missed; the user's own mistakes and their fixes.
2. Fill the monthly template (see [TEMPLATE.md](TEMPLATE.md)) — the four Faria fields plus **Caught** and **Story seeds**.
3. **Impact rule (Julia):** state it *exactly as good as it is* — no inflation, no hedging. Every "shipped" line names an outcome (who uses it, metric, $, time saved), not a task. For fuzzy work: goal → actions taken → observable effect. Mark any unverified number `[ESTIMADO]`.
4. **Every shipped line carries three tags** (format in TEMPLATE.md):
   - **Ownership:** `mine`, `led`, `with <role or name>`, or `contributed`. If a teammate wrote most of it, say so here; "we" in the prose is fine, the tag is not.
   - **Status as of today:** `prod <date>`, `staging`, `dev`, `PR open`, `flagged off`, `beta <N users>`. Never round staging up to shipped.
   - **Refs:** PR numbers, ticket IDs, ADR, the query behind a number.
5. **Every number gets its method** in the same line or a footnote: source, sample, environment ("8.9 to 3.5 credits per request, ledger, 48 requests each loop, dev"). A ratio from one quick test is marked `[smoke test]` and never copied into a CV until re-measured.
6. Prepend the entry under a `## <Month Year>` header. Never overwrite past months. When a later month changes an earlier item's status (staging → production), say so in the new month; don't edit the old line.

### example
Show a filled monthly entry so the user sees the shape and bar. Read [EXAMPLE.md](EXAMPLE.md), display it, then offer to turn it into a real draft for their chosen target.

### review
Sharpen an existing entry the user points at. Line by line:
- task or impact? vague or specific? number or hand-wave? inflated or honest?
- **ownership:** does the tag match git (authored commits vs teammates')? Is anything implied as built that already existed?
- **status:** still true today? Re-check open PRs and releases.
- **provenance:** does each number say how it was measured? Is a smoke test posing as a result?
- **who caught it:** does a "found" line credit the user for something a bot, reviewer or QA found?
- **story seeds:** is there a decision, disagreement, mistake or catch in this month that has no seed?

Rewrite task→impact, flag unsupported claims, cut anything that oversells. Report the diffs and reasons — don't silently edit.

### compile
Roll N monthly entries into one output. Ask which and the date range, then produce:
- `promo` → promo packet / self-review organized by Julia's full categories (projects & impact, collaboration & mentorship, design & docs, company building, what I learned, outside of work). Pull the `periscope` contribution log for this range too. Influence entries land mostly under **collaboration & mentorship** and **company building** — the two categories a packet built only from commits leaves conspicuously empty, which is the gap that sinks a promo case.
- `cv` → hand the impact bullets to **cv-craft** as achievement source material, each with its ownership tag, status and provenance so cv-craft doesn't have to re-derive them.
- `stories` → collect every story seed in the range and expand the strongest into story cards in cv-craft's format (headline, 20-second and 60-to-90-second versions, follow-ups, ownership, evidence, status). Write to `<cv dir>/career-evidence/story-seeds-<range>.md`, never straight into the story bank; the user picks which become cards. Group by the story types interviewers ask for: agent was wrong and I caught it, disagreement, own mistake, decision I'd change, pushback on a requirement, discovery to rollout, incident, cost or performance. Say which types have no seed in the range.

## Story seeds and the shared doc

The `work` doc is shared with a manager. Seeds about a disagreement or a plan the user disproved must be written blame-free and factual ("tested the plan with a real order; the recurring order is only created on the next billing date; proposed two alternatives"). If a seed can't be written that way, put it in `projects/side/brag/<employer>-private.md` instead and leave a one-line pointer.

## Method & sources
- **Lucas Faria** — monthly cadence (first of the month), the 4 fields, the "would be much better if…" unblock field, and *share it with your manager and ask for feedback on what's written* (makes their perf-review job easier, anchors the conversation on what happened).
- **Julia Evans** — impact over tasks, the category taxonomy, "make it sound exactly as good as it is", and that a running doc beats memory six months later. Original: https://jvns.ca/blog/brag-documents/
- **cv-craft `STORIES.md`** — ownership ladder, status vocabulary, metric provenance and the story card format.

## Cadence
Monthly. For `work`, share with the manager after each entry. For `side`, the log is CV/portfolio source — keep it publishable.

## Humanize the written prose (if available)

Before writing generated prose to a file, if the `humanizer` skill is installed, run it on the drafted text so the created document reads naturally and free of AI tells; skip silently if it is not available. Apply it to the human-facing document body only, never to code, frontmatter, file paths, IDs, or literal templates.
