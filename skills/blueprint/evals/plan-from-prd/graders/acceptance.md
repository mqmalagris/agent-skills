---
# the plan's Acceptance Criteria are numbered rules with Given/When/Then examples
type: regex
pattern: '## Acceptance Criteria[\s\S]*AC-1[\s\S]*\bGiven\b[\s\S]*\bWhen\b[\s\S]*\bThen\b[\s\S]*## Edge Cases'
target: { source: file, path: docs/plans/0001-saved-carts.md }
---
