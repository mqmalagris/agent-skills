# Eval history

One JSON line per recorded eval run, one file per skill. This is the trend: whether a skill got better or worse across versions, and whether it still beats the no-skill baseline.

```bash
py -3 scripts/eval_history.py trend              # every skill (python3 on Linux/macOS)
py -3 scripts/eval_history.py trend grill-me     # one skill
```

## How lines get here

- **`/publish-skill`** records one automatically before it commits: it runs the skill's suite on your Claude login and commits the line with the skill change. A suite below 0.8 aborts the publish (`--skip-evals` to override).
- **By hand:** `bash scripts/eval-run.sh <skill> --record [--runs 3] [--baseline]`, then commit the file with the change it measured.

The pre-push hook reads these files too: a skill whose pushed content (the `tree` hash) already has a passing line is not re-run.

## Reading a line

| Field | Meaning |
|---|---|
| `tree` | git tree hash of `skills/<name>/` as committed, so a line maps to exact content |
| `runs`, `ablation` | runs per case; `with-without` means a no-skill baseline arm ran too |
| `cases.<name>.with` / `.without` | mean score per case with and without the skill |
| `mean_delta` | what the skill adds over the bare model (only with a baseline) |
| `skipped` | `needs-bash` cases that could not run on that machine (native Windows) |

Compare like with like: a 1-run line is a smoke check, a 3-run line with a baseline is the one to quote. Scores come from runs on the recording machine's model, so `claude` (the CLI version) is recorded as well.
