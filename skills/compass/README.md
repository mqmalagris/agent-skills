# swe-compass

A multi-mode software engineering coach for [Claude Code](https://claude.com/claude-code).

Routes the user's request to one of five workflows backed by topic and reference material covering processes, requirements, modeling, design principles, design patterns, architecture, testing, refactoring, and DevOps.

## What it does

| Intent | Workflow |
|--------|----------|
| Design a system / pick architecture / structure new feature | architect |
| "Should I…", "how should I…", pre-code consultation | advisor |
| Review code / PR / diff against principles | reviewer |
| Refactor / clean up / fix code smell | refactor |
| Explain a concept / pattern / principle | explain |

## Install

```text
/plugin marketplace add mqmalagris/agent-skills
/plugin install swe-compass@agent-skills
/reload-plugins
```

## Trigger

```text
/swe-compass help me architect a multi-channel notification system
/swe-compass review this code: <paste>
/swe-compass refactor this function: <paste>
/swe-compass explain SOLID
```

Or mention it inline: `use swe-compass to review this PR`.

## Stack policy

Stack-agnostic by default. If you haven't named a stack, the skill asks what stacks you know, walks the trade-offs for the project at hand, and **defers to your final choice**. After the choice, recommendations are tailored to that stack's idioms — no patterns the language already solves natively.

## Layout

```
swe-compass/
├── SKILL.md              # entry point + intent routing
├── workflows/            # one file per workflow
├── topics/               # processes, principles, patterns, architecture, testing, etc.
├── reference/            # cross-cutting tables (heuristics, quality criteria, anti-patterns, …)
└── checklists/           # operational pass-lists for design, review, refactor, ADR
```

## Output discipline

- Concrete recommendations first, theory second.
- Always surfaces trade-offs (gain / loss / simpler alternative).
- Treats best practices as defaults with counter-cases, not commandments.
- Concise by default; expands on request.

## License

MIT — see [LICENSE](../LICENSE) at the repo root.
