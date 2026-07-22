# claude-skills

A curated collection of [Claude Code](https://claude.com/claude-code) skills, packaged as a plugin marketplace for one-line install. Some are mine; some are forks/adaptations of public skills — attribution noted per skill.

## What's in here

Fourteen skills, grouped by purpose:

### Dev pipeline (6)

The core loop I use to take a feature idea from "vague hunch" to "merged code" without writing fiction at any step:

| Skill | What it does |
|-------|--------------|
| [`dev-flow`](dev-flow/) | Conductor for the pipeline below. Detects a task's tier (bug / feature / architecture / client), prints the exact subset of stages it will run and skip — with reasons — confirms, then drives the sub-skills in order. Matches ceremony to stakes so a bug gets three steps and a new subsystem gets the full chain. |
| [`grill-me`](grill-me/) | Stress-test a plan or design via relentless interview. Resolves each branch of the decision tree, captures domain vocabulary, emits a Design Notes + Glossary block. Adapted from [mattpocock/skills](https://github.com/mattpocock/skills). |
| [`to-prd`](to-prd/) | Synthesize the conversation into a PRD. Writes `docs/prds/NNNN-<slug>.md` on disk and publishes to GitHub Issues via `gh issue create`. Includes a Glossary section for downstream skills. Adapted from [mattpocock/skills](https://github.com/mattpocock/skills). |
| [`compass`](compass/) | Multi-mode software engineering coach: architect, advisor, reviewer, refactor, legacy, and explainer workflows. Stack-agnostic by default. Auto-writes ADRs to `docs/adr/` when a non-trivial architectural decision settles. |
| [`heist`](heist/) | Turn a settled feature scope into an implementation plan at `docs/plans/NNNN-<slug>.md`. Crew (files touched), sequence (ordered tasks + parallel phases), getaway (rollback/risks), payoff (acceptance criteria). Consumes PRDs + ADRs. |
| [`maestro`](maestro/) | Verify plans for parallel-execution feasibility, build a conflict graph from files-touched data, orchestrate agents in git worktrees (`parallel/<slug>` branches), run integration tests, clean up. |

### Code (1)

| Skill | What it does |
|-------|--------------|
| [`code-craft`](code-craft/) | Language- and framework-specific code best practices and idioms. Reader and reviewer modes. Ships rules for **7 languages** (TypeScript, Rust, CSS/SASS, Tailwind, Dart, Go, Python) and **12 frameworks** (React, Next.js, RN+Expo, Hono, Cloudflare Workers, Astro, Svelte, Drizzle, Supabase, AWS Lambda+SAM, Terraform, Flutter). Tactical complement to `compass`. |

### Reporting (1)

| Skill | What it does |
|-------|--------------|
| [`commit-report`](commit-report/) | Dual-format commit report (prose paragraph + bullet list) from recent git activity, tunable to audience (dev / pm / client). Default scope is the current user's latest commit batch at HEAD; supports `--since`, `--last`, `--count`, `--range`, `--path` overrides. |

### Career (2)

| Skill | What it does |
|-------|--------------|
| [`cv-craft`](cv-craft/) | Maintain a canonical master CV in Markdown and produce tailored, ATS-friendly resumes plus recruiter-screen prep packs from job descriptions. Four modes: bootstrap, sync (import existing resume), tailor (match JD), screen-prep. |
| [`portfolio-sync`](portfolio-sync/) | Sync the current project into a central project-portfolio Markdown archive — every project worked on, with stack, role, and scope. `cv-craft` reads this as a source of truth. |

### Writing (2)

| Skill | What it does |
|-------|--------------|
| [`write-with-ai`](write-with-ai/) | Online-content writing: articles, newsletters, social posts, hooks, headlines, sales copy. Frameworks from Nicolas Cole and Dickie Bush's *Write With AI* library plus Maria Sukhareva's voice-preserving workflow. For Substack, LinkedIn, X/Twitter, Medium, Instagram, YouTube scripts, email, landing pages. |
| [`write-a-skill`](write-a-skill/) | Meta-skill: build new Claude Code skills with proper structure, progressive disclosure (subdirs for reference/workflows/checklists), and bundled resources. |

### SEO (1)

| Skill | What it does |
|-------|--------------|
| [`seo`](seo/) | Deterministic LLM-first SEO audits for websites, blog posts, and GitHub repositories. 16 specialized sub-skills, 10 specialist agents, 33 evidence-collector scripts. Covers technical SEO, schema, Core Web Vitals, E-E-A-T, hreflang, GEO/AEO. Adapted from [Bhanunamikaze/Agentic-SEO-Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill), originally [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo). |

### Security (1)

| Skill | What it does |
|-------|--------------|
| [`wstg-security-testing`](wstg-security-testing/) | Web application security testing via the OWASP [Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) (WSTG) — 12 categories, ~109 canonical test cases. Four modes: guide an authorized pentest, self-review your own app, build/score a coverage checklist, or review a code diff against relevant WSTG tests. Bundles a full per-category reference, detection payloads, a reporting template, and scripts to look up WSTG IDs and generate/score checklists. Methodology from [OWASP/wstg](https://github.com/OWASP/wstg). Authorized/defensive use only. |

## How I use them — the dev pipeline

The engineering-workflow skills are designed to compose into a single pipeline, with `dev-flow` as the optional conductor that picks which stages a given task actually needs:

```
dev-flow  ⟶  routes to a subset of:
grill-me  →  to-prd  →  compass  →  heist  →  maestro  →  code (+ code-craft)
```

| Stage | Artifact produced | Lives in |
|-------|-------------------|----------|
| `grill-me` | Design Notes + Glossary block | conversation only |
| `to-prd` | PRD + Glossary | `docs/prds/NNNN-<slug>.md` + GitHub Issue |
| `compass` | ADR per locked decision | `docs/adr/NNNN-<slug>.md` |
| `heist` | Implementation plan | `docs/plans/NNNN-<slug>.md` |
| `maestro` | Parallel agents in worktrees, then merge | `parallel/<slug>` branches → main |
| `code-craft` | Inside-file idiom checks | tactical, runs alongside code phase |

Each stage **consumes** the artifacts the previous stage wrote. Each can be skipped if its artifact already exists. Heist refuses to plan if architecture is unsettled and routes back to compass; to-prd refuses to synthesize fiction if context is thin and routes back to grill-me.

Real example, fresh repo:

```text
/grill-me                  # I get interrogated about a half-baked idea
/to-prd                    # PRD written to docs/prds/0001-feature.md + GH issue
/compass                   # architecture discussion, ADR(s) written to docs/adr/
/heist                     # plan written to docs/plans/0001-feature.md
/maestro                   # if multiple plans, parallel worktrees + dispatch
# ... code happens, with code-craft applied for stack idioms ...
/commit-report             # standup note from the commits
```

The other skills (`commit-report`, `cv-craft`, `portfolio-sync`, `write-with-ai`, `write-a-skill`, `seo`, `wstg-security-testing`) are independent — invoke as needed.

## Install

Add this repo as a marketplace and install the skills you want:

```text
/plugin marketplace add mqmalagris/claude-skills
/plugin install dev-flow@claude-skills
/plugin install grill-me@claude-skills
/plugin install to-prd@claude-skills
/plugin install compass@claude-skills
/plugin install heist@claude-skills
/plugin install maestro@claude-skills
/plugin install code-craft@claude-skills
/plugin install commit-report@claude-skills
/plugin install cv-craft@claude-skills
/plugin install portfolio-sync@claude-skills
/plugin install write-with-ai@claude-skills
/plugin install write-a-skill@claude-skills
/plugin install seo@claude-skills
/plugin install wstg-security-testing@claude-skills
/reload-plugins
```

Or pick à la carte. Each skill is standalone — the pipeline composition is a convention, not a hard dependency.

## Triggering

Each skill self-describes its trigger keywords in its frontmatter `description`. Claude Code auto-loads a skill when the user's request matches. Sample invocations:

```text
# Dev pipeline
/dev-flow add magic-link auth to the API
grill me on this auth design
write a PRD for the magic-link flow
/compass help me pick between layered and hexagonal here
plan this feature
/maestro can we run these three plans in parallel?

# Code
/code-craft what's the modern Rust error-handling pattern?
review this Hono route for idioms: <paste>
is forwardRef still needed in React 19?

# Reporting / career / writing
write a standup note for today
update my CV for this JD: <paste>
sync this project into my portfolio
draft a LinkedIn post about <topic>

# SEO
perform SEO audit on https://example.com
review the schema on this page

# Security
self-review this Next.js app against OWASP WSTG
build a WSTG checklist for my API
what does WSTG-INPV-05 cover?
```

You can also explicitly route: `use compass to review this PR` or `apply code-craft to this file`.

## Contributing

Issues and PRs welcome. For a new skill in this monorepo:

1. Create a top-level folder `<skill-name>/` with `SKILL.md` and supporting content. Typical layouts: `workflows/`, `topics/`, `reference/`, `checklists/` (for coaching skills); `languages/`, `frameworks/` (for reference skills); `scripts/` (for skills with evidence collectors).
2. Add a `<skill-name>/.claude-plugin/plugin.json` manifest.
3. Register the new plugin in `.claude-plugin/marketplace.json`.
4. Add an entry to the table above.
5. If the skill is forked/adapted from elsewhere, credit the source in both the plugin description and the README entry.

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgements

- [Matt Pocock](https://github.com/mattpocock) — `grill-me` and `to-prd` skills, adapted from his [skills repo](https://github.com/mattpocock/skills) (*Skills for Real Engineers, straight from my .claude directory*).
- [Bhanunamikaze](https://github.com/Bhanunamikaze) and [AgriciDaniel](https://github.com/AgriciDaniel) — the `seo` skill is adapted from [Agentic-SEO-Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill), itself based on [claude-seo](https://github.com/AgriciDaniel/claude-seo).
- [OWASP](https://owasp.org) — the `wstg-security-testing` skill encodes the methodology and test catalog from the [Web Security Testing Guide](https://github.com/OWASP/wstg) (CC BY-SA).
