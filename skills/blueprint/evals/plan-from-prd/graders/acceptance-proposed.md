---
# the PRD has no acceptance examples, so the drafted rules are marked proposed on the AC rule line itself
type: regex
pattern: '\*\*AC-\d+\*\*[^\n]*\(proposed\)'
flags: i
target: { source: file, path: docs/plans/0001-saved-carts.md }
---
