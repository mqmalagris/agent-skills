---
name: review-pass
description: Single review-only entry point for an existing diff — runs verify → code-review → implementation-review (and security-audit only when the change touches a trust boundary), then consolidates every finding into one go/no-go verdict. Use when you have a change ready and want it reviewed without running the whole dev-flow build chain. Triggers on /review-pass, "review this diff", "review my changes", "is this ready to commit", "give this a once-over". NOT for reviewing a remote GitHub PR (use /code-review) or for a task still being built (use /dev-flow).
---

# review-pass

Thin orchestrator over the review stages of the canonical chain. It does NOT re-implement any check — each sub-skill owns its own logic and its own skip rules. This skill only scopes the diff, orders the stages, drives them, and merges their output into one verdict. Point it at a change that's already written; it decides nothing about how the change was built.

Executor note: this is a prompt, not a script. Drive one stage via the Skill tool, wait for it to finish, checkpoint, then start the next. Never fire all four blind.

## Protocol

1. **Scope** — determine what's under review. Default: the local working-tree diff (staged + unstaged) vs the merge-base. Accept an explicit target (`--staged`, a commit range, a path). From the diff note two things that drive the plan: (a) does it have **runtime surface** (product source, not docs/test-only) — gates `verify`; (b) does it touch a **trust boundary** (auth/authz, input parsing, secrets, file upload, external calls, SQL) — gates `security-audit`.
2. **Print the plan** — the four stages, each marked RUN or SKIP with a one-line reason (table below). Never skip silently.
3. **Confirm** — user says go / edit / abort. Accept partial edits ("skip verify", "add security-audit"). **Skip this step when an orchestrator drove you here** — dev-flow runs this as one chain stage and already had the user approve the whole chain; a second confirm inside an approved run is friction, not safety. Print the plan as a notice and proceed.
4. **Drive** — invoke each RUN stage via the Skill tool, in order. After each returns, checkpoint: report its findings (blockers vs nits) in one line, then start the next. A blocker from an early stage doesn't halt the pass — collect everything, decide at the end.
5. **Verdict** — merge all findings into ONE list, deduped, ranked blocker → nit. Close with a go/no-go: **ship** (no blockers), **fix-first** (blockers listed), or **needs-a-human** (findings you can't adjudicate). This consolidated verdict is the whole point of the skill — don't just concatenate the sub-skill outputs.
6. **Act** — if there are actionable findings, ask how to apply them (skip this if the verdict is clean; when orchestrator-driven, a clean verdict returns straight to the conductor with no prompt):
   - **Post as PR comments** — re-run `/code-review --comment` so findings land as inline comments on the PR. Only offer this when a PR actually exists for the branch; if none does, say so and drop the option.
   - **Fix directly** — re-run `/code-review --fix` to apply the findings to the working tree. Then re-verify the touched paths.
   - **Just report** — leave the verdict as-is; the user handles it.

   Don't pick for the user — ask, then do exactly what they choose.

## Stages

Run in this order — cheapest signal and hardest gate first.

**Depth.** Default runs all four gates. `quick` runs stages 1–2 only, and exists for one case: a single-file fix with no plan, where implementation-review's plan and coverage checks have nothing to read against and code-review already covers a diff that small. dev-flow passes `quick` on its bug tier and the default everywhere else. Anything beyond a one-file fix uses the default — when unsure, use the default.

| Stage | Order | Gate (RUN only when true) |
|-------|-------|---------------------------|
| **verify** | 1 | Diff has runtime surface. SKIP for docs/test-only diffs — nothing to drive. |
| **code-review** | 2 | Anything beyond a trivial one-liner. Hunts correctness bugs in the diff. |
| **implementation-review** | 3 | Always at default depth, for a real change. SKIP at `quick`. Seven parallel checks; **its check 7 already runs security-audit**, so this covers the baseline security pass. |
| **security-audit** | 4 | SKIP by default — implementation-review already ran it. RUN standalone ONLY when the change sits squarely on a trust boundary and you want the full WSTG pass, not the summary check. On a plain UI/CRUD diff this is pure double-pay. |

## Rules

- **Orchestrate, don't decide inside a stage.** Once a sub-skill is invoked, follow its instructions — don't second-guess its internals.
- **This skill owns the review gates.** dev-flow delegates its entire review tail here and deliberately does not restate these gates. They were duplicated in both files once and drifted — dev-flow said "SKIP implementation-review on the bug tier" while this file said "always". A gate policy changes here, and only here.
- **Never skip silently.** Print SKIP + reason so the user can override.
- **Don't double-pay security.** implementation-review → security-audit is redundant unless the diff is genuinely security-shaped. Say so in the SKIP reason.
- **One verdict, not four.** The value is the merged, deduped, ranked finding list + a single go/no-go — not a wall of concatenated reports.
- **Review first, act second.** The four stages are read-only; only the step-6 Act phase touches anything, and only with the user's pick. Fixing is `/code-review --fix`, PR comments are `/code-review --comment` — this skill routes to them, it doesn't re-implement either. Committing is still pr-craft's job.
- **Obey CLAUDE.md conventions** (shell wrappers, etc.) — sub-skills that touch the shell already honor these.

## When to skip review-pass entirely

- Reviewing a remote GitHub PR — use `/code-review <pr-number>` (it takes a PR number, branch, or path, and supports `--comment` / `--fix`).
- Mid-build task with no diff yet — use /dev-flow (it builds first, then drives this skill as its review stage).
- One-line edit, typo, rename — just eyeball it.
