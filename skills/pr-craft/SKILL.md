---
name: pr-craft
description: Create a pull request with a structured, concise description derived from the diff and conversation context. Use when the user asks to "create a PR", "open a PR", "PR to <branch>", "raise a pull request", or wants the full branch → commit → push → gh pr create flow. Produces a body with Problem / Root cause / Fix / Test / Out of scope sections and references task/ticket IDs.
---

# pr-craft

Drive a clean PR end to end: branch, stage only the relevant files, conventional-commit, push, open the PR with a structured body.

## Flow

1. **Inspect.** `git status` + `git diff` (and `git diff --staged`). Identify which changed files belong to *this* task. Pre-existing modified/untracked files unrelated to the work (lockfiles, config, scratch dirs) are NOT yours — leave them.
2. **Branch.** If on the base branch (`main`/`staging`/`master`), create `type/short-slug` (e.g. `fix/marketing-consent-required-signup`). Type matches the commit type. If already on a feature branch, stay.
3. **Stage explicitly.** `git add <file> <file> …` — name each relevant file. Never `git add .` / `-A`. Re-run `git status` to confirm only intended files are staged.
4. **Commit.** Conventional Commits subject (`type(scope): summary`, ≤72 chars). Body explains *why* + bullet the changes. End with `Refs task <id>` / `Refs <ticket>` when known. Obey the repo's CLAUDE.md (e.g. no `Co-Authored-By` trailer if it says so).
5. **Push.** `git push -u origin <branch>`.
6. **Open PR.** `gh pr create --base <base> --head <branch> --title "<same as commit subject>" --body "$(cat <<'EOF' … EOF)"`. Base = the branch the user named, else the repo default (`staging` here, often `main` elsewhere — check `git remote show origin` or repo CLAUDE.md if unsure).
7. **Report** the PR URL. Offer follow-ups (log time, comment the link on the task).

## PR body structure

Only include sections that carry signal — drop empty ones. Concise, no filler.

```md
## Problem
What's broken / needed and who reported it. The user-facing or compliance impact.

## Root cause
Why it happens, by layer/file. Cite `file:line` or function names.

## Fix
- Bullet each change, what it does and why.
- Note side effects / benefits.

## Test
1. Numbered manual steps a reviewer runs to confirm.

## Out of scope (flag to <owner>)
- Known gaps deliberately not handled (other locales, data backfill, etc.).

Refs task <id>
```

## Gotchas

- **Bash tool is POSIX sh** — for multi-line commit/PR text use a heredoc (`-F -` for commit, `$(cat <<'EOF' … EOF)` for `--body`). Do NOT use PowerShell here-strings (`@'…'@`) in the Bash tool — the `@` leaks into the message. Quote the heredoc delimiter (`<<'EOF'`) so backticks/`$` stay literal.
- **Don't sweep unrelated changes** into the commit — the #1 mistake. Stage by name.
- **Subject = PR title** — keep them identical.
- Derive body content from the actual diff + what was discussed, not guesses. If root cause wasn't established, say "investigating" rather than inventing one.

See [EXAMPLE.md](EXAMPLE.md) for a full worked PR.
