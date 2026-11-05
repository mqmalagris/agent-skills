---
# the report names one subagent with the staged diff's real size, 1 file and 2 lines (numstat 1 1); the number may sit on either side of the size
type: regex
pattern: 'subagents\W{0,6}1\W{1,6}1 files?\W{1,6}(and )?2 (changed )?lines?|\b(one|1) ((?!checks?\b)[a-z-]+ ){0,2}(sub)?(agents?|reviewers?)\b[^\n]{0,40}?\b1 files?\W{1,6}(and )?2 (changed )?lines?|\b1 files?\W{1,6}(and )?2 (changed )?lines?[^\n]{0,40}?\b(one|1) ((?!checks?\b)[a-z-]+ ){0,2}(sub)?(agents?|reviewers?)\b'
flags: i
target: last_message
---
