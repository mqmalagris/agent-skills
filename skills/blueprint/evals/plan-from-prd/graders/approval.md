---
# the PRD had no acceptance examples, so the first open question asks to approve the drafted (proposed) ACs
type: regex
pattern: '## Open Questions\s*\n+\s*- \[ \] [^\n]*(approv|confirm|sign off|sign-off)'
flags: i
target: { source: file, path: docs/plans/0001-saved-carts.md }
---
