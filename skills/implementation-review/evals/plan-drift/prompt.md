---
description: "Reconciles the staged diff against the plan's Edge Cases ledger and flags the handle-but-missing case and the absent tests. The diff is 1 file and 2 lines, so one subagent runs all seven checks and the report says so."
tags: [implementation-review, git, expensive, needs-bash]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash, Agent]
append_system_prompt: "There is no GitHub PR and no remote in this sandbox. Review the staged change and report findings; do not commit anything."
---

Am I done? Check the staged change against the plan before I commit.
