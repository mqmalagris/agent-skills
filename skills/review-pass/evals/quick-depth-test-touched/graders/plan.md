---
type: llm
---

The reply is a review plan at quick depth for a fix to src/cart.ts whose diff also deletes a test from src/cart.test.ts.
PASS if it runs the live-run check (/run) and code-review, AND plans implementation-review restricted to its tests-only mode (Check 4: test integrity and philosophy) because the diff touches a test file, AND marks security-audit as SKIP.
FAIL if it skips implementation-review entirely, plans the full seven-check implementation-review, or plans security-audit.
