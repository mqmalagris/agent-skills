---
# the report names seven subagents with the staged diff's real size, 4 files and 74 lines (numstat 25+9+1+17+22, both columns); the number may sit on either side of the size
type: regex
pattern: 'subagents\W{0,6}7\W{1,6}4 files?\W{1,6}(and )?74 (changed )?lines?|\b(seven|7) ((?!checks?\b)[a-z-]+ ){0,2}(sub)?(agents?|reviewers?)\b[^\n]{0,40}?\b4 files?\W{1,6}(and )?74 (changed )?lines?|\b4 files?\W{1,6}(and )?74 (changed )?lines?[^\n]{0,40}?\b(seven|7) ((?!checks?\b)[a-z-]+ ){0,2}(sub)?(agents?|reviewers?)\b'
flags: i
target: last_message
---
