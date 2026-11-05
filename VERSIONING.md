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

Releases run in GitHub Actions (`.github/workflows/release.yml`), in two steps:

1. **Prepare.** Run the `release` workflow by hand (the Actions tab, or `gh workflow run release.yml -f bump=minor`) and pick `patch`, `minor` or `major`. It validates `main`, bumps the collection version, moves the `[Unreleased]` notes under the new version on a `release/vX.Y.Z` branch cut from `main`, and opens a "release vX.Y.Z" PR with the notes as its body. Running it again rebuilds that PR from the current `main`, which is what you want after a skill was published while it was open. A rebuild replaces the branch, so fix the notes in `CHANGELOG.md` on `main`, not on the release branch. Once the new PR is up, an open release PR for a different version is closed and its branch deleted. The new version must be above the current one and the latest tag, and prepare refuses while the version already on `main` has no release.
2. **Publish.** Merge the PR. On every push to `main`, the workflow reads the collection version, and if it has no release yet, it tags the commit that set that version `vX.Y.Z` (the release PR's merge, even if more commits landed since) and creates the GitHub Release from the version's CHANGELOG section. Running it again is safe: if the tag and the Release both exist there is nothing to do, and a tag without a Release gets its Release.

Nothing pushes `main` directly; a release always lands through its PR and the `validate` check.

**One-time setup.** The prepare step opens the PR with the Actions token, which needs **Settings, Actions, General, "Allow GitHub Actions to create and approve pull requests"** turned on. A PR opened with that token triggers no other workflows, so prepare dispatches `validate.yml` on the release branch itself to put the required check on the PR.

**Local fallback.** The same two steps, for when the workflow is broken or Actions is down. Run them from a clone whose only remote is `origin`, or set `GH_REPO=mqmalagris/agent-skills`, so `gh` opens the PR and the Release on this repo. `publish --ref <commit>` also finishes an older release whose tag went out without its Release, and doesn't mark it Latest.

```bash
python3 scripts/release.py prepare --bump minor --dry-run   # preview the version and notes
python3 scripts/release.py prepare --bump minor --pr        # push release/vX.Y.Z and open the PR with your gh login
python3 scripts/release.py publish --ref origin/main        # after the merge: the tag and the Release; pushes only a tag
```

## CI

`.github/workflows/validate.yml` runs on every push to `main`, every PR, and on dispatch. It runs `scripts/validate_repo.py` (every `skills/<name>/` has a `SKILL.md` + `plugin.json`, all JSON parses, names are kebab-case and consistent, versions are valid SemVer, and each `plugin.json` version matches its `marketplace.json` entry) and the release script's tests in `scripts/tests/`. Those tests use a fake `gh` written as a shell script, so on native Windows they skip; run them under WSL or Linux.

`.github/workflows/release.yml` runs the two release steps above.
