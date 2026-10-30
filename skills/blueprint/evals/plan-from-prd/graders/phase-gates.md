---
# phases gate on AC ids
type: regex
pattern: '### Phase[\s\S]*Done when[^\n]*AC-\d'
flags: i
target: { source: file, path: docs/plans/0001-saved-carts.md }
---
