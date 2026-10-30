---
description: "Does not flag an expected-value edit that follows an AC the plan already changed before this diff."
tags: [implementation-review, git, expensive, needs-bash]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash, Agent]
append_system_prompt: "There is no GitHub PR and no remote in this sandbox. Review the staged change and report findings; do not commit anything."
---

Tests are green now. Am I done? Check the staged change against the plan before I commit.
