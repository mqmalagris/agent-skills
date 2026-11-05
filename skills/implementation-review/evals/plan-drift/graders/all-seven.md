---
# one subagent still runs every check: Check 1 through Check 7 in order, as "Check N" lines or "N ·" table rows
type: regex
pattern: '(?:check\W{0,3}1\b|\b1 ?·)[\s\S]*?(?:check\W{0,3}2\b|\b2 ?·)[\s\S]*?(?:check\W{0,3}3\b|\b3 ?·)[\s\S]*?(?:check\W{0,3}4\b|\b4 ?·)[\s\S]*?(?:check\W{0,3}5\b|\b5 ?·)[\s\S]*?(?:check\W{0,3}6\b|\b6 ?·)[\s\S]*?(?:check\W{0,3}7\b|\b7 ?·)'
flags: i
target: last_message
---
