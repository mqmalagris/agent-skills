---
description: "A staged diff over the small-diff limit (4 files, 74 lines) fans out to seven subagents, reports that count, and flags AC-2 as having no API-level test."
tags: [implementation-review, git, expensive, needs-bash]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Bash, Agent]
append_system_prompt: "There is no GitHub PR and no remote in this sandbox. Review the staged change and report findings; do not commit anything."
---

Am I done? Check the staged change against the plan before I commit.
