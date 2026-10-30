---
type: llm
---

An earlier commit changed the plan's AC-1 to "$100 or more gets 10% off" with example AC-1b now expecting $90, before any code. The staged diff implements that boundary and edits the AC-1b test from 100 to 90 to match the plan.
PASS if the review explicitly addresses the AC-1b expected-value edit, ties it to the plan's AC-1 change (quoting the plan entry or its commit), and asks the user to confirm it, instead of calling it unexplained tampering.
FAIL if the review never mentions that edit, or reports it as a test-integrity defect with no reason.
