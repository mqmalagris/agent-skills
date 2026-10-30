---
# the intent had no user examples, so the agent-written rules are marked proposed on the AC rule line itself
type: regex
pattern: '\*\*AC-\d+\*\*[^\n]*\(proposed\)'
flags: i
target: { source: file, path: docs/prds/0001-saved-carts.md }
---
