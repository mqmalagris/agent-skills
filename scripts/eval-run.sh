#!/usr/bin/env bash
# Run one skill's eval suite on the caller's own Claude login.
#
#   scripts/eval-run.sh <skill> [--record] [--runs N] [--baseline]
#
#   --record    append the result to evals-history/<skill>.jsonl (committed:
#               that file is the trend over time)
#   --runs N    runs per case (default $EVAL_RUNS, else 1)
#   --baseline  also run the no-skill arm and report the delta (2x the runs)
#
# Exit 0 when every runnable case scores >= 0.8, 1 otherwise.
# Cases tagged `needs-bash` grant the agent Bash, which the eval runner only
# allows where an OS sandbox exists (Linux, macOS, WSL2); on native Windows
# they are skipped and listed, and the record says which were skipped.

set -uo pipefail

root=$(git rev-parse --show-toplevel) || exit 2
cd "$root" || exit 2

skill=${1:?usage: scripts/eval-run.sh <skill> [--record] [--runs N] [--baseline]}
shift
record=0
runs=${EVAL_RUNS:-1}
ablation=none
while [ $# -gt 0 ]; do
  case $1 in
    --record)   record=1 ;;
    --runs)     runs=$2; shift ;;
    --baseline) ablation=with-without ;;
    *) echo "eval-run: unknown option $1" >&2; exit 2 ;;
  esac
  shift
done

[ -d "skills/$skill/evals" ] || { echo "eval-run: $skill has no evals/, nothing to run"; exit 0; }

# python 3 (this repo's Windows machines may have python 2 first on PATH)
PY=""
for c in python3 python "py -3"; do
  if $c -c 'import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)' >/dev/null 2>&1; then PY=$c; break; fi
done
[ -n "$PY" ] || { echo "eval-run: python 3 not found" >&2; exit 2; }

case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) sandbox=0 ;; *) sandbox=1 ;; esac

# Content hash of the skill as it will be committed (.gitignore'd results
# excluded). The pre-push hook compares this against the pushed tree to know
# a recorded run already covers exactly this content.
tmpidx=$(mktemp)
cp "$(git rev-parse --git-dir)/index" "$tmpidx" 2>/dev/null || : > "$tmpidx"
GIT_INDEX_FILE=$tmpidx git add "skills/$skill" >/dev/null 2>&1
tree=$(GIT_INDEX_FILE=$tmpidx git write-tree --prefix="skills/$skill/")
rm -f "$tmpidx"

stamp=$(date -u +%Y%m%dT%H%M%SZ)
out="skills/$skill/evals/results/_run-$stamp"
mkdir -p "$out"

cases=()
skipped=()
for p in skills/"$skill"/evals/*/prompt.md; do
  [ -f "$p" ] || continue
  if grep -qE '^tags:.*needs-bash' "$p" && [ "$sandbox" = 0 ]; then
    skipped+=("$(basename "$(dirname "$p")")")
  else
    cases+=("$p")
  fi
done

echo "eval-run: $skill  ${#cases[@]} case(s) x ${runs} run(s)  ablation=$ablation  tree=${tree:0:7}"

run_case() {
  local p=$1 runs=$2 ablation=$3 sandbox=$4 out=$5
  local name; name=$(basename "$(dirname "$p")")
  local tools=(Write)
  [ "$sandbox" = 1 ] && tools+=(Bash)
  # --scaffold: fixture scripts are this repo's own code.
  if claude plugin eval "$p" --runs "$runs" --ablation "$ablation" --no-publish --trust-plugin \
       --threshold 0.8 --scaffold --allow-tools "${tools[@]}" --json "$out/$name.json" \
       >"$out/$name.log" 2>&1; then
    echo "  pass  $name"
  else
    echo "  FAIL  $name   (log: $out/$name.log)"
    return 1
  fi
}
export -f run_case

status=0
if [ "${#cases[@]}" -gt 0 ]; then
  printf '%s\n' "${cases[@]}" |
    xargs -P 4 -I{} bash -c 'run_case "$@"' _ {} "$runs" "$ablation" "$sandbox" "$out" || status=1
fi
for c in "${skipped[@]}"; do
  echo "  skip  $c   (needs-bash: no OS sandbox on native Windows; run under WSL2/Linux)"
done

if [ "$record" = 1 ] && [ "${#cases[@]}" -gt 0 ]; then
  mkdir -p evals-history
  $PY scripts/eval_history.py record --skill "$skill" --tree "$tree" --runs "$runs" \
    --ablation "$ablation" --skipped "${skipped[*]:-}" --out "evals-history/$skill.jsonl" "$out"/*.json \
    && echo "eval-run: recorded -> evals-history/$skill.jsonl"
fi

exit $status
