# claude-skills

A small collection of [Claude Code](https://claude.com/claude-code) skills, packaged as a plugin marketplace for one-line install.

## Skills in this collection

| Skill | What it does |
|-------|--------------|
| [`swe-compass`](swe-compass/) | Multi-mode software engineering coach — architect, advisor, reviewer, refactor, and concept explainer. Stack-agnostic by default. |
| [`code-craft`](code-craft/) | Language- and framework-specific code best practices and idioms. Reader and reviewer modes. Ships TypeScript, Rust, CSS/SASS, React, Next.js, React Native + Expo, and Hono references. |

The two are designed to compose: `swe-compass` for **across-system** decisions (architecture, design, refactoring strategy), `code-craft` for **inside-the-file** decisions (idioms, anti-patterns, framework conventions).

More skills will be added over time.

## Install

Add this repo as a marketplace and install the skills you want:

```text
/plugin marketplace add mqmalagris/claude-skills
/plugin install swe-compass@claude-skills
/plugin install code-craft@claude-skills
/reload-plugins
```

That registers the marketplace and installs the chosen skills into your local Claude Code. To install additional skills from this collection later, just rerun `/plugin install <name>@claude-skills`.

## Use

Each skill self-describes its triggers in its own README.

**`swe-compass`** — architecture, design, refactoring across modules:

```text
/swe-compass help me architect X
/swe-compass review this code: <paste>
/swe-compass refactor this <function>
/swe-compass explain SOLID
```

**`code-craft`** — language idioms and framework conventions:

```text
/code-craft what's the modern Rust error-handling pattern?
/code-craft review this TypeScript: <paste>
TS best practices for async cancellation
review this Hono route for idioms: <paste>
is `forwardRef` still needed in React 19?
```

You can also just mention the skill in a normal prompt: `use swe-compass to review this PR` or `apply code-craft to this file`.

## Contributing

Issues and PRs welcome. Suggested workflow for new skills in this monorepo:

1. Create a new top-level folder `<skill-name>/` with `SKILL.md` and supporting content (typical layouts: `workflows/`, `topics/`, `reference/`, `checklists/` — or `languages/`, `frameworks/` for reference-style skills).
2. Add a `<skill-name>/.claude-plugin/plugin.json` manifest.
3. Register the new plugin in `.claude-plugin/marketplace.json`.
4. Add an entry to the table above.
5. Add a `<skill-name>/README.md` describing triggers and structure.

## License

MIT — see [LICENSE](LICENSE).
