#!/usr/bin/env python3
"""Cut a collection release for agent-skills, in two steps.

  prepare  validate, bump the collection version, roll CHANGELOG [Unreleased]
           into it, and force-push that as one commit on release/vX.Y.Z, cut
           from origin/main. --pr opens the release PR (or updates its body)
           and closes any other open release/* PR.
  publish  if the collection version of a commit on origin/main has no
           release yet, tag it vX.Y.Z and create the GitHub Release from that
           version's CHANGELOG section. Safe to re-run; pushes only a tag.

Neither step pushes main, and neither touches the working tree. CI runs both
(.github/workflows/release.yml); locally they are the fallback:

  python3 scripts/release.py prepare --bump minor --pr
  python3 scripts/release.py prepare --bump patch --dry-run
  python3 scripts/release.py publish
"""
import argparse, datetime, json, os, re, subprocess, sys, tempfile
from pathlib import Path

# CHANGELOG entries carry σ, arrows and dashes; a cp1252 console (the Windows
# default) raises UnicodeEncodeError when the notes are printed.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
MARKETPLACE = ".claude-plugin/marketplace.json"
CHANGELOG = "CHANGELOG.md"
RELEASE_BRANCH = "release/v"


def run(cmd, check=True, capture=True, env=None, stdin=None):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=capture, env=env, input=stdin,
                       encoding=None if isinstance(stdin, bytes) else "utf-8")
    if check and r.returncode:
        out = r.stdout.decode() if isinstance(r.stdout, bytes) else (r.stdout or "")
        err = r.stderr.decode() if isinstance(r.stderr, bytes) else (r.stderr or "")
        sys.exit(f"! `{' '.join(cmd)}` failed:\n{out}{err}")
    return r


def semver(v):
    m = SEMVER.match(v)
    if not m:
        sys.exit(f"! bad version {v}")
    return tuple(int(x) for x in m.groups())


def bump(v, part):
    M, m, p = semver(v)
    return {"major": f"{M+1}.0.0", "minor": f"{M}.{m+1}.0", "patch": f"{M}.{m}.{p+1}"}[part]


def show(rev, path):
    return run(["git", "show", f"{rev}:{path}"]).stdout


def section_re(heading):
    return re.compile(rf"##\s*\[{re.escape(heading)}\][^\n]*\n(.*?)(?=\n##\s*\[|\Z)", re.S)


def remote_tags():
    out = run(["git", "ls-remote", "--tags", "--refs", "origin"]).stdout
    return {line.split("refs/tags/", 1)[1] for line in out.splitlines() if "refs/tags/" in line}


def write_temp(directory, name, text):
    path = Path(directory) / name
    path.write_text(text + "\n", encoding="utf-8", newline="\n")
    return str(path)


def commit_on(base, files, message):
    """One commit on top of `base` with `files` replaced. Built in a scratch
    index, so the working tree and the real index are never touched."""
    with tempfile.TemporaryDirectory() as d:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(d) / "index")}
        run(["git", "read-tree", base], env=env)
        for path, text in files.items():
            # bytes, so Windows text mode can't turn the blob's LF into CRLF
            blob = run(["git", "hash-object", "-w", "--stdin"], stdin=text.encode("utf-8")).stdout.decode().strip()
            run(["git", "update-index", "--add", "--cacheinfo", f"100644,{blob},{path}"], env=env)
        tree = run(["git", "write-tree"], env=env).stdout.strip()
    return run(["git", "commit-tree", tree, "-p", base, "-m", message]).stdout.strip()


def prepare(args):
    run([sys.executable, str(ROOT / "scripts" / "validate_repo.py")], capture=False)
    run(["git", "fetch", "-q", "origin", "main"])
    base = run(["git", "rev-parse", "origin/main"]).stdout.strip()
    mp = json.loads(show(base, MARKETPLACE))
    cur = mp["metadata"]["version"]
    new = args.version or bump(cur, args.bump)
    semver(new)
    date = args.date or datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    tag, branch = f"v{new}", f"{RELEASE_BRANCH}{new}"

    cl = show(base, CHANGELOG)
    m = section_re("Unreleased").search(cl)
    if not m:
        sys.exit(f"! {CHANGELOG} has no [Unreleased] section")
    notes = m.group(1).strip()
    if not notes:
        sys.exit("! [Unreleased] is empty; nothing to release")
    rolled = cl[:m.start()] + f"## [Unreleased]\n\n## [{new}] - {date}\n\n{notes}\n" + cl[m.end():]
    mp["metadata"]["version"] = new

    print(f"release {tag} ({cur} -> {new}) on {date}, from origin/main {base[:7]}")
    print("--- notes ---"); print(notes); print("---")
    if args.dry_run:
        print("dry-run: nothing written or pushed.")
        return

    commit = commit_on(base, {MARKETPLACE: json.dumps(mp, indent=2) + "\n", CHANGELOG: rolled}, f"release {tag}")
    run(["git", "push", "-q", "--force", "origin", f"{commit}:refs/heads/{branch}"])
    print(f"pushed {branch} at {commit[:7]}")
    if args.pr:
        open_release_pr(branch, tag, notes)
    if args.dispatch_validate:
        # A PR opened with the Actions token triggers no workflows; a dispatch
        # is the exception, and it puts the required check on the PR's head.
        run(["gh", "workflow", "run", "validate.yml", "--ref", branch])
        print(f"dispatched validate on {branch}")


def open_release_pr(branch, tag, notes):
    prs = json.loads(run(["gh", "pr", "list", "--state", "open", "--json", "number,headRefName",
                          "--limit", "100"]).stdout or "[]")
    mine = None
    for pr in prs:
        head = pr["headRefName"]
        if head == branch:
            mine = pr["number"]
        elif head.startswith(RELEASE_BRANCH):
            run(["gh", "pr", "close", str(pr["number"]), "--comment", f"Replaced by {branch}."])
            run(["git", "push", "-q", "origin", "--delete", head], check=False)
            print(f"closed #{pr['number']} and deleted {head}")
    with tempfile.TemporaryDirectory() as d:
        body = write_temp(d, "body.md", notes)
        if mine:
            run(["gh", "pr", "edit", str(mine), "--body-file", body])
            print(f"updated release PR #{mine}")
            return
        r = run(["gh", "pr", "create", "--base", "main", "--head", branch, "--title", f"release {tag}",
                 "--body-file", body], check=False)
    if r.returncode:
        sys.exit("! gh pr create failed. From CI, check the repo setting \"Allow GitHub Actions to create and "
                 f"approve pull requests\" (Settings, Actions, General).\n{r.stdout}{r.stderr}")
    print(f"opened {r.stdout.strip()}")


def publish(args):
    run(["git", "fetch", "-q", "origin", "main"])
    sha = run(["git", "rev-parse", f"{args.ref}^{{commit}}"]).stdout.strip()
    if run(["git", "merge-base", "--is-ancestor", sha, "origin/main"], check=False).returncode:
        sys.exit(f"! {args.ref} ({sha[:7]}) is not on origin/main; publish only tags commits that are")
    version = json.loads(show(sha, MARKETPLACE))["metadata"]["version"]
    semver(version)
    tag = f"v{version}"
    tags = remote_tags()
    has_tag = tag in tags
    has_release = has_tag and run(["gh", "release", "view", tag, "--json", "tagName"], check=False).returncode == 0
    if has_tag and has_release:
        print(f"{tag} is already tagged and released; nothing to do.")
        return
    if not has_tag:
        released = [t[1:] for t in tags if t.startswith("v") and SEMVER.match(t[1:])]
        latest = max(released, key=semver, default=None)
        if latest and semver(version) < semver(latest):
            sys.exit(f"! collection version {version} is below the latest tag v{latest}; refusing to tag it")
    m = section_re(version).search(show(sha, CHANGELOG))
    notes = m.group(1).strip() if m else ""
    if not notes:
        sys.exit(f"! {CHANGELOG} at {sha[:7]} has no [{version}] section; refusing to release {tag}")

    print(f"publish {tag} at {sha[:7]}" + (" (tag exists; creating the missing Release)" if has_tag else ""))
    if args.dry_run:
        print("--- notes ---"); print(notes); print("---")
        print("dry-run: no tag pushed, no Release created.")
        return
    if not has_tag:
        run(["git", "tag", "-a", tag, sha, "-m", f"agent-skills {tag}"])
        run(["git", "push", "-q", "origin", f"refs/tags/{tag}"])
    with tempfile.TemporaryDirectory() as d:
        run(["gh", "release", "create", tag, "--title", tag, "--notes-file", write_temp(d, "notes.md", notes),
             "--verify-tag"])
    print(f"OK released {tag}")


def main():
    ap = argparse.ArgumentParser(description="Cut a collection release: prepare a release PR, then publish it")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare", help="bump and roll the changelog on release/vX.Y.Z; --pr opens the release PR")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--version", help="explicit new collection version X.Y.Z")
    g.add_argument("--bump", choices=["major", "minor", "patch"])
    p.add_argument("--date", help="release date YYYY-MM-DD (default: today, UTC)")
    p.add_argument("--pr", action="store_true", help="open the release PR or update its body; close other release/* PRs")
    p.add_argument("--dispatch-validate", action="store_true",
                   help="run validate.yml on the release branch (needed when the Actions token opened the PR)")
    p.add_argument("--dry-run", action="store_true", help="print the version and notes; write and push nothing")
    q = sub.add_parser("publish", help="tag vX.Y.Z and create the GitHub Release if the collection version has none")
    q.add_argument("--ref", default="HEAD", help="commit to publish; must be on origin/main (default: HEAD)")
    q.add_argument("--dry-run", action="store_true", help="check and print; push no tag, create no Release")
    args = ap.parse_args()
    prepare(args) if args.cmd == "prepare" else publish(args)


if __name__ == "__main__":
    main()
