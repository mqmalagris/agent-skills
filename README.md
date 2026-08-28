# agent-skills

[![skills.sh](https://www.skills.sh/b/mqmalagris/agent-skills)](https://www.skills.sh/mqmalagris/agent-skills)

A curated, **dual-format** collection of [Agent Skills](https://www.anthropic.com/news/skills). Install it as a [Claude Code](https://claude.com/claude-code) plugin marketplace, **or** with [`bunx skills`](https://www.skills.sh/) into any of 75+ agents (Cursor, Copilot, Windsurf, Codex, …) — same `SKILL.md` files, either way.

Most skills are mine; a few are forks/adaptations of public skills, attributed per skill below. Third-party skills I use but don't vendor here live in [`THIRD_PARTY.md`](THIRD_PARTY.md).

## Install

**With `bunx skills` (any agent):**

```bash
bunx skills add mqmalagris/agent-skills             # pick skills interactively
bunx skills add mqmalagris/agent-skills -s heist    # just one
bunx skills add mqmalagris/agent-skills --all -g    # everything, installed globally
```

**With Claude Code (plugin marketplace):**

```text
/plugin marketplace add mqmalagris/agent-skills
/plugin install heist@agent-skills
```

## Layout

Each skill is a directory under [`skills/`](skills/) with a `SKILL.md` (plus optional `references/`, `scripts/`, or templates). [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) indexes them for Claude Code; `bunx skills` discovers the same directories directly.

## Versioning & releases

Each skill is versioned independently (SemVer in its `plugin.json`); the collection is snapshotted with git tags `vX.Y.Z` and [GitHub Releases](https://github.com/mqmalagris/agent-skills/releases). See [`CHANGELOG.md`](CHANGELOG.md) and [`VERSIONING.md`](VERSIONING.md). Manifests are validated in CI on every push and PR.

## What's in here (29 skills)

### Dev pipeline (10)

The loop I use to take a feature from vague hunch to merged code without writing fiction at any step. `dev-flow` conducts; the rest are its stages.

| Skill | What it does |
|-------|--------------|
| [`dev-flow`](skills/dev-flow/) | Conductor. Detects a task's tier (bug / feature / architecture / client), prints the exact subset of stages it will run and skip with reasons, confirms, then drives them. Matches ceremony to stakes. |
| [`grill-me`](skills/grill-me/) | Stress-test a plan via relentless interview; captures domain vocabulary, emits a Design Notes + Glossary block and persists it to `docs/intent/NNNN-<slug>.md`. Adapted from [mattpocock/skills](https://github.com/mattpocock/skills). |
| [`to-prd`](skills/to-prd/) | Synthesize the conversation into a PRD at `docs/prds/NNNN-<slug>.md` and publish to GitHub Issues. Adapted from [mattpocock/skills](https://github.com/mattpocock/skills). |
| [`compass`](skills/compass/) | Multi-mode software-engineering coach (architect, advisor, reviewer, refactor, legacy, explainer). Auto-writes ADRs to `docs/adr/`. |
| [`heist`](skills/heist/) | Turn a settled scope into an implementation plan at `docs/plans/NNNN-<slug>.md`: crew, sequence, getaway, payoff. Consumes PRDs + ADRs. |
| [`maestro`](skills/maestro/) | Verify plans for parallel feasibility, build a conflict graph, orchestrate agents in git worktrees (`parallel/<slug>`), run integration tests, clean up. |
| [`parallel-worktrees`](skills/parallel-worktrees/) | Plan-optional counterpart to maestro: go/no-go, file partitioning, isolation mechanism, integration + cleanup for ad-hoc parallel work. |
| [`pr-craft`](skills/pr-craft/) | Open a PR with a structured body (Problem / Root cause / Fix / Test / Out of scope). Drives branch → commit → push → `gh pr create`, and opens GitHub-native **stacked PRs** (one PR per dependent layer) for large, layered changes. |
| [`babysit-prs`](skills/babysit-prs/) | Drive a PR through review on its own loop: fetch feedback (human + bots like Copilot/Qodo/CodeRabbit), triage, fix, report per item with the commit SHA, resolve threads, push — repeating until MERGED. Never merges itself. |
| [`sentinel`](skills/sentinel/) | The Maintain stage the chain otherwise lacks. Runs on a schedule, not in a build: scans shipped work for recurring fix classes, reverts, and (where configured) prod threshold breaches, then files findings as `docs/intent/NNNN-<slug>.md` so they re-enter the chain as ordinary work. Never fixes or commits. |

### Quality & review (7)

| Skill | What it does |
|-------|--------------|
| [`review-pass`](skills/review-pass/) | Review-only entry point for a diff you already have: harvests any existing automated review, then runs `/run` → `code-review` → `implementation-review` (plus `security-audit` only on trust-boundary changes), then merges every finding into one ranked go/no-go verdict. |
| [`implementation-review`](skills/implementation-review/) | Pre-commit quality gate: seven parallel-subagent checks (plan gaps, use-case coverage, test scenarios, test philosophy, SOLID, Clean Code, security). Runs after `verify`, before commit. |
| [`testing-philosophy`](skills/testing-philosophy/) | What a good test is: behavior over implementation, the Testing Trophy, an e2e floor for user-facing features. Stack-agnostic (TS/Rust/Go/Elixir/Python). |
| [`security-audit`](skills/security-audit/) | High-confidence security review of a diff, layered on `wstg-security-testing`. Confidence gate, false-positive precedents, WSTG-ID mapping, dependency audit. Deliberately diff-scoped: repo-wide and posture audits route to `wstg-security-testing` mode 2, whose precedents don't suppress absence-shaped findings. |
| [`semver`](skills/semver/) | Decide the SemVer bump for a change (major/minor/patch): analyze the diff against the public surface, run the ecosystem's breaking-change detector, then apply. Stack-agnostic; feeds `publish-skill` / `release.py`. |
| [`code-craft`](skills/code-craft/) | Language- and framework-specific idioms; reader and reviewer modes. 7 languages + 12 frameworks. Tactical complement to `compass`. |
| [`wstg-security-testing`](skills/wstg-security-testing/) | OWASP WSTG web-security testing: 12 categories, ~109 test cases, four modes. Mode 2 is the whole-codebase audit and carries a systematic protocol — stack detection, route-handler enumeration, tenant-isolation and secret sweeps, frontend-gate cross-referencing, evidence-backed strengths. Methodology from [OWASP/wstg](https://github.com/OWASP/wstg). Authorized/defensive use only. |

### Reporting (2)

| Skill | What it does |
|-------|--------------|
| [`audit-report`](skills/audit-report/) | Renders audit findings (JSON in) as a designed A4 PDF — cover, severity donut, category bars, colored severity chips, evidence-backed strengths, prioritized recommendations, and copy-ready GitHub issue blocks. English default with a pt-BR pack; self-verifying and leaves a re-runnable generator script beside the report. |
| [`commit-report`](skills/commit-report/) | Work report in two modes — `quick` (git-only: prose + bullets from the current repo) and `standup` (multi-source: GitHub PRs/reviews/comments, git across repos, deploys) — tunable to audience (dev / pm / client), delivered as a copy-ready channel block or a `--doc` file. |

### Career (4)

| Skill | What it does |
|-------|--------------|
| [`periscope`](skills/periscope/) | Role-play a senior / staff / principal engineer and sweep the surfaces you declare for tech, product and org opportunities. At most 5 ranked openings, each with a concrete first move and a draft. Read-only until you approve one specific message. Feeds `brag-doc`. |
| [`cv-craft`](skills/cv-craft/) | Maintain a canonical master CV and produce tailored, ATS-friendly resumes + recruiter-screen prep from job descriptions. |
| [`portfolio-sync`](skills/portfolio-sync/) | Sync the current project into a central project-portfolio archive. `cv-craft` reads it as source of truth. |
| [`brag-doc`](skills/brag-doc/) | Maintain a monthly brag document and roll it up into a promo packet, self-review, or CV material. Reads `periscope`'s contribution log so influence work with no commit behind it still counts. Feeds `cv-craft`. |

### Product (1)

| Skill | What it does |
|-------|--------------|
| [`cagan-check`](skills/cagan-check/) | Apply Marty Cagan (SVPG) + Teresa Torres Continuous Discovery to a dev's workflow. Flags feature-factory smells; green/yellow/red per dimension. |

### Meta (3)

| Skill | What it does |
|-------|--------------|
| [`llm-wiki`](skills/llm-wiki/) | Build and maintain an interlinked Markdown knowledge base distilled from curated sources (Karpathy's LLM Wiki pattern). Three operations: ingest, query, lint. Path-agnostic — you pick where the wiki lives. |
| [`write-a-skill`](skills/write-a-skill/) | Create new skills with proper structure, progressive disclosure, and bundled resources. |
| [`publish-skill`](skills/publish-skill/) | Publish one of my own skills to this repo: copies it under `skills/<name>/`, mints its `plugin.json`, upserts `marketplace.json`, bumps its SemVer, and opens a CI-gated PR. Idempotent. |

### Marketing (2)

| Skill | What it does |
|-------|--------------|
| [`aso-craft`](skills/aso-craft/) | App Store Optimization for iOS and Android from one per-locale Markdown source: free live-store keyword probing, per-surface assignment, and a listing linter (limits, coverage gaps, wasted keyword budget, stuffing). |
| [`seo`](skills/seo/) | Deterministic LLM-first SEO audits for sites, posts, and repos. Adapted from [Bhanunamikaze/Agentic-SEO-Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill) (originally AgriciDaniel/claude-seo). |

## Attribution & license

MIT ([`LICENSE`](LICENSE)). Adapted skills credit their upstream in the table above and in each skill's `SKILL.md`; the rest are my own. Third-party skills I use but don't include here: [`THIRD_PARTY.md`](THIRD_PARTY.md).
