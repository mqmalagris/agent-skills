# Changelog

All notable changes to this collection are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the collection follows [SemVer](https://semver.org). See [VERSIONING.md](VERSIONING.md) for the per-skill vs collection model.

## [Unreleased]
- Eval coverage for the rest of the core chain: grill-me (4 cases), to-prd (3), blueprint (4), pr-craft (3) and implementation-review (2), on top of dev-flow, review-pass and sentinel. Fixtures are self-contained scaffold scripts (a shared saved-carts repo with an ADR, intent, PRD and plan), so grill-me, to-prd and blueprint run on native Windows; the git-driven pr-craft and implementation-review cases are tagged `needs-bash`.
- Eval trend: `evals-history/<skill>.jsonl` is committed, one line per recorded run (date, version, content hash, per-case with/without scores, mean delta). `scripts/eval-run.sh <skill> --record [--runs N] [--baseline]` runs a suite and appends to it; `scripts/eval_history.py trend` prints the history. The pre-push hook now delegates to `eval-run.sh` and skips a skill whose pushed content already has a passing recorded entry.
- publish-skill: runs the skill's eval suite on the publisher's own Claude login before committing and commits the result to `evals-history/`, aborting below threshold (`--skip-evals` to override). Resolves Git for Windows' bash rather than the System32 WSL launcher stub.
- grill-me: tighten "one question at a time" to forbid a second decision tucked into the closing line. Caught by the new eval: 8/10 before, 10/10 after, same rubric.
- pr-craft: count the task's new files in the size gate (`git add -N` first). `git diff --numstat HEAD` ignores untracked files, so a feature made of new files measured 0 lines and bypassed the 800-line stack gate.
- review-pass: code-review runs in a fresh subagent when the session wrote the diff (the writer does not grade its own work), and a per-repo review ledger turns a mistake class caught twice into a proposed CLAUDE.md rule. Adds a 3-case eval suite (docs-only, auth trust boundary, quick depth).
- sentinel: tier-2 control bands (mean/σ over a trailing baseline) alongside hard thresholds, with graded responses: 1σ log, 2σ read-only diagnosis in the intent, 3σ or threshold breach files an urgent intent and alerts. Adds a 3-case eval suite (revert files an intent, healthy repo stays quiet, low commit-convention coverage files nothing).
- cv-craft: disable ligatures in the PDF stylesheet and add verify-pdf.py, so rendered CVs extract as real text for ATS keyword search
- Add `claude plugin eval` behavioral regression suites, starting with dev-flow (8 cases: one per tier, resume-from-existing-plan, trivial-edit skip, and a negative trigger). New `scripts/hooks/pre-push` runs the suite of any skill a push changes on the pusher's own Claude login (`git config core.hooksPath scripts/hooks`); `needs-bash` cases skip on native Windows. Measured locally at mean Δ +0.50 against a no-skill baseline, +1.00 on every tier-routing case.

## [0.13.0] - 2026-09-17

- blueprint: rename of `heist` (v0.3.0 lineage continued at v0.4.0). Document sections formalized for PR review: The Job / Crew / Sequence / Payoff / Blind Spots / Getaway become Summary / Files Affected / Implementation Phases / Acceptance Criteria / Edge Cases / Rollback and Risk. Drop the `phase` frontmatter field, whose only consumer was maestro. All 10 referring skills updated; `implementation-review` and the plan parser accept both heading styles so pre-rename plans keep working.
- Remove maestro. Its premise never held in practice: across 54 authored plans no two ever shared a `phase` value, and every declared `depends on` was sequential ("X must merge first"), which is the opposite of the parallelism it existed to find. `parallel-worktrees` absorbs the plan-driven case instead of deferring to it.
- compass: delegate test strategy to `testing-philosophy`, whose Testing Trophy and e2e floor the old pyramid material contradicted; `topics/testing.md` is now testability-as-design-signal only. Add Decision checkpoints, so a hard-to-reverse decision is presented with a recommendation, trade-offs and flip conditions and then confirmed with the user rather than decided for them. Stack policy now requires a ranked recommendation instead of a survey. Description picks up the legacy-code triggers the workflow already served.
- pr-craft: add a diff size gate before the branch and commit steps (under 400 lines one PR, 400-800 offer the split, over 800 propose a stack), measured with `git diff --numstat <base>...HEAD` excluding lockfiles and generated output, and explicit that size alone never justifies splitting a change with one seam. Document that `gh stack merge` with no argument merges the entire stack without prompting in a non-interactive shell.
- dev-flow: add a `design` tier that ends at artifacts rather than a diff (adhd, grill-me, to-prd, compass, blueprint, then pr-craft docs-only), for work that must be designed and signed off without being built.
- commit-report: enforce a formal, agentless voice (no grammatical person in any of the three) across report prose, bullets and the channel block. Add a Discretion section so a fix states present behavior instead of narrating the prior defect, with client rules against before/after contrast, defect duration and scope, and jokes about a failure, plus a one-neutral-clause allowance at pm. Run the humanizer pass on every report rather than only on `--doc` bodies, leashed to both voice rules. Retire the `voice` config key; any persisted value, legacy `"first"` included, is read and ignored.

## [0.12.0] - 2026-08-31

- security-audit: narrow scope to change review. The description now declines whole-codebase and posture audits, and a new 'When this is the wrong skill' section routes them to wstg-security-testing mode 2, naming the three precedents that break on a repo-wide ask.
- wstg-security-testing: add reference/CODEBASE-AUDIT.md, a systematic whole-codebase audit protocol for mode 2 (stack detection and category mapping, route-handler enumeration, tenant-isolation and secret sweeps, frontend-gate cross-referencing, evidence-backed strengths). Mode 2 now owns repo-wide security asks.
- Add audit-report: render audit findings as an A4 PDF with severity donut, category bars, severity chips, evidence-backed strengths, and copy-ready GitHub issue blocks. English default, pt-BR label pack, self-verifying render.

## [0.11.0] - 2026-08-28

- pr-craft: report which automated reviewers the repo runs when the PR is opened
- testing-philosophy: correct the sibling-skill list in the description (/verify no longer exists)
- implementation-review: repoint the pre-commit live check from the removed /verify to /run; fall back to docs/intent for plan-gap checks
- babysit-prs: add PROVENANCE-FLAG triage row and bot identification by user.type; flag silent or paused automated reviewers
- commit-report: add --metrics (review coverage, rework depth, artifact lag, spec churn, recurring fix classes)
- to-prd: read docs/intent as a Glossary source when the conversation does not carry the grill-me block
- grill-me: persist Design Notes, Glossary and edge cases to docs/intent/NNNN-<slug>.md instead of leaving them in conversation
- review-pass: harvest existing automated review before running its own stages; add the automated-reviewers reference
- dev-flow: add sentinel as the scheduled Maintain stage, make the on-disk artifact chain explicit, repoint the review tail's live check to /run
- Add sentinel: scheduled post-ship detector that files recurring fix classes, reverts, and prod threshold breaches as docs/intent files

## [0.10.4] - 2026-08-26

- exclusion rule states the principle (employer- and client-owned skills stay out) instead of naming one private skill

## [0.10.3] - 2026-08-26

- Flutter audio guidance no longer names a specific app; the technical anchors (SF2 SoundFont, MIDI, FFI) carry the specificity

## [0.10.2] - 2026-08-26

- folder-matching examples genericized (no client or personal project names); each example now states which matching case it illustrates

## [0.10.1] - 2026-08-26

- drop third-party ponytail marker from the scope note; rationale kept verbatim
- reads the periscope contribution log as a first-class evidence source in draft and compile, so influence work with no commit behind it reaches the promo packet

## [0.10.0] - 2026-08-26

- new skill: role-driven opportunity scan across tech / product / org lenses, kind-based surfaces with a hard tool allowlist, per-lens credibility, evidence trail for brag-doc
- drop third-party ponytail attribution; the rule keeps the idea as its own stated floor
- review tail delegated to review-pass as one stage (was verify + code-review + implementation-review restated inline); removes the duplicated gate specs that had drifted, and the chain now ends in one merged go/no-go verdict
- adds quick depth (verify + code-review only) and an orchestrator-driven mode that skips the confirm step; now the single owner of the review gate policy
- stdout/stderr forced to UTF-8: publishing a NEW skill whose description contains an arrow or dash no longer dies with UnicodeEncodeError on a cp1252 console
- new skill: review-only entry point over verify -> code-review -> implementation-review, merged into one go/no-go verdict
- new skill: LLM-maintained interlinked Markdown wiki with ingest / query / lint operations
- employer-internal exclusion note is employer-agnostic
- client tier is employer-agnostic (no employer name)
- employer-agnostic: target `al` renamed to `work`, employment doc path generalized to <employer>.md with multi-employer resolution
- employer-agnostic: agency-specific sections reframed as client-services context (applies whenever a paying stakeholder sits between team and end user); employer name removed
- copytree now ignores __pycache__, *.pyc, .DS_Store, .pytest_cache and *.egg-info so build droppings are never vendored into the public repo
- new skill: cross-store ASO from one per-locale Markdown source, free live-store keyword probing, listing linter
- sync mode gains standalone-rewrite sub-flow, DOCX export, three-tier metric markers and data-integrity rules; example persona genericized (no real PII or client names)
- scripts 33 -> 88 (crawl audit, schema tooling, a11y, LCP subparts, repo SEO, log analysis) + reference and sub-skill updates
- Check 3 now reconciles the shipped diff against the plan Blind Spots ledger
- new "## The Blind Spots" section: pre-code edge-case ledger with a decision per case
- new "## Edge cases" output block: lens 6-7 findings survive the session with a handle/defer/wont decision
- edge-case ledger now flows grill-me -> heist -> implementation-review
- `dev-flow` 0.4.1 — updated
- `parallel-worktrees` 0.1.1 — updated

## [0.9.0] - 2026-08-12

- `dev-flow` 0.4.0 — add observability rule (name outcome metric + add telemetry before pr-craft, risk-scaled) alongside the test-sequencing rule
- `dev-flow` 0.3.0 — add "test the sharp edge as you cut it" rule (risk-driven early tests) + cross-ref testing-philosophy

## [0.8.0] - 2026-08-11

- `dev-flow` 0.2.1 — updated
- `pr-craft` 0.2.0 — updated
- `publish-skill` 0.1.2 — fix: `git clean -fd` in ensure_repo so a stray dry-run skill dir cannot be swept into the next publish

## [0.7.0] - 2026-08-10

- `commit-report` 0.1.3 — updated
- `babysit-prs` 0.1.0 — new skill
- `commit-report` 0.1.2 — updated

## [0.6.0] - 2026-08-10

- `dev-flow` 0.2.0 — updated

## [0.5.0] - 2026-08-07

### Added
- `semver` — decide and apply the SemVer bump for a change: analyzes the diff against the public surface, runs the ecosystem's breaking-change detector (Rust/npm/Go/Elixir/Python), then bumps the manifest + changelog. Stack-agnostic; feeds `publish-skill` / `release.py`.

### Changed
- Adopted a PR-based workflow: `publish-skill` now opens a CI-gated PR by default (`--auto-merge` / `--merge` / `--push-main` to control) instead of pushing to `main`.
- README: added the skills.sh badge.

## [0.4.1] - 2026-08-07

### Fixed
- `brag-doc`, `cagan-check`, `code-craft`, `commit-report`, `portfolio-sync` had an unquoted `: ` in their SKILL.md frontmatter `description`, which broke strict YAML parsers and hid them from [skills.sh](https://www.skills.sh/mqmalagris/agent-skills). Descriptions converted to `>-` block scalars; each patch-bumped.

### Changed
- `validate_repo.py` now strict-parses SKILL.md frontmatter (PyYAML in CI, colon-space heuristic locally) so invalid frontmatter fails the build.

## [0.4.0] - 2026-08-07

### Added
- Seven skills: `implementation-review`, `security-audit`, `testing-philosophy`, `parallel-worktrees`, `pr-craft`, `brag-doc`, `cagan-check`.
- `publish-skill` — publish a local skill to this repo: mint `plugin.json`, upsert `marketplace.json`, auto-bump its SemVer, log a CHANGELOG entry, commit + push.
- Dual-format install: usable as a Claude Code plugin marketplace **and** via `bunx skills`.
- `THIRD_PARTY.md` — skills used but not vendored here.
- Versioning + release tooling: `VERSIONING.md`, this changelog, CI manifest validation (`scripts/validate_repo.py` + `.github/workflows/validate.yml`), and `scripts/release.py`.

### Changed
- Restructured all skills under `skills/<name>/` (previously at the repo root).
- Renamed the repo `claude-skills` -> `agent-skills`.
- Added a "Humanize the written prose (if available)" hook to the nine doc-writing skills (`to-prd`, `heist`, `compass`, `cv-craft`, `portfolio-sync`, `brag-doc`, `commit-report`, `seo`, `grill-me`).

### Removed
- `write-with-ai`.

## [0.3.0] - 2026-08-07

### Added
- Initial curated collection, packaged as a Claude Code plugin marketplace.
