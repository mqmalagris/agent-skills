#!/usr/bin/env python3
"""Cut a collection release for agent-skills.

Pipeline: validate -> set collection version -> roll CHANGELOG [Unreleased]
into the new version -> commit -> tag vX.Y.Z -> push main + tag -> gh release.

  python3 scripts/release.py --bump minor
  python3 scripts/release.py --version 0.4.0
  python3 scripts/release.py --bump patch --dry-run
"""
import argparse, datetime, json, re, subprocess, sys, tempfile, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def run(cmd, check=True, capture=True):
    r = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=capture)
    if check and r.returncode:
        sys.exit(f"! `{' '.join(cmd)}` failed:\n{r.stdout}{r.stderr}")
    return r


def bump(v, part):
    M, m, p = (int(x) for x in SEMVER.match(v).groups())
    return {"major": f"{M+1}.0.0", "minor": f"{M}.{m+1}.0", "patch": f"{M}.{m}.{p+1}"}[part]


def main():
    ap = argparse.ArgumentParser(description="Cut a collection release")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--version", help="explicit new collection version X.Y.Z")
    g.add_argument("--bump", choices=["major", "minor", "patch"])
    ap.add_argument("--date", default=None, help="release date YYYY-MM-DD (default: today)")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="prepare files, no commit/tag/push/release")
    args = ap.parse_args()

    # 1. validate the repo first
    run([sys.executable, str(ROOT / "scripts" / "validate_repo.py")], capture=False)

    mp_path = ROOT / ".claude-plugin" / "marketplace.json"
    mp = json.loads(mp_path.read_text(encoding="utf-8"))
    cur = mp["metadata"]["version"]
    new = args.version or bump(cur, args.bump)
    if not SEMVER.match(new):
        sys.exit(f"! bad version {new}")
    date = args.date or datetime.date.today().isoformat()
    tag = f"v{new}"

    # 2. roll CHANGELOG [Unreleased] into [new] - date
    cl_path = ROOT / "CHANGELOG.md"
    cl = cl_path.read_text(encoding="utf-8")
    m = re.search(r"##\s*\[Unreleased\]\s*\n(.*?)(?=\n##\s*\[|\Z)", cl, re.S)
    if not m:
        sys.exit("! CHANGELOG.md has no [Unreleased] section")
    notes = m.group(1).strip()
    if not notes:
        sys.exit("! [Unreleased] is empty; nothing to release")
    rolled = cl[:m.start()] + f"## [Unreleased]\n\n## [{new}] - {date}\n\n{notes}\n" + cl[m.end():]

    # 3. set collection version
    mp["metadata"]["version"] = new

    print(f"release {tag} ({cur} -> {new}) on {date}")
    print("--- notes ---"); print(notes); print("---")
    if args.dry_run:
        print("dry-run: no files written, no git.")
        return

    cl_path.write_text(rolled, encoding="utf-8")
    mp_path.write_text(json.dumps(mp, indent=2) + "\n", encoding="utf-8")

    run(["git", "add", "CHANGELOG.md", ".claude-plugin/marketplace.json"])
    run(["git", "commit", "-m", f"release {tag}"])
    run(["git", "tag", "-a", tag, "-m", f"agent-skills {tag}"])
    local_sha = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    if args.no_push:
        print(f"committed + tagged {tag} at {local_sha[:7]} (--no-push).")
        return
    run(["git", "push", "origin", "HEAD:main"])
    run(["git", "push", "origin", tag])
    remote_sha = run(["git", "ls-remote", "origin", "-h", "refs/heads/main"]).stdout.split()[0]
    if local_sha != remote_sha:
        sys.exit("! push did not land; check remote")
    fd, tmp = tempfile.mkstemp(suffix=".md", text=True)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(notes + "\n")
    run(["gh", "release", "create", tag, "--title", tag, "--notes-file", tmp,
         "--repo", "mqmalagris/agent-skills", "--verify-tag"])
    os.unlink(tmp)
    print(f"OK released {tag} -> origin/main + GitHub Release")


if __name__ == "__main__":
    main()
