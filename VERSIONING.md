# Versioning & releases

This collection uses **per-skill SemVer** plus **collection releases**. Two axes, both meaningful:

## Per-skill version (source of truth)

Each skill carries its own version in `skills/<name>/.claude-plugin/plugin.json`, mirrored in its `marketplace.json` entry (CI enforces they match). This is the version consumers see when they install one skill (`bunx skills add mqmalagris/agent-skills -s <name>`, `/plugin install <name>@agent-skills`).

Bump it per [SemVer](https://semver.org) when the skill changes:

| Part | When |
|------|------|
| **MAJOR** | Breaking change to the skill's contract: renamed/removed flags, changed output format or file paths, removed capability. |
| **MINOR** | New capability, mode, or option; backward-compatible additions. |
| **PATCH** | Wording, clarifications, bug fixes, no behavior change. |

`publish-skill` bumps the changed skill's PATCH automatically on republish (`--bump minor|major` or `--version` to override, `--no-bump` to hold).

## Collection version (human-facing snapshot)

`marketplace.json.metadata.version` versions the whole set. Each release gets a git tag `vX.Y.Z` and a GitHub Release whose notes come from the CHANGELOG. Think of it like a monorepo release ([Changesets](https://github.com/changesets/changesets) model) or a distro snapshot: the individual skills are independently versioned, the tag names the state of the collection on a date.

| Part | When |
|------|------|
| **MAJOR** | Structural change to the repo (layout, install mechanism, mass removal). |
| **MINOR** | Skills added or removed. |
| **PATCH** | Edits within the existing set (no add/remove). |

## Changelog

`CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com). Unreleased work accumulates under `## [Unreleased]` (grouped Added / Changed / Removed / Fixed); `publish-skill` appends a line there per publish. Cutting a release rolls that section into the new version.

## Cutting a release

```bash
python3 scripts/validate_repo.py            # runs in CI too; must pass
python3 scripts/release.py --bump minor      # or --version X.Y.Z / --bump patch|major
```

`release.py` validates, sets the collection version, rolls the CHANGELOG, commits, tags `vX.Y.Z`, pushes main + tag, and creates the GitHub Release. Use `--dry-run` to preview, `--no-push` to stop at the local commit + tag.

## CI

`.github/workflows/validate.yml` runs `scripts/validate_repo.py` on every push and PR: every `skills/<name>/` has a `SKILL.md` + `plugin.json`, all JSON parses, names are kebab-case and consistent, versions are valid SemVer, and each `plugin.json` version matches its `marketplace.json` entry.
