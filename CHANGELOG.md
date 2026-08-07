# Changelog

All notable changes to this collection are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the collection follows [SemVer](https://semver.org). See [VERSIONING.md](VERSIONING.md) for the per-skill vs collection model.

## [Unreleased]

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
