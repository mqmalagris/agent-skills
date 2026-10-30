---
# AC rule lines carry a Trophy tier (presence; the llm graders judge each rule)
type: regex
pattern: 'AC-\d+\**[^\n]*\((integration|e2e|unit)\)'
flags: i
target: { source: file, path: docs/plans/0001-saved-carts.md }
---
