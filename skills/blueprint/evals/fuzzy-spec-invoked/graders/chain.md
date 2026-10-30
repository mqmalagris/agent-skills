---
type: llm
weight: 3
---

The user asked for a build plan, but no spec exists. Judge only whether the reply plans the feature and what it asks the user to answer.

PASS if the reply declines to plan because the scope is unsettled and sends the user to grill-me or to-prd.

FAIL if either of these is in the reply:
- A plan for the feature: phases, files to change, or implementation steps for building it, even one labeled a guess.
- A scoping interview: questions the user is asked to answer about the feature, decisions or constraints.

These are neither a plan nor an interview, so they never cause a FAIL: a numbered list of skills to run next (grill-me, to-prd, compass, blueprint), a summary of the code in the repo, examples of what the feature could be, pointing out that an architecture decision is open, and offering to plan from a spec the user already has.
