---
name: commit-report
description: Generate dual-format commit report (prose paragraph + bullet list) from recent git activity, tunable to audience (dev / pm / client). Use when user asks for a standup note, status update, work summary, "what did I ship today", commit recap, end-of-day report, PM/client update, or runs /commit-report. Triggers on phrases like "write a report", "summarize commits", "report for the PM", "update for the client", "what did I do today". Always emits BOTH a prose Report and a Bullets list in the same response, level-tuned. Default scope = current user's latest commit batch at HEAD; supports --since <hash>, --last, --count, --range, --path overrides.
---

# commit-report

Generate two-part commit report: prose paragraph + bullet list. Always both, in same response. Audience-tuned: `dev` (tech-heavy), `pm` (mid), `client` (no jargon). Source = git log of current repo.

## Quick start

```
/commit-report                          # default: dev level, --since-mine scope
/commit-report pm                       # PM-friendly summary of latest batch
/commit-report client --last 4h         # client-safe wording, last 4h
/commit-report dev --count 5            # last 5 commits by user
/commit-report pm --since a3f2c1d       # commits since this hash up to HEAD
/commit-report pm --range main..HEAD    # explicit range
/commit-report dev --path apps/web      # restrict to subdir
```

## Workflow

1. **Resolve user identity**: `git config user.email`. Bail with clear error if unset.
2. **Resolve scope** (precedence: explicit flag > default `--since-mine`):
   - `--since-mine` *(default, no arg)*: contiguous commits at HEAD authored by user. Walk back through `git log --pretty='%H%x09%ae'`; stop at first commit whose author email ≠ user. If HEAD's author ≠ user → fallback to `--last today` and note the fallback in output.
   - `--since <hash>`: explicit boundary. Run `git log <hash>..HEAD --author="$email"`. Hash = exclusive lower bound (commits AFTER `<hash>` up to HEAD). Accepts short or full SHA.
   - `--last <duration>`: `1h`, `4h`, `today`, `week`. Run `git log --author="$email" --since=<duration>`.
   - `--count <n>`: `git log --author="$email" -n <n>`.
   - `--range <ref..ref>`: `git log --author="$email" <range>`.
   - `--path <dir>`: append `-- <dir>` to any `git log` invocation. Repo cwd is default.
3. **Resolve audience** (positional first arg, default `dev`): `dev` | `pm` | `client`.
4. **Collect commit data**: subject, body, files changed (`git show --stat --pretty=format:'%H%n%s%n%b' <sha>`). Skip merge commits (`Merge branch …`, `Merge pull request …`) unless `dev` + `--include-merges`.
5. **Synthesize** per audience (see [Audience map](#audience-map)). Group related commits; do not echo subjects 1:1.
6. **Render** in this exact order:

   ```
   ## Report
   <prose, level-appropriate>

   ## Bullets
   - point 1
   - point 2
   ```

7. **Bullet count**: 5–8 default. Each bullet = one shipped change, verb-first, level-vocab.
8. **Report length**: dev ≈ 2 short paragraphs; pm ≈ 1 paragraph (~120 words); client ≈ 1 paragraph (~80 words).

## Audience map

| Concept                    | dev                                                     | pm                                              | client                              |
| -------------------------- | ------------------------------------------------------- | ----------------------------------------------- | ----------------------------------- |
| `useEffect` cleanup leak   | "fixed memory leak in `useEffect` cleanup on Dashboard" | "fixed memory leak in dashboard"                | "dashboard runs smoother"           |
| DB index added             | "added btree index on `orders.user_id`"                 | "sped up order lookups"                         | "orders load faster"                |
| Pure refactor, no UX delta | "extracted `AuthGuard` HOC, dedup in 4 routes"          | "cleaned up auth code for maintainability"      | "ongoing improvements to keep things stable" |
| Auth bug                   | "fixed JWT expiry off-by-one in `validateToken`"        | "fixed login bug where sessions expired early"  | "login is more reliable"            |
| New endpoint               | "added `POST /api/exports` with stream response"        | "shipped exports endpoint for the export flow"  | "you can now export your data"      |

Rules per level:

- **dev**: backticks for files/functions/symbols. Short SHAs in parens, e.g. `(a3f2c1d)`. May mention internals.
- **pm**: no SHAs, no file paths, no function names. Frame as features / fixes / improvements / cleanup. Light tech terms OK ("API", "auth flow", "caching").
- **client**: outcomes only. No tech terms. No internal names. Always include every commit — frame refactor/chore/test work as softened reliability/stability statements ("ongoing improvements", "behind-the-scenes work to keep things stable", "groundwork for upcoming features"). Never drop commits silently.

## Edge cases

- **No commits in scope** → state plainly, suggest widening (`--last today`, `--last week`).
- **`--since-mine` + HEAD not user's** → fallback to `--last today`, prepend one-line note: *"HEAD not authored by you — showing today's commits instead."*
- **Mixed merge commits** → skip by default; include only with `dev --include-merges`.
- **Single commit** → still produce both Report and Bullets (Bullets may be 1–2 items).
- **Repo not initialized / outside repo** → bail with clear error.
- **Commit body contains secrets/tokens** → surface only subject + summarized intent, never raw body.

## Output rules

- Both `## Report` and `## Bullets` always rendered, in that order, in same response.
- No emoji.
- Code/file refs in backticks at `dev` only.
- No commit hashes in `pm` / `client`.
- Caveman mode does NOT apply to report content — write normal prose. Commands/code still verbatim.
