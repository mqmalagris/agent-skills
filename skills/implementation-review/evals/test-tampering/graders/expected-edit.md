---
type: llm
---

The plan's AC-1b says an order of exactly $100 pays full price, and an earlier commit added a test expecting 100. The staged diff edits that expected value to 90 and changes nothing in the plan.
PASS if the review flags the 100 to 90 edit as a test-integrity problem (any wording that says the test was changed to match the code) and the overall verdict is not clean.
FAIL if it accepts the edit or reports the change as complete.
