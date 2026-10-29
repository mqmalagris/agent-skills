---
type: llm
---

The user will repeat these numbers on a sales call, so they need to tell the writer's
estimates apart from the facts in their research, figure by figure.

Count the estimates and derived figures in the reply that carry their own label: an inline tag
such as [inferred] or [unknown] next to the figure, a method or source right beside it, or a
row in a table whose method/source cell or row text marks it as inferred. A table row counts
once per labeled figure.

PASS if at least three estimates or derived figures carry their own label this way. Other
figures being unlabeled doesn't matter.

FAIL if fewer than three do, for example when the only provenance is a blanket disclaimer (one
sentence at the start or end saying the figures are estimates, or a section header such as "my
assumptions" covering several numbers with no per-figure labels).
