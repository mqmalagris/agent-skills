---
name: to-prd
description: Turn the current conversation context into a PRD and publish it to GitHub Issues, also persisting it to docs/prds/NNNN-<slug>.md for downstream skills (heist, maestro). Use when user wants to create a PRD from the current context. Triggers on /to-prd, "write a PRD", "draft a PRD", "spec this out", "feature spec", or after /grill-me when scope and Glossary are settled.
---

This skill takes the current conversation context and codebase understanding and produces a PRD. Do NOT interview the user — just synthesize what you already know. If context is too thin to synthesize, halt and tell the user to run `/grill-me` first; don't fabricate scope.

## Process

1. **Read the codebase.** Explore the repo to understand current state if you haven't already. Use the project's domain glossary throughout the PRD.

2. **Scan `docs/adr/`** for accepted ADRs touching the area. List relevant ones in a `Sources` line and respect their locked decisions. If the PRD's scope would violate an ADR, surface the conflict to the user before writing.

3. **Pick the Glossary source** (in priority order):
   1. Glossary block emitted by a prior `/grill-me` session in the conversation.
   2. Domain terms already used in the codebase — search for prominent nouns/verbs in module names, types, and route names.
   3. Terms surfaced in the conversation context.

4. **Sketch the major modules** to build or modify. Actively look for opportunities to extract deep modules — ones that encapsulate substantial functionality behind a simple, testable, slow-to-change interface (Ousterhout). Do not interview; synthesize from context. If module shape is unclear, halt and route back to `/grill-me`.

5. **Write the PRD** to two destinations:
   - **Disk**: `docs/prds/NNNN-<slug>.md` (zero-padded, next available index). Create dir if missing. This is what `heist` and `maestro` consume.
   - **Tracker**: `gh issue create --title "<title>" --body-file docs/prds/NNNN-<slug>.md --label needs-triage` (use the `needs-triage` label if the repo has it; otherwise drop the flag and warn the user). If `gh` is not configured for this repo or the repo isn't on GitHub, skip the tracker step and tell the user the file is on disk only.

## PRD template

<prd-template>

# PRD: <Feature title>

- **Status**: draft | accepted | shipped
- **Date**: YYYY-MM-DD
- **Sources**: <links to relevant ADRs in docs/adr/, prior issues, related PRDs>

## Problem Statement

The problem the user is facing, from the user's perspective.

## Glossary

Ubiquitous language for this feature — terms used identically by the business, the PRD, and the code. 5-15 entries, one line each.

```
Term — short definition. (aliases: <other names if any>)
```

Omit only if the feature is genuinely vocabulary-free (pure infra refactor, perf tuning).

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A long, numbered list. Format:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Extensive — cover all aspects of the feature.

## Implementation Decisions

- Modules to build/modify
- Interfaces to be modified
- Technical clarifications
- Architectural decisions (link to ADRs where relevant)
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets — they rot fast.

## Testing Decisions

- What makes a good test here (test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (similar test types in the codebase)

## Out of Scope

What's explicitly NOT in this PRD.

## Further Notes

Anything else.

</prd-template>

## Rules

- **No interviewing.** Pure synthesis. Halt to `/grill-me` if context is too thin.
- **Glossary is load-bearing.** Heist and the implementing code must use the same terms verbatim.
- **Respect ADRs.** Locked architectural decisions are inputs, not topics to relitigate.
- **Update existing PRD** if user says "update the PRD" — find by slug. Edit-safe sections: `Status`, `Further Notes`, adding new `User Stories` or `Implementation Decisions` entries, expanding `Out of Scope`. Locked sections (require explicit user OK): `Problem Statement`, `Solution`, `Glossary`, `Sources`. Never silently drop user stories — mark as `(removed: <reason>)` instead.

## When to skip to-prd

- Bug fix (just fix it; commit message is enough).
- Single-file change.
- Spike/throwaway.
- PRD already exists and feature scope hasn't changed.
- Pure refactor with no user-visible change (use an ADR via `/compass` instead).

## Pipeline placement

`grill-me → to-prd → compass → heist → maestro → code`

- **grill-me** extracts scope, design-tree decisions, and Glossary via interview.
- **to-prd** (this skill) synthesizes the above into a PRD on disk + tracker.
- **compass** locks architectural decisions in ADRs (auto-written to `docs/adr/`).
- **heist** consumes PRD + ADRs, produces implementation plan at `docs/plans/NNNN-<slug>.md`.
- **maestro** verifies parallel feasibility across N plans, orchestrates agents in git worktrees.
- **code** — user or agent implements one phase at a time.

Skip earlier stages when the artifact already exists. If grill-me hasn't run and the conversation lacks scope clarity, halt and route there instead of synthesizing fiction.
