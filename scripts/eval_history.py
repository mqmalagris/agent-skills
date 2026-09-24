#!/usr/bin/env python3
"""Eval trend store: one JSON line per recorded suite run, per skill.

  eval_history.py record --skill S --tree T --runs N --ablation A \
      [--skipped "a b"] --out evals-history/S.jsonl result1.json [result2.json ...]
  eval_history.py trend  [S ...]      # table of every recorded run, oldest first

The result files are `claude plugin eval --json` outputs (one per case when the
runner filters cases). Lines are written compact so the pre-push hook can grep
for `"tree":"<hash>"` and `"passed":true` without parsing JSON.
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

THRESHOLD = 0.8
ROOT = Path(__file__).resolve().parent.parent


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def record(a):
    cases, claude, started = {}, None, None
    for f in a.results:
        r = json.loads(Path(f).read_text(encoding="utf-8"))
        claude = claude or r.get("claudeVersion")
        started = min(filter(None, [started, r.get("startedAt")]), default=None)
        for c in r.get("cases", []):
            w = [x["score"] for x in c["arms"].get("with", [])]
            o = [x["score"] for x in c["arms"].get("without", [])]
            errs = sum(1 for x in c["arms"].get("with", []) if x.get("error"))
            cases[c["name"]] = {
                "with": round(mean(w), 3) if w else None,
                "without": round(mean(o), 3) if o else None,
                **({"errors": errs} if errs else {}),
            }
    if not cases:
        sys.exit("eval_history: no case results found; nothing recorded")

    manifest = ROOT / "skills" / a.skill / ".claude-plugin" / "plugin.json"
    version = json.loads(manifest.read_text(encoding="utf-8")).get("version") if manifest.exists() else None
    withs = [c["with"] for c in cases.values() if c["with"] is not None]
    deltas = [c["with"] - c["without"] for c in cases.values()
              if c["with"] is not None and c["without"] is not None]
    line = {
        "date": (started or dt.datetime.now(dt.timezone.utc).isoformat())[:19] + "Z",
        "skill": a.skill,
        "version": version,
        "tree": a.tree,
        "claude": claude,
        "platform": sys.platform,
        "runs": a.runs,
        "ablation": a.ablation,
        "cases": dict(sorted(cases.items())),
        "skipped": sorted(a.skipped.split()) if a.skipped else [],
        "mean_with": round(mean(withs), 3) if withs else None,
        "mean_delta": round(mean(deltas), 3) if deltas else None,
        "passed": all(w >= THRESHOLD for w in withs),
    }
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(line, separators=(",", ":"), ensure_ascii=False) + "\n")


def trend(a):
    files = [ROOT / "evals-history" / f"{s}.jsonl" for s in a.skills] if a.skills \
        else sorted((ROOT / "evals-history").glob("*.jsonl"))
    for f in files:
        if not f.exists():
            print(f"{f.stem}: no history")
            continue
        rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        print(f"\n{f.stem}  ({len(rows)} recorded run(s))")
        print(f"  {'date':<20} {'version':<8} {'tree':<8} {'runs':>4} {'with':>5} {'delta':>6}  pass  cases below {THRESHOLD}")
        for r in rows:
            low = [k for k, v in r["cases"].items() if v["with"] is not None and v["with"] < THRESHOLD]
            d = "" if r["mean_delta"] is None else f"{r['mean_delta']:+.2f}"
            skip = f"  (+{len(r['skipped'])} skipped)" if r.get("skipped") else ""
            print(f"  {r['date']:<20} {str(r['version']):<8} {r['tree'][:7]:<8} {r['runs']:>4} "
                  f"{r['mean_with']:>5.2f} {d:>6}  {'yes' if r['passed'] else 'NO ':<4}  {', '.join(low) or '-'}{skip}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("--skill", required=True)
    r.add_argument("--tree", required=True)
    r.add_argument("--runs", type=int, required=True)
    r.add_argument("--ablation", required=True)
    r.add_argument("--skipped", default="")
    r.add_argument("--out", required=True)
    r.add_argument("results", nargs="+")
    t = sub.add_parser("trend")
    t.add_argument("skills", nargs="*")
    a = ap.parse_args()
    record(a) if a.cmd == "record" else trend(a)


if __name__ == "__main__":
    main()
