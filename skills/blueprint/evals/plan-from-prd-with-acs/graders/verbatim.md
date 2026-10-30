---
type: llm
focus: { source: file, path: docs/plans/0001-saved-carts.md }
---

The approved saved-carts PRD carries AC-1 to AC-4, each a one-line rule with lettered Given/When/Then examples, none marked (proposed).
PASS if ALL hold: (1) the plan's Acceptance Criteria list AC-1 to AC-4 with the PRD's rule wording unchanged and their examples carried over; (2) every rule names a test tier; (3) no rule is marked (proposed) and no open question asks the user to approve the ACs; (4) counter-examples such as cancelling the confirm prompt or a save refused at the limit are not tagged e2e (one or two critical happy-path examples may be).
FAIL if a rule is reworded, renumbered or dropped, a rule has no tier, the plan re-asks for approval, or a counter-example is pushed to e2e.
