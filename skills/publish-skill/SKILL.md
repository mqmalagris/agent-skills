---
name: publish-skill
description: "Publish one of the user's own skills from ~/.claude/skills to the mqmalagris/agent-skills GitHub repo — copies the skill under skills/<name>/, mints its .claude-plugin/plugin.json, upserts the marketplace.json entry, then commits and pushes to main. Use when the user says 'publish this skill', 'push <skill> to my repo', 'add <skill> to agent-skills', 'ship this skill', or wants a locally-authored skill added to their public skill collection. NOT for third-party skills (those go in THIRD_PARTY.md, not vendored) or for editing skill content."
---

# publish-skill

Publishes a locally-authored skill (`~/.claude/skills/<name>/`) to **mqmalagris/agent-skills** (a dual-format Claude-marketplace + `bunx skills` repo). The script does all mechanical work idempotently; you supply the two editorial bits it can't guess: **category** and **keywords**.

Do not use this for third-party skills — those belong in the repo's `THIRD_PARTY.md`, not vendored. `al-cli` stays out entirely (Arctic Leaf internal).

## Steps

1. **Confirm it's the user's own skill.** If it's a fork/adaptation, note the upstream so the description can attribute it (the repo credits adapted skills). Bail if it's third-party.
2. **Decide category + keywords.** Read the skill's `SKILL.md`. Category matches the repo's groups: `engineering-workflow`, `security`, `development`, `reporting`, `career`, `product`, `meta`, `marketing`. Keywords: 3-6 kebab tags. The script derives a concise description from the SKILL.md frontmatter unless you pass `--description`.
3. **Run the script** (kebab-case skill name = its dir name):
   ```bash
   python3 ~/.claude/skills/publish-skill/scripts/publish_skill.py <skill-name> \
     --category <category> --keywords tag-a,tag-b,tag-c
   ```
   It refreshes a repo cache, copies the skill, mints `plugin.json`, upserts `marketplace.json`, validates all JSON, commits, and pushes to `main` (verifying the remote SHA). Use `--no-push` to stop at the local commit, `--dry-run` to prepare without committing, `--description "..."` / `--version X.Y.Z` to override.
4. **Update the README table.** The script prints a suggested row and the target `skills/` path. Add that row to the right group section in the repo's `README.md`, then commit + push it (the script does not touch README — groupings are editorial). Skip only if the user says the README doesn't matter.
5. **Report** the pushed commit SHA and the install commands: `bunx skills add mqmalagris/agent-skills -s <name>` and `/plugin install <name>@agent-skills`.

## Notes

- Re-running for the same skill **updates** it (no duplicate marketplace entry) — safe for republishing after edits.
- Repo conventions and the full layout are in memory `[[reference-agent-skills-repo]]`. The script hardcodes the repo URL, author (Matheus Malagris), and MIT license to match.
- Requires `gh`/git auth for the push (already configured for this user).
