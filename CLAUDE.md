# agent-skills: rules for changes

Promoted from repeat review findings (each class seen in two separate reviews).

- A review gate must not be satisfiable by the reviewed agent's own output (a stated reason, a plan edit it committed, commit order); route anything only the agent can vouch for to the user.
- Write each eval grader so a wrong output fails it: check content, not just that a heading or keyword exists, and probe every regex against a near-miss before committing.
- When a skill reads or measures a diff, name the exact git command for the target it reviews (`--staged`, the merge-base range, untracked files), never a bare `git diff`.
- State a policy only in the skill that owns it; other skills name that skill instead of describing its behavior.
