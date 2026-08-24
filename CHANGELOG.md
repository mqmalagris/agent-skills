# Changelog

All notable changes to this collection are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the collection follows [SemVer](https://semver.org). See [VERSIONING.md](VERSIONING.md) for the per-skill vs collection model.

## [Unreleased]
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
