#!/usr/bin/env python3
"""Cut a collection release for agent-skills, in two steps.

  prepare  bump the collection version on origin/main, roll CHANGELOG
           [Unreleased] into it, validate, and force-push that as one commit
           on release/vX.Y.Z. --pr opens the release PR (or updates its body),
           then closes any other open release PR from this repo and deletes
           its branch.
  publish  if the collection version of a commit on origin/main has no
           release yet, tag the first commit that has both that version and
           its CHANGELOG section vX.Y.Z, and create the GitHub Release from
           that section. Safe to re-run; pushes only a tag.

Neither step pushes main, and neither touches the working tree. CI runs both
(.github/workflows/release.yml, which sets GH_REPO); locally they are the
fallback, run from a clone whose only remote is origin (or with GH_REPO set):

  python3 scripts/release.py prepare --bump minor --pr
  python3 scripts/release.py prepare --bump patch --dry-run
  python3 scripts/release.py publish --ref origin/main
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
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MARKETPLACE = ".claude-plugin/marketplace.json"
CHANGELOG = "CHANGELOG.md"
REMOTE, BASE = "origin", "origin/main"
RELEASE_BRANCH = "release/v"
RELEASE_BRANCH_RE = re.compile(r"^release/v\d+\.\d+\.\d+$")
VALIDATE_WORKFLOW = "validate.yml"
SETTING = "Allow GitHub Actions to create and approve pull requests"


def run(cmd, check=True, capture=True, env=None, stdin=None):
    """Run a command in the repo. Text in and out, except bytes when `stdin` is bytes."""
    r = subprocess.run(cmd, cwd=ROOT, capture_output=capture, env=env, input=stdin,
                       encoding=None if isinstance(stdin, bytes) else "utf-8")
    if check and r.returncode:
        text = lambda s: s.decode(errors="replace") if isinstance(s, bytes) else (s or "")
        sys.exit(f"! `{' '.join(cmd)}` failed:\n{text(r.stdout)}{text(r.stderr)}")
    return r


def parse_semver(v):
    m = SEMVER.match(v or "")
    if not m:
        sys.exit(f"! bad version {v!r}; use X.Y.Z")
    return tuple(int(x) for x in m.groups())


def bump(v, part):
    M, m, p = parse_semver(v)
    return {"major": f"{M+1}.0.0", "minor": f"{M}.{m+1}.0", "patch": f"{M}.{m}.{p+1}"}[part]


def show(rev, path, check=True):
    r = run(["git", "show", f"{rev}:{path}"], check=check)
    return r.stdout if r.returncode == 0 else None


def version_at(rev):
    """The collection version at `rev`, or None if marketplace.json is missing or unreadable there."""
    try:
        return json.loads(show(rev, MARKETPLACE, check=False) or "")["metadata"]["version"]
    except (ValueError, KeyError, TypeError):
        return None


def section(changelog, heading):
    """(match, text) of a `## [heading]` section, ending at the next `## [` line."""
    m = re.compile(rf"^##\s*\[{re.escape(heading)}\][^\n]*(?:\n|\Z)(.*?)(?=^##\s*\[|\Z)", re.S | re.M).search(changelog or "")
    return (m, m.group(1).strip()) if m else (None, "")


def notes_at(rev, version):
    return section(show(rev, CHANGELOG, check=False), version)[1]


def remote_tags():
    """{tag: commit} on origin, with annotated tags peeled to their commit."""
    tags = {}
    for line in run(["git", "ls-remote", "--tags", REMOTE]).stdout.splitlines():
        sha, ref = line.split("\t")
        name = ref.removeprefix("refs/tags/")
        if name.endswith("^{}"):
            tags[name[:-3]] = sha
        else:
            tags.setdefault(name, sha)
    return tags


def latest_version(tags):
    released = [t[1:] for t in tags if t.startswith("v") and SEMVER.match(t[1:])]
    return max(released, key=parse_semver, default=None)


def on_main(rev):
    return run(["git", "merge-base", "--is-ancestor", rev, BASE], check=False).returncode == 0


def print_notes(notes):
    print("--- notes ---"); print(notes); print("---")


def write_temp(directory, name, text):
    path = Path(directory) / name
    path.write_text(text + "\n", encoding="utf-8", newline="\n")
    return str(path)


def validate_tree(rev):
    """Run validate_repo.py on `rev`'s exact tree, the one being released, not on the checkout."""
    with tempfile.TemporaryDirectory() as d:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(d) / "index")}
        tree = Path(d) / "tree"
        run(["git", "read-tree", rev], env=env)
        run(["git", "checkout-index", "-a", f"--prefix={tree.as_posix()}/"], env=env)
        run([sys.executable, str(tree / "scripts" / "validate_repo.py")], capture=False)


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


def next_version(args, cur, tags):
    latest = latest_version(tags)
    if latest and f"v{cur}" not in tags and parse_semver(cur) > parse_semver(latest):
        sys.exit(f"! collection version {cur} on main is not tagged yet; run "
                 f"`release.py publish --ref {BASE}` before preparing the next one")
    new = args.version if args.version is not None else bump(cur, args.bump)
    floor = max([cur] + ([latest] if latest else []), key=parse_semver)
    if parse_semver(new) <= parse_semver(floor) or f"v{new}" in tags:
        sys.exit(f"! {new} must be above the current version {cur} and the latest tag "
                 f"{'v' + latest if latest else '(none)'}, and not tagged already")
    return new


def prepare(args):
    if args.version is not None:
        parse_semver(args.version)
    if args.date is not None and not (DATE.match(args.date) and _iso_date(args.date)):
        sys.exit(f"! bad --date {args.date!r}; use YYYY-MM-DD")
    run(["git", "fetch", "-q", REMOTE, "main"])
    base = run(["git", "rev-parse", BASE]).stdout.strip()
    try:
        mp = json.loads(show(base, MARKETPLACE))
        cur = mp["metadata"]["version"]
    except (ValueError, KeyError, TypeError):
        sys.exit(f"! {MARKETPLACE} on {BASE} is unreadable; run scripts/validate_repo.py on main")
    cl = show(base, CHANGELOG)
    m, notes = section(cl, "Unreleased")
    if not m:
        sys.exit(f"! {CHANGELOG} has no [Unreleased] section")
    if not notes:
        sys.exit("! [Unreleased] is empty; nothing to release")
    new = next_version(args, cur, remote_tags())
    validate_tree(base)
    date = args.date or datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    tag, branch = f"v{new}", f"{RELEASE_BRANCH}{new}"
    rest = cl[m.end():]
    rolled = cl[:m.start()] + f"## [Unreleased]\n\n## [{new}] - {date}\n\n{notes}\n" + ("\n" + rest if rest else "")
    mp["metadata"]["version"] = new

    print(f"release {tag} ({cur} -> {new}) on {date}, from {BASE} {base[:7]}")
    print_notes(notes)
    if args.dry_run:
        print("dry-run: nothing written or pushed.")
        return

    commit = commit_on(base, {MARKETPLACE: json.dumps(mp, indent=2) + "\n", CHANGELOG: rolled}, f"release {tag}")
    run(["git", "push", "-q", "--force", REMOTE, f"{commit}:refs/heads/{branch}"])
    print(f"pushed {branch} at {commit[:7]}")
    replaced = open_or_update_release_pr(branch, tag, notes) if args.pr else []
    if args.dispatch_validate:
        # A PR opened with the Actions token triggers no workflows; a dispatch
        # is the exception, and it puts the required check on the PR's head.
        run(["gh", "workflow", "run", VALIDATE_WORKFLOW, "--ref", branch])
        print(f"dispatched {VALIDATE_WORKFLOW} on {branch}")
    close_release_prs(replaced, branch)


def _iso_date(text):
    try:
        datetime.date.fromisoformat(text)
        return True
    except ValueError:
        return False


def open_or_update_release_pr(branch, tag, notes):
    """Open the release PR or update its body; return the other open release PRs.
    Only PRs from this repo whose branch is exactly release/vX.Y.Z count, since
    a fork can name its branch anything."""
    prs = json.loads(run(["gh", "pr", "list", "--state", "open", "--limit", "500",
                          "--json", "number,headRefName,isCrossRepository"]).stdout or "[]")
    ours = [pr for pr in prs if not pr.get("isCrossRepository") and RELEASE_BRANCH_RE.match(pr["headRefName"])]
    mine = next((pr["number"] for pr in ours if pr["headRefName"] == branch), None)
    with tempfile.TemporaryDirectory() as d:
        body = write_temp(d, "body.md", notes)
        if mine:
            run(["gh", "pr", "edit", str(mine), "--body-file", body])
            print(f"updated release PR #{mine}")
        else:
            r = run(["gh", "pr", "create", "--base", "main", "--head", branch, "--title", f"release {tag}",
                     "--body-file", body], check=False)
            if r.returncode:
                gone = run(["git", "push", "-q", REMOTE, "--delete", branch], check=False).returncode == 0
                sys.exit(f"! gh pr create failed; {branch} was {'deleted again' if gone else 'left on origin'}. "
                         f"From CI, check the repo setting \"{SETTING}\" (Settings, Actions, General).\n{r.stdout}{r.stderr}")
            print(f"opened {r.stdout.strip()}")
    return [pr for pr in ours if pr["headRefName"] != branch]


def close_release_prs(prs, branch):
    """Close the replaced release PRs and delete their branches. Runs last, so a
    failure here never leaves the new release PR without its PR or check."""
    for pr in prs:
        run(["gh", "pr", "close", str(pr["number"]), "--comment", f"Replaced by {branch}."])
        gone = run(["git", "push", "-q", REMOTE, "--delete", pr["headRefName"]], check=False).returncode == 0
        print(f"closed #{pr['number']}" + (f" and deleted {pr['headRefName']}" if gone else
                                           f"; could not delete {pr['headRefName']}"))


def release_commit(sha, version):
    """The commit to tag for `version`: on sha's first-parent history, the first
    commit at or after the one that set the version whose CHANGELOG has the
    version's section. Normally that is the release PR's merge. None if no
    commit up to sha has the section."""
    start = sha
    for c in run(["git", "rev-list", "--first-parent", sha, "--", MARKETPLACE]).stdout.split():
        if version_at(c) != version:
            break
        start = c
    later = run(["git", "rev-list", "--first-parent", "--reverse", f"{start}..{sha}", "--", CHANGELOG]).stdout.split()
    return next((c for c in [start] + later if notes_at(c, version)), None)


def publish(args):
    run(["git", "fetch", "-q", REMOTE, "main"])
    ref = args.ref or "HEAD"
    sha = run(["git", "rev-parse", f"{ref}^{{commit}}"]).stdout.strip()
    if not on_main(sha):
        sys.exit(f"! {ref} ({sha[:7]}) is not on {BASE}; publish only tags commits that are")
    version = version_at(sha)
    parse_semver(version)
    tag = f"v{version}"
    tags = remote_tags()
    has_tag = tag in tags
    has_release = has_tag and run(["gh", "release", "view", tag, "--json", "tagName"], check=False).returncode == 0
    if has_tag and has_release:
        main_version = version_at(BASE)
        unreleased = main_version and main_version != version and f"v{main_version}" not in tags
        hint = f" ({BASE} holds {main_version}, not tagged yet; pass --ref {BASE} to publish it)" if unreleased else ""
        print(f"{tag} is already tagged and released; nothing to do.{hint}")
        return
    latest = latest_version(tags)
    older = bool(latest) and parse_semver(version) < parse_semver(latest)
    if has_tag:
        # finish a release whose tag got pushed but whose Release didn't, wherever
        # the tag is, as long as it is a release commit for this version on main
        target = tags[tag]
        if older and args.ref is None:
            sys.exit(f"! collection version {version} is below the latest tag v{latest}; to finish its Release, "
                     "pass --ref with the commit to publish")
        if not on_main(target) or version_at(target) != version:
            sys.exit(f"! tag {tag} points at {target[:7]}, which is not a commit on {BASE} with collection version "
                     f"{version}; fix or delete the tag")
    elif older:
        sys.exit(f"! collection version {version} is below the latest tag v{latest}; refusing to tag it")
    else:
        target = release_commit(sha, version)
        if not target:
            sys.exit(f"! {CHANGELOG} has no [{version}] section on {BASE} up to {sha[:7]}; refusing to release {tag}")
    notes = notes_at(target, version) or notes_at(sha, version)
    if not notes:
        sys.exit(f"! {CHANGELOG} has no [{version}] section at {target[:7]}; refusing to release {tag}")

    print(f"publish {tag} at {target[:7]}" + (" (tag exists; creating the missing Release)" if has_tag else ""))
    if args.dry_run:
        print_notes(notes)
        print("dry-run: no tag pushed, no Release created.")
        return
    if not has_tag:
        local = run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}^{{commit}}"], check=False).stdout.strip()
        if local and local != target:
            sys.exit(f"! a local tag {tag} points at {local[:7]}, not {target[:7]}; delete it with `git tag -d {tag}`")
        if not local:
            run(["git", "tag", "-a", tag, target, "-m", f"agent-skills {tag}"])
        run(["git", "push", "-q", REMOTE, f"refs/tags/{tag}"])
    with tempfile.TemporaryDirectory() as d:
        # an older version's Release must not become the repo's Latest
        run(["gh", "release", "create", tag, "--title", tag, "--notes-file", write_temp(d, "notes.md", notes),
             "--verify-tag"] + (["--latest=false"] if older else []))
    print(f"OK released {tag}" + (" (not marked Latest)" if older else ""))


def main():
    ap = argparse.ArgumentParser(description="Cut a collection release: prepare a release PR, then publish it")
    sub = ap.add_subparsers(dest="cmd", required=True)
    prep = sub.add_parser("prepare", help="bump and roll the changelog on release/vX.Y.Z; --pr opens the release PR")
    prep.set_defaults(func=prepare)
    g = prep.add_mutually_exclusive_group(required=True)
    g.add_argument("--version", help="explicit new collection version X.Y.Z (above the current one)")
    g.add_argument("--bump", choices=["major", "minor", "patch"])
    prep.add_argument("--date", help="release date YYYY-MM-DD (default: today, UTC)")
    prep.add_argument("--pr", action="store_true", help="open the release PR or update its body; close other release PRs")
    prep.add_argument("--dispatch-validate", action="store_true",
                      help=f"run {VALIDATE_WORKFLOW} on the release branch (needed when the Actions token opened the PR)")
    prep.add_argument("--dry-run", action="store_true", help="print the version and notes; write and push nothing")
    pub = sub.add_parser("publish", help="tag vX.Y.Z and create the GitHub Release if the collection version has none")
    pub.set_defaults(func=publish)
    pub.add_argument("--ref", help=f"commit to publish; must be on {BASE} (default: HEAD). Needed to finish "
                     "an older release whose tag went out without its Release")
    pub.add_argument("--dry-run", action="store_true", help="check and print; push no tag, create no Release")
    args = ap.parse_args()
    if not os.environ.get("GH_REPO") and len(run(["git", "remote"]).stdout.split()) > 1:
        sys.exit("! this clone has several remotes, so gh could pick the wrong repo; set GH_REPO=owner/repo "
                 "to origin's GitHub repo (CI sets it)")
    args.func(args)


if __name__ == "__main__":
    main()
