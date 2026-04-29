# claude-skills

A small collection of [Claude Code](https://claude.com/claude-code) skills, packaged as a plugin marketplace for one-line install.

## Skills in this collection

| Skill | What it does |
|-------|--------------|
| [`swe-compass`](swe-compass/) | Multi-mode software engineering coach — architect, advisor, reviewer, refactor, and concept explainer. Stack-agnostic by default. |

More skills will be added over time.

## Install

Add this repo as a marketplace and install the skill you want:

```text
/plugin marketplace add mqmalagris/claude-skills
/plugin install swe-compass@claude-skills
/reload-plugins
```

That registers the marketplace and installs the chosen skill into your local Claude Code. To install additional skills from this collection later, just rerun `/plugin install <name>@claude-skills`.

## Use

Each skill self-describes its triggers in its own README. For `swe-compass`, the typical triggers are:

```text
/swe-compass help me architect X
/swe-compass review this code: <paste>
/swe-compass refactor this <function>
/swe-compass explain SOLID
```

You can also just mention the skill in a normal prompt: `use swe-compass to review this PR`.

## Contributing

Issues and PRs welcome. Suggested workflow for new skills in this monorepo:

1. Create a new top-level folder `<skill-name>/` with the standard layout (`SKILL.md`, `workflows/`, `topics/`, `reference/`, `checklists/`).
2. Add a `<skill-name>/.claude-plugin/plugin.json` manifest.
3. Register the new plugin in `.claude-plugin/marketplace.json`.
4. Add an entry to the table above.

## License

MIT — see [LICENSE](LICENSE).
