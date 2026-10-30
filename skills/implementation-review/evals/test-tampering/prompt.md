---
description: "Flags an edited expected value and a test-environment branch as test-integrity blockers."
tags: [implementation-review, git, expensive, needs-bash]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash, Agent]
append_system_prompt: "There is no GitHub PR and no remote in this sandbox. Review the staged change and report findings; do not commit anything."
---

Tests are green now. Am I done? Check the staged change against the plan before I commit.
