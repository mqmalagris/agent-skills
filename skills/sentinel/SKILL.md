---
name: sentinel
description: Close the loop after ship — scan a repo (and optionally its live prod signal) for post-release trouble, then file what it finds as docs/intent/NNNN-<slug>.md so it re-enters the dev-flow chain as ordinary work. Detects recurring fix classes, reverts, and threshold breaches on the outcome metric a feature named at plan time. Read-only on code: it never fixes, commits, or opens a PR. Use when the user says "sentinel", "what's rotting", "post-ship check", "did anything regress", "watch this repo", "maintain scan", or runs /sentinel — and as the scheduled Maintain stage that dev-flow's chain ends without.
---

# sentinel

The chain gates correctness *at* ship and then goes blind. `review-pass` is a one-time gate, `/run` is a one-time demo, and after `pr-craft` nothing is watching. sentinel is the stage that watches, and its only output is an **intent file** — the same artifact `grill-me` writes, so a problem found in production re-enters the pipeline as ordinary planned work rather than as an interrupt.

It decides nothing about how to fix anything. It files findings; a human picks up the intent file and routes it through `/dev-flow` like any other task. That division is deliberate: the detector runs unattended, so the moment it could also *change* code it would need a level of trust no scheduled job has earned.

## Two tiers

Run tier 1 always. Add tier 2 per project, only where the signal justifies the credential.

| Tier | Source | Cost | Catches |
|---|---|---|---|
| **1 — history** | the repo's own git log | nothing | recurring fix classes, reverts, fix-rate drift |
| **2 — prod** | a live telemetry API you configure | one scoped read token per project | error-rate and latency breaches, the outcome metric a feature was supposed to move |

Tier 1 is lagging and coarse — it tells you a file keeps breaking, days or weeks after users noticed. Tier 2 is the one that catches an incident while it's happening. Neither replaces the other, and tier 1 alone is still worth scheduling because it costs nothing and needs no wiring.

## Protocol

1. **Scope** — which repo, which window. Default: current repo, last 30 days. On a multi-repo sweep, run per repo and report separately; findings don't merge across repos.
2. **Tier 1 scan** — `py -3 scripts/scan_git_signals.py --repo <path> --since "<window>"` (Windows; `python3` on POSIX). Returns JSON: `totals`, `repeat_classes`, `reverts`, `conventional_commit_coverage`.
3. **Tier 2 scan** (only if the repo appears in [config](#tier-2-config)) — query the configured source, compare against its thresholds.
4. **Triage** — apply the [filing bar](#the-filing-bar). Most runs file nothing, and that is the expected outcome, not a failure.
5. **Dedup before writing** — for each finding that clears the bar, grep `docs/intent/` for its `signature`. Found → **amend** that file (add a dated observation line, bump the count) rather than minting a new index. This is the difference between a useful log and 52 near-identical files a year.
6. **File** — write `docs/intent/NNNN-<slug>.md` per the [template](#what-it-files), path from `bash scripts/next-intent-index.sh <slug>`.
7. **Report** — one line per finding: filed / amended / considered-and-dropped. Name what was dropped and why; a detector that silently discards is one you stop trusting.

## The filing bar

A finding is worth a human's attention only if it clears all three:

- **`recurring`, and nothing else.** The scanner sorts every candidate into one of four buckets, and only the first is fileable:

  | Bucket | Meaning | File it? |
  |---|---|---|
  | `recurring` | outlier fix count for this repo, spread over 7+ days | yes |
  | `common` | repeatedly fixed, but normal wear at this repo's fix rate | no |
  | `clustered` | fixes span under 7 days — one bug being iterated in a sitting | no |
  | `expected-churn` | locale catalogs, snapshots, generated output: changing often is the job | no |

  The bar is **relative to the repo**, not an absolute count: `recurring` requires the file to sit at or above the 95th percentile of that repo's own per-file fix distribution. This matters more than it sounds. An absolute "2 fixes over 7 days" bar was silent on a 250-commit side project and flagged 57 files on a client repo doing 400 commits a month at a 40% fix share — useless in both directions. Measured against its own repo, the same scan reports zero and a readable dozen.

- **File at most 3 per run.** Even a well-calibrated scan on a busy repo surfaces a dozen candidates, and twelve new intent files is not a finding, it's a backlog nobody reads. Take the top 3 by fix count, file those, and list the rest under "observed, not filed" in the report. They will still be there next run if they matter, and the amend path means a standing problem accumulates observations in one file rather than spawning new ones.
- **Actionable.** There is something a person could decide about. "This file changes often" is not a finding; "this file has absorbed 4 fixes across 6 weeks and every one touched date parsing" is.
- **Not already filed.** See dedup above.

Any revert clears the bar on its own. A revert means something reached users broken, and the git record is unambiguous about it.

**Trust the coverage number.** The scanner reports `conventional_commit_coverage`. Below ~0.7 the tier-1 signal is close to noise, because the detector identifies fixes by their `fix:` prefix and most commits aren't declaring one. Say so in the report and don't file from tier 1 on that repo until the convention is in use.

## What it files

```markdown
# Intent: <short problem title>

- **Status**: draft
- **Date**: YYYY-MM-DD
- **Slug**: <kebab-slug>
- **Source**: sentinel (tier <1|2>, automated detection)
- **Signature**: <dedup key — the file path, or the metric name for tier 2>

## Signal
<what was detected, with the evidence: fix count, span, SHAs, subjects, or the
metric, its threshold, and the observed value. Facts only.>

## Observations
- YYYY-MM-DD — first detected: <n> fixes over <n> days
- YYYY-MM-DD — still present: now <n> fixes

## Why this might matter
<one paragraph of hypothesis, explicitly labelled as hypothesis. The detector
sees a pattern in history; it does not know the cause. Do not write this as if
the cause were established.>

## Not yet decided
- [ ] Is this a real design problem or an artifact of how the work was sequenced?
- [ ] <question a human needs to answer before this becomes work>
```

Status stays `draft` — a machine-detected intent has not been through `grill-me`, so it carries none of the scope and Glossary work a human-authored one does. Whoever picks it up runs the normal chain from the top.

## Tier 2 config

`config.json` beside this file, gitignored, one entry per repo. Absent → tier 1 only, silently.

```json
{
  "my-edge-api": {
    "source": "cloudflare-workers",
    "account_id": "<id>",
    "script_name": "my-edge-api",
    "token_env": "CF_ANALYTICS_TOKEN",
    "thresholds": {
      "cpu_time_p99_ms": 350,
      "error_rate": 0.01
    }
  }
}
```

The token lives in the environment, never in the file — `token_env` names the variable to read. Scope it to Analytics:Read only; this skill never needs write access to anything.

**Cloudflare Workers** is the worked example because its failure mode is exactly the shape this tier exists for: module-load CPU creeps toward the startup limit as dependencies accumulate, and nothing warns you — the first symptom is a deploy failing outright with error 10021. `cpu_time_p99_ms` at 350 against a 400ms budget is the kind of threshold that turns that into a filed intent a week early instead of a broken deploy. Query the GraphQL analytics endpoint (`api.cloudflare.com/client/v4/graphql`, `workersInvocationsAdaptive` dataset, `quantiles.cpuTimeP99` + `sum.errors`). **Verify the current dataset and field names against Cloudflare's schema when you wire it** — that API's fields have moved before, and a scheduled job failing silently on a renamed field is worse than no job.

Other sources follow the same shape: a query, a threshold set, a token env var. Add them when a project earns one; don't pre-wire projects that have never had an incident.

## Scheduling

Not a `dev-flow` chain stage — it runs on a clock, not in a build. Two ways:

- **`/schedule`** — a cron routine, the right choice for an unattended weekly sweep. Weekly is a sensible default for tier 1; the signal it reads moves in weeks.
- **`/loop`** — a self-paced loop inside a session, for watching a specific rollout you just shipped.

Run it far more often than that and tier 1 has nothing new to say, because git history doesn't move fast enough to justify a daily read. Tier 2 can justify a tighter cadence when it's watching a live threshold.

## Rules

- **Never fix, never commit code, never open a PR.** File the intent and stop. The whole reason this can run unattended is that its blast radius is one Markdown file.
- **Findings are hypotheses.** The detector sees correlation in commit history. Write it as a hypothesis, and let the human who picks it up decide whether it's real.
- **Quiet is the normal result.** A run that files nothing on a healthy repo is the detector working. Tuning it until it always finds something is how it becomes noise you ignore.
- **Say what you dropped.** Every run reports considered-and-dropped findings with the reason, so the bar stays visible and adjustable.
- **One repo, one report.** Don't merge findings across repos; a pattern in one says nothing about another.
- **Obey CLAUDE.md conventions** (`rtk` prefix, no attribution trailers) — this skill writes files and reads git, both covered there.

## Pipeline placement

```
grill-me → to-prd → compass → heist → code → review-pass → pr-craft → [shipped]
    ↑                                                                      │
    └────────────────── sentinel (scheduled) ←─────────────────────────────┘
```

`dev-flow`'s "Instrument what you can't see after ship" rule is the other half of this: it forces `to-prd`/`heist` to name the outcome metric and `code` to add the telemetry. sentinel is what reads them. A feature that named no metric can still be watched by tier 1, just more coarsely.

## Humanize the written prose (if available)

Before writing the intent file, if the `humanizer` skill is installed, run it on the drafted body so the document reads naturally and free of AI tells; skip silently if unavailable. Apply to the prose sections only — never to the Signature, SHAs, file paths, metric names, or the frontmatter.
