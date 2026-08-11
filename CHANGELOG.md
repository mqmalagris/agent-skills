# Changelog

All notable changes to this collection are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the collection follows [SemVer](https://semver.org). See [VERSIONING.md](VERSIONING.md) for the per-skill vs collection model.

## [Unreleased]
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
