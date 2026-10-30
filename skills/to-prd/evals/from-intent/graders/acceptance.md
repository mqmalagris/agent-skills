---
# the PRD carries numbered acceptance examples in Given/When/Then
type: regex
pattern: '## Acceptance Examples[\s\S]*AC-1[\s\S]*\bGiven\b[\s\S]*\bWhen\b[\s\S]*\bThen\b'
target: { source: file, path: docs/prds/0001-saved-carts.md }
---
