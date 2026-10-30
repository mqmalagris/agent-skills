# PRD template

Fill the block between the `<prd-template>` tags. Drop the tags from the final file written to `docs/prds/`.

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

## Acceptance Examples

The rules each user story must obey, with key examples per rule in Given/When/Then. Number rules `AC-1`, `AC-2`, ... across the whole PRD and letter their examples. Blueprint copies this section verbatim into the plan and the tests carry the ids, the same way Glossary terms travel.

- Group by story. A rule is one line. Examples follow `testing-philosophy`'s scenario rules: Glossary terms, real-looking data, and what the actor observes rather than how a UI is driven. For an API whose user is a developer, the response is the observable outcome.
- Key examples, not every case: the edge-case decisions cover the rest. Five or six rules on one story is the usual sign it should be split.
- Mark a rule `(proposed)` when the agent wrote its examples rather than the user; drop the mark once the user approves the PRD.
- A criterion that isn't a behavior example (a latency budget, a reversible migration) goes after the ACs as a plain testable bullet, with no id.
- Ids are stable: never renumber, and mark a dropped rule `(removed: <reason>)`.

<acceptance-example>
### Story 3: transfer between own accounts
- **AC-4** A transfer can't take the source account below zero.
  - *a.* **Given** checking holds $50 **When** the customer transfers $80 to savings **Then** the transfer is refused as insufficient funds and checking still holds $50
  - *b.* **Given** checking holds $50 **When** the customer transfers $50 to savings **Then** checking holds $0 and savings has gained $50
</acceptance-example>

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

- What makes a good test here (test external behavior, not implementation details; see `testing-philosophy`)
- Which modules will be tested
- Prior art for the tests (similar test types in the codebase)

## Out of Scope

What's explicitly NOT in this PRD.

## Further Notes

Anything else.

</prd-template>
