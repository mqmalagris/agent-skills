#!/usr/bin/env python3
"""Integration tests for scripts/release.py.

Each test builds a throwaway repo with a bare `origin`, copies release.py and
validate_repo.py into it, and runs `release.py` as a subprocess, asserting what
a maintainer would see: exit code, output, and the branches, tags and files on
`origin`. `gh` is the one external boundary: a fake on PATH keeps the PRs,
Releases and workflow runs that GitHub would, so tests assert that state. Test
names carry the acceptance-criteria ids from the release-in-ci plan.

  python3 -m unittest discover -s scripts/tests -v
"""
import datetime, json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
DATE = "2026-11-05"
SETTING = "Allow GitHub Actions to create and approve pull requests"

FAKE_GH = r'''#!/usr/bin/env python3
"""Fake gh: keeps PR, Release and workflow-run state in $FAKE_GH_STATE."""
import json, os, sys
from pathlib import Path

state = Path(os.environ["FAKE_GH_STATE"])
args = sys.argv[1:]
cmd = " ".join(args[:2])
if cmd in os.environ.get("FAKE_GH_FAIL", "").split(","):
    sys.exit(f"gh {cmd}: failed (injected by the test)")
prs_path = state / "prs.json"
prs = json.loads(prs_path.read_text()) if prs_path.exists() else []


def opt(name):
    return args[args.index(name) + 1] if name in args else None


def pr(number):
    return next(p for p in prs if p["number"] == int(number))


if cmd == "pr list":
    print(json.dumps([p for p in prs if p["state"] == "open"]))
elif cmd == "pr create":
    n = max([p["number"] for p in prs], default=0) + 1
    prs.append({"number": n, "headRefName": opt("--head"), "baseRefName": opt("--base"), "title": opt("--title"),
                "body": Path(opt("--body-file")).read_text(), "state": "open", "isCrossRepository": False})
    print(f"https://github.com/example/agent-skills/pull/{n}")
elif cmd == "pr edit":
    pr(args[2])["body"] = Path(opt("--body-file")).read_text()
elif cmd == "pr close":
    pr(args[2])["state"] = "closed"
elif cmd == "release view":
    sys.exit(0 if (state / "releases" / args[2]).exists() else 1)
elif cmd == "release create":
    (state / "releases").mkdir(exist_ok=True)
    (state / "releases" / args[2]).write_text(Path(opt("--notes-file")).read_text())
    if "--latest=false" in args:
        (state / "releases" / f"{args[2]}.not-latest").touch()
elif cmd == "workflow run":
    with open(state / "workflow-runs", "a") as f:
        f.write(f"{args[2]} {opt('--ref')}\n")
prs_path.write_text(json.dumps(prs))
'''

SKILL_MD = '---\nname: demo\ndescription: "A demo skill for release tests."\n---\n\n# demo\n'


def changelog(unreleased, released):
    out = ["# Changelog", "", "## [Unreleased]"] + [f"- {e}" for e in unreleased] + [""]
    for version, entries in released:
        out += [f"## [{version}] - 2026-10-01", ""] + [f"- {e}" for e in entries] + [""]
    return "\n".join(out)


@unittest.skipIf(os.name == "nt", "the fake gh is a POSIX script; run under Linux or WSL")
class ReleaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="release-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.origin, self.repo, self.state = self.tmp / "origin.git", self.tmp / "repo", self.tmp / "gh"
        self.state.mkdir()
        bindir = self.tmp / "bin"
        bindir.mkdir()
        (bindir / "gh").write_text(FAKE_GH)
        (bindir / "gh").chmod(0o755)
        ident = {f"GIT_{who}_{what}": val for who in ("AUTHOR", "COMMITTER")
                 for what, val in (("NAME", "test"), ("EMAIL", "test@example.com"))}
        # ignore the developer's git config (signing, hooks) so the fixture behaves the same everywhere
        isolate = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
        self.env = {**os.environ, **ident, **isolate, "FAKE_GH_STATE": str(self.state),
                    "PATH": f"{bindir}{os.pathsep}{os.environ['PATH']}"}
        for name in ("PYTHONIOENCODING", "FAKE_GH_FAIL", "GH_REPO"):
            self.env.pop(name, None)
        self.run_git(["init", "-q", "--bare", "-b", "main", str(self.origin)], cwd=self.tmp)
        self.run_git(["init", "-q", "-b", "main", str(self.repo)], cwd=self.tmp)
        (self.repo / "scripts").mkdir()
        for name in ("release.py", "validate_repo.py"):
            shutil.copy(SCRIPTS / name, self.repo / "scripts" / name)
        skill = self.repo / "skills" / "demo"
        (skill / ".claude-plugin").mkdir(parents=True)
        (skill / "SKILL.md").write_text(SKILL_MD)
        (skill / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": "demo", "version": "0.1.0"}))
        self.write_main("0.14.0", ["first entry"], [("0.14.0", ["old entry"])], "init")
        self.git("remote", "add", "origin", str(self.origin))
        self.git("push", "-q", "-u", "origin", "main")
        # v0.14.0 is already tagged and released, as on the real repo
        self.tag("v0.14.0", push=True)
        self.add_release("v0.14.0")

    # --- fixture helpers ---

    def run_git(self, args, cwd=None):
        return subprocess.run(["git", *args], cwd=cwd or self.repo, env=self.env, check=True,
                              capture_output=True, text=True).stdout.strip()

    def git(self, *args):
        return self.run_git(list(args))

    def head(self):
        return self.git("rev-parse", "HEAD")

    def tag(self, name, rev="HEAD", push=False):
        self.git("tag", "-a", name, rev, "-m", name)
        if push:
            self.git("push", "-q", "origin", f"refs/tags/{name}")

    def write_main(self, version, unreleased, released, message, push=False, changelog_text=None, plugin_version="0.1.0"):
        mp = {"name": "agent-skills", "metadata": {"version": version},
              "plugins": [{"name": "demo", "source": "./skills/demo", "version": plugin_version}]}
        (self.repo / ".claude-plugin").mkdir(exist_ok=True)
        (self.repo / ".claude-plugin" / "marketplace.json").write_text(json.dumps(mp, indent=2) + "\n")
        (self.repo / "CHANGELOG.md").write_text(changelog_text or changelog(unreleased, released))
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        if push:
            self.git("push", "-q", "origin", "HEAD:main")
        return self.head()

    def released_on_main(self, version, entries):
        """What merging a release PR leaves on main: the bumped version and its section."""
        return self.write_main(version, [], [(version, entries), ("0.14.0", ["old entry"])], f"release v{version}", push=True)

    def merge_release_branch(self, version):
        """Merge origin's release branch into main with a two-parent merge commit, as GitHub's merge button does."""
        self.git("fetch", "-q", "origin")
        self.git("merge", "-q", "--no-ff", "-m", f"Merge release v{version}", f"origin/release/v{version}")
        self.git("push", "-q", "origin", "HEAD:main")
        return self.head()

    def advance_main(self, message):
        """An unrelated commit landing on main after the release, like another skill publish."""
        (self.repo / "later.txt").write_text(message + "\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        self.git("push", "-q", "origin", "HEAD:main")
        return self.head()

    def release(self, *args, **env):
        return subprocess.run([sys.executable, "scripts/release.py", *args], cwd=self.repo,
                              env={**self.env, **env}, capture_output=True, encoding="utf-8", errors="replace")

    def on_origin(self, *args):
        return self.run_git(["--git-dir", str(self.origin), *args], cwd=self.tmp)

    def origin_file(self, ref, path):
        return self.on_origin("show", f"{ref}:{path}")

    def origin_refs(self, kind):
        return set(self.on_origin("for-each-ref", "--format=%(refname:short)", f"refs/{kind}/").split())

    def origin_release_branches(self):
        return {b for b in self.origin_refs("heads") if b.startswith("release/")}

    def tag_commit(self, name):
        return self.on_origin("rev-parse", f"{name}^{{commit}}")

    def prs(self):
        path = self.state / "prs.json"
        return json.loads(path.read_text()) if path.exists() else []

    def open_prs(self):
        return [p for p in self.prs() if p["state"] == "open"]

    def pr(self, number):
        return next(p for p in self.prs() if p["number"] == number)

    def add_pr(self, head, cross=False, body="old body\n"):
        prs = self.prs()
        n = max([p["number"] for p in prs], default=0) + 1
        prs.append({"number": n, "headRefName": head, "baseRefName": "main", "title": head, "body": body,
                    "state": "open", "isCrossRepository": cross})
        (self.state / "prs.json").write_text(json.dumps(prs))
        return n

    def workflow_runs(self):
        path = self.state / "workflow-runs"
        return path.read_text().splitlines() if path.exists() else []

    def add_release(self, tag):
        (self.state / "releases").mkdir(exist_ok=True)
        (self.state / "releases" / tag).write_text("notes\n")

    def release_notes(self, tag):
        path = self.state / "releases" / tag
        return path.read_text() if path.exists() else None

    def assert_ok(self, r):
        self.assertEqual(r.returncode, 0, f"exit {r.returncode}\n{r.stdout}{r.stderr}")

    def assert_refused(self, r, *phrases):
        self.assertNotEqual(r.returncode, 0, f"expected a refusal\n{r.stdout}{r.stderr}")
        for phrase in phrases:
            self.assertIn(phrase, r.stdout + r.stderr)

    # --- prepare ---

    def test_ac_1_prepare_pushes_the_rolled_changelog_to_a_release_branch_and_opens_its_pr(self):
        r = self.release("prepare", "--bump", "patch", "--pr", "--date", DATE)
        self.assert_ok(r)
        self.assertEqual(self.on_origin("rev-parse", "release/v0.14.1^"), self.on_origin("rev-parse", "main"))
        mp = json.loads(self.origin_file("release/v0.14.1", ".claude-plugin/marketplace.json"))
        self.assertEqual(mp["metadata"]["version"], "0.14.1")
        cl = self.origin_file("release/v0.14.1", "CHANGELOG.md")
        self.assertIn(f"## [Unreleased]\n\n## [0.14.1] - {DATE}\n\n- first entry\n\n## [0.14.0] - 2026-10-01\n\n- old entry", cl)
        [pr] = self.open_prs()
        self.assertEqual((pr["headRefName"], pr["baseRefName"], pr["title"], pr["body"]),
                         ("release/v0.14.1", "main", "release v0.14.1", "- first entry\n"))

    def test_ac_1_prepare_dispatches_validate_on_the_release_branch_only_when_asked(self):
        self.assert_ok(self.release("prepare", "--bump", "patch", "--pr", "--dispatch-validate", "--date", DATE))
        self.assertEqual(self.workflow_runs(), ["validate.yml release/v0.14.1"])
        self.assert_ok(self.release("prepare", "--bump", "patch", "--pr", "--date", DATE))
        self.assertEqual(self.workflow_runs(), ["validate.yml release/v0.14.1"])

    def test_ac_1b_prepare_refuses_an_empty_unreleased_section(self):
        self.write_main("0.14.0", [], [("0.14.0", ["old entry"])], "nothing new", push=True)
        r = self.release("prepare", "--bump", "patch", "--pr", "--date", DATE)
        self.assert_refused(r, "nothing to release")
        self.assertFalse(self.origin_release_branches())
        self.assertFalse(self.open_prs())

    def test_prepare_ends_the_unreleased_notes_at_the_next_heading_even_without_a_blank_line(self):
        tight = "# Changelog\n\n## [Unreleased]\n## [0.14.0] - 2026-10-01\n\n- old entry\n"
        self.write_main("0.14.0", [], [], "tight, empty", push=True, changelog_text=tight)
        self.assert_refused(self.release("prepare", "--bump", "patch", "--date", DATE), "nothing to release")
        tight = "# Changelog\n\n## [Unreleased]\n- first entry\n## [0.14.0] - 2026-10-01\n\n- old entry\n"
        self.write_main("0.14.0", [], [], "tight, one entry", push=True, changelog_text=tight)
        self.assert_ok(self.release("prepare", "--bump", "patch", "--pr", "--date", DATE))
        self.assertEqual(self.open_prs()[0]["body"], "- first entry\n")
        self.assertEqual(self.origin_file("release/v0.14.1", "CHANGELOG.md").count("## [0.14.0]"), 1)

    def test_prepare_without_a_date_stamps_todays_utc_date(self):
        before = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
        self.assert_ok(self.release("prepare", "--bump", "patch"))
        after = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
        cl = self.origin_file("release/v0.14.1", "CHANGELOG.md")
        self.assertTrue(f"## [0.14.1] - {before}" in cl or f"## [0.14.1] - {after}" in cl, cl)

    def test_prepare_refuses_a_date_that_is_not_yyyy_mm_dd(self):
        for date in ("2026-13-40", "20261105", "2026-W45-4", ""):
            with self.subTest(date=date):
                self.assert_refused(self.release("prepare", "--bump", "patch", "--date", date), "--date")
        self.assertFalse(self.origin_release_branches())

    def test_prepare_refuses_an_empty_version(self):
        r = self.release("prepare", "--version", "", "--date", DATE)
        self.assert_refused(r, "bad version")
        self.assertNotIn("Traceback", r.stderr)
        self.assertFalse(self.origin_release_branches())

    def test_ac_2a_prepare_again_rebuilds_the_branch_and_updates_the_open_pr(self):
        self.assert_ok(self.release("prepare", "--bump", "patch", "--pr", "--date", DATE))
        [first] = self.open_prs()
        self.write_main("0.14.0", ["first entry", "second entry"], [("0.14.0", ["old entry"])], "publish another skill", push=True)
        self.assert_ok(self.release("prepare", "--bump", "patch", "--pr", "--date", DATE))
        [pr] = self.open_prs()
        self.assertEqual(pr["number"], first["number"])
        self.assertEqual(pr["body"], "- first entry\n- second entry\n")
        self.assertIn(f"## [0.14.1] - {DATE}\n\n- first entry\n- second entry\n",
                      self.origin_file("release/v0.14.1", "CHANGELOG.md"))
        self.assertEqual(self.on_origin("rev-parse", "release/v0.14.1^"), self.on_origin("rev-parse", "main"))

    def test_ac_2b_prepare_for_another_version_closes_the_old_release_pr_and_deletes_its_branch(self):
        self.git("push", "-q", "origin", "main:refs/heads/release/v0.15.0")
        old = self.add_pr("release/v0.15.0")
        self.assert_ok(self.release("prepare", "--bump", "major", "--pr", "--date", DATE))
        self.assertEqual(self.pr(old)["state"], "closed")
        self.assertNotIn("release/v0.15.0", self.origin_refs("heads"))
        self.assertEqual([p["headRefName"] for p in self.open_prs()], ["release/v1.0.0"])

    def test_prepare_leaves_unrelated_and_fork_prs_alone(self):
        for branch in ("feature/x", "release/v2-docs"):
            self.git("push", "-q", "origin", f"main:refs/heads/{branch}")
        feature, docs = self.add_pr("feature/x"), self.add_pr("release/v2-docs")
        fork = self.add_pr("release/v0.14.1", cross=True, body="fork body\n")
        self.assert_ok(self.release("prepare", "--bump", "patch", "--pr", "--date", DATE))
        for n in (feature, docs, fork):
            self.assertEqual(self.pr(n)["state"], "open")
        self.assertEqual(self.pr(fork)["body"], "fork body\n")
        self.assertTrue({"feature/x", "release/v2-docs"} <= self.origin_refs("heads"))
        ours = [p for p in self.open_prs() if p["headRefName"] == "release/v0.14.1" and not p["isCrossRepository"]]
        self.assertEqual([p["body"] for p in ours], ["- first entry\n"])

    def test_prepare_keeps_the_old_release_pr_when_the_new_one_cannot_be_created(self):
        self.git("push", "-q", "origin", "main:refs/heads/release/v0.15.0")
        old = self.add_pr("release/v0.15.0")
        r = self.release("prepare", "--bump", "major", "--pr", "--date", DATE, FAKE_GH_FAIL="pr create")
        self.assert_refused(r, SETTING)
        self.assertEqual(self.pr(old)["state"], "open")
        self.assertIn("release/v0.15.0", self.origin_refs("heads"))
        self.assertNotIn("release/v1.0.0", self.origin_refs("heads"))

    def test_prepare_dispatches_validate_before_closing_old_release_prs(self):
        self.git("push", "-q", "origin", "main:refs/heads/release/v0.15.0")
        self.add_pr("release/v0.15.0")
        r = self.release("prepare", "--bump", "major", "--pr", "--dispatch-validate", "--date", DATE, FAKE_GH_FAIL="pr close")
        self.assert_refused(r)
        self.assertEqual(self.workflow_runs(), ["validate.yml release/v1.0.0"])
        self.assertIn("release/v1.0.0", [p["headRefName"] for p in self.open_prs()])

    def test_prepare_refuses_a_version_that_is_not_above_the_current_one_or_the_latest_tag(self):
        for args in (["--version", "0.14.0"], ["--version", "0.13.0"]):
            with self.subTest(args=args):
                self.assert_refused(self.release("prepare", *args, "--date", DATE), "must be above")
        self.tag("v0.14.1", push=True)
        self.assert_refused(self.release("prepare", "--bump", "patch", "--date", DATE), "must be above")
        self.assertFalse(self.origin_release_branches())

    def test_prepare_refuses_while_the_current_version_has_no_release(self):
        self.write_main("0.14.1", ["next entry"], [("0.14.1", ["first entry"]), ("0.14.0", ["old entry"])],
                        "merged, never published", push=True)
        self.assert_refused(self.release("prepare", "--bump", "patch", "--date", DATE), "publish")
        self.assertFalse(self.origin_release_branches())

    def test_prepare_validates_and_releases_origin_main_not_the_checkout(self):
        self.git("checkout", "-q", "-b", "wip")
        self.write_main("0.14.0", ["first entry"], [("0.14.0", ["old entry"])], "broken locally", plugin_version="9.9.9")
        self.assert_ok(self.release("prepare", "--bump", "patch", "--pr", "--date", DATE))
        self.assertEqual(self.on_origin("rev-parse", "release/v0.14.1^"), self.on_origin("rev-parse", "main"))
        mp = json.loads(self.origin_file("release/v0.14.1", ".claude-plugin/marketplace.json"))
        self.assertEqual(mp["plugins"][0]["version"], "0.1.0")

    def test_prepare_refuses_when_origin_main_fails_validation(self):
        healthy = self.head()
        self.write_main("0.14.0", ["first entry"], [("0.14.0", ["old entry"])], "broken on main", push=True,
                        plugin_version="9.9.9")
        self.git("checkout", "-q", "-b", "healthy", healthy)
        self.assert_refused(self.release("prepare", "--bump", "patch", "--pr", "--date", DATE), "version mismatch")
        self.assertFalse(self.origin_release_branches())
        self.assertFalse(self.open_prs())

    def test_ac_5a_prepare_dry_run_prints_non_ascii_notes_on_a_cp1252_console(self):
        self.write_main("0.14.0", ["sentinel: mean/σ bands"], [("0.14.0", ["old entry"])], "sigma", push=True)
        r = self.release("prepare", "--bump", "patch", "--dry-run", PYTHONIOENCODING="cp1252")
        self.assert_ok(r)
        self.assertIn("mean/σ bands", r.stdout)

    def test_prepare_dry_run_pushes_nothing_and_opens_no_pr(self):
        self.assert_ok(self.release("prepare", "--bump", "patch", "--pr", "--dispatch-validate", "--dry-run"))
        self.assertFalse(self.origin_release_branches())
        self.assertFalse(self.open_prs())
        self.assertFalse(self.workflow_runs())

    # --- publish ---

    def test_ac_3_publish_tags_the_commit_that_set_the_version_even_after_main_moved_on(self):
        self.assert_ok(self.release("prepare", "--bump", "patch", "--pr", "--date", DATE))
        release_sha = self.merge_release_branch("0.14.1")
        self.advance_main("a later skill publish")
        self.assert_ok(self.release("publish"))
        self.assertEqual(self.tag_commit("v0.14.1"), release_sha)
        self.assertEqual(self.release_notes("v0.14.1"), "- first entry\n")
        self.assertFalse((self.state / "releases" / "v0.14.1.not-latest").exists())

    def test_ac_3b_publish_does_nothing_when_the_tag_and_release_exist(self):
        sha = self.released_on_main("0.14.1", ["first entry"])
        self.tag("v0.14.1", push=True)
        self.add_release("v0.14.1")
        r = self.release("publish")
        self.assert_ok(r)
        self.assertIn("nothing to do", r.stdout)
        self.assertEqual(self.release_notes("v0.14.1"), "notes\n")
        self.assertEqual(self.tag_commit("v0.14.1"), sha)

    def test_ac_3c_publish_creates_the_missing_release_for_an_existing_tag(self):
        sha = self.released_on_main("0.14.1", ["first entry"])
        self.tag("v0.14.1", push=True)
        self.assertNotEqual(self.advance_main("a later skill publish"), sha)
        self.assert_ok(self.release("publish"))
        self.assertEqual(self.release_notes("v0.14.1"), "- first entry\n")
        self.assertEqual(self.tag_commit("v0.14.1"), sha)
        self.assertFalse((self.state / "releases" / "v0.14.1.not-latest").exists())

    def test_ac_3d_publish_fails_without_a_changelog_section_and_creates_no_tag(self):
        self.write_main("0.14.2", [], [("0.14.0", ["old entry"])], "bump by hand", push=True)
        self.assert_refused(self.release("publish"), "[0.14.2]")
        self.assertNotIn("v0.14.2", self.origin_refs("tags"))

    def test_ac_3e_publish_refuses_a_version_below_the_latest_tag(self):
        self.tag("v0.14.1", push=True)
        self.write_main("0.13.5", [], [("0.13.5", ["backport"]), ("0.14.0", ["old entry"])], "downgrade", push=True)
        self.assert_refused(self.release("publish"), "0.13.5", "v0.14.1")
        self.assertNotIn("v0.13.5", self.origin_refs("tags"))

    def test_publish_compares_versions_as_numbers_not_text(self):
        self.tag("v0.14.1", push=True)
        self.write_main("0.9.5", [], [("0.9.5", ["backport"]), ("0.14.0", ["old entry"])], "downgrade", push=True)
        self.assert_refused(self.release("publish"), "0.9.5", "v0.14.1")
        self.assertNotIn("v0.9.5", self.origin_refs("tags"))

    def test_publish_completes_an_older_tagged_release_without_marking_it_latest(self):
        half = self.released_on_main("0.14.1", ["first entry"])
        self.tag("v0.14.1", push=True)  # the tag went out, the Release didn't
        self.write_main("0.14.2", [], [("0.14.2", ["next entry"]), ("0.14.1", ["first entry"]), ("0.14.0", ["old entry"])],
                        "release v0.14.2", push=True)
        self.tag("v0.14.2", push=True)
        self.add_release("v0.14.2")
        self.assert_ok(self.release("publish", "--ref", half))
        self.assertEqual(self.release_notes("v0.14.1"), "- first entry\n")
        self.assertTrue((self.state / "releases" / "v0.14.1.not-latest").exists())
        self.assertEqual(self.tag_commit("v0.14.1"), half)

    def test_publish_finishes_an_older_release_only_with_an_explicit_ref(self):
        self.released_on_main("0.14.1", ["first entry"])
        self.tag("v0.14.1", push=True)  # the tag went out, the Release didn't
        self.write_main("0.14.2", [], [("0.14.2", ["next entry"]), ("0.14.1", ["first entry"]), ("0.14.0", ["old entry"])],
                        "release v0.14.2", push=True)
        self.tag("v0.14.2", push=True)
        self.add_release("v0.14.2")
        self.released_on_main("0.14.1", ["first entry"])  # main reverted to the older version
        self.assert_refused(self.release("publish"), "--ref")
        self.assertIsNone(self.release_notes("v0.14.1"))
        self.assert_ok(self.release("publish", "--ref", "v0.14.1"))
        self.assertEqual(self.release_notes("v0.14.1"), "- first entry\n")

    def test_ac_4a_prepare_and_publish_never_move_origin_main(self):
        before = self.on_origin("rev-parse", "main")
        self.assert_ok(self.release("prepare", "--bump", "patch", "--pr", "--date", DATE))
        self.assertEqual(self.on_origin("rev-parse", "main"), before)
        merged = self.merge_release_branch("0.14.1")
        self.assert_ok(self.release("publish"))
        self.assertIn("v0.14.1", self.origin_refs("tags"))
        self.assertEqual(self.on_origin("rev-parse", "main"), merged)

    def test_ac_4b_publish_refuses_a_commit_that_is_not_on_origin_main(self):
        self.write_main("0.14.1", [], [("0.14.1", ["first entry"]), ("0.14.0", ["old entry"])], "local only")
        self.assert_refused(self.release("publish"), "not on origin/main")
        self.assertNotIn("v0.14.1", self.origin_refs("tags"))

    def test_publish_from_a_checkout_behind_origin_main(self):
        stale = self.head()
        sha = self.released_on_main("0.14.1", ["first entry"])
        self.git("reset", "-q", "--hard", stale)
        r = self.release("publish")
        self.assert_ok(r)
        self.assertIn("nothing to do", r.stdout)
        self.assertIn("--ref origin/main", r.stdout)
        self.assertNotIn("v0.14.1", self.origin_refs("tags"))
        self.assert_ok(self.release("publish", "--ref", "origin/main"))
        self.assertEqual(self.tag_commit("v0.14.1"), sha)
        with self.subTest("main only gained an unrelated commit: no hint"):
            self.git("merge", "-q", "--ff-only", "origin/main")
            self.add_release("v0.14.1")
            self.advance_main("a later skill publish")
            self.git("reset", "-q", "--hard", "HEAD~1")
            r = self.release("publish")
            self.assert_ok(r)
            self.assertNotIn("--ref origin/main", r.stdout)

    def test_publish_tags_the_first_commit_that_has_the_version_and_its_section(self):
        self.write_main("0.14.1", [], [("0.14.0", ["old entry"])], "bump, section forgotten", push=True)
        self.assert_refused(self.release("publish"), "[0.14.1]")
        fixed = self.write_main("0.14.1", [], [("0.14.1", ["first entry"]), ("0.14.0", ["old entry"])], "add the section", push=True)
        self.assert_ok(self.release("publish"))
        self.assertEqual(self.tag_commit("v0.14.1"), fixed)
        self.assertEqual(self.release_notes("v0.14.1"), "- first entry\n")

    def test_publish_refuses_an_existing_tag_on_a_main_commit_with_another_version(self):
        self.released_on_main("0.14.1", ["first entry"])
        self.tag("v0.14.1", rev="HEAD~1", push=True)
        self.assert_refused(self.release("publish"), "fix or delete the tag")
        self.assertIsNone(self.release_notes("v0.14.1"))

    def test_publish_refuses_an_existing_tag_on_a_commit_that_never_reached_main(self):
        self.released_on_main("0.14.1", ["first entry"])
        main_head = self.head()
        self.git("checkout", "-q", "-b", "side")
        self.write_main("0.14.1", [], [("0.14.1", ["side entry"]), ("0.14.0", ["old entry"])], "side commit")
        self.tag("v0.14.1", push=True)
        self.git("checkout", "-q", "main")
        self.assertEqual(self.head(), main_head)
        self.assert_refused(self.release("publish"), "fix or delete the tag")
        self.assertIsNone(self.release_notes("v0.14.1"))

    def test_release_refuses_a_clone_with_several_remotes_unless_gh_repo_is_set(self):
        self.git("remote", "add", "upstream", str(self.origin))
        for cmd in (["prepare", "--bump", "patch", "--dry-run"], ["publish", "--dry-run"]):
            with self.subTest(cmd=cmd[0]):
                self.assert_refused(self.release(*cmd), "GH_REPO")
                self.assert_ok(self.release(*cmd, GH_REPO="example/agent-skills"))

    def test_publish_creates_the_first_release_when_the_repo_has_no_tags(self):
        first = self.git("rev-list", "--max-parents=0", "HEAD")
        self.git("push", "-q", "origin", ":refs/tags/v0.14.0")
        self.git("tag", "-d", "v0.14.0")
        (self.state / "releases" / "v0.14.0").unlink()
        self.assert_ok(self.release("publish"))
        self.assertEqual(self.tag_commit("v0.14.0"), first)
        self.assertEqual(self.release_notes("v0.14.0"), "- old entry\n")

    def test_publish_reuses_a_local_tag_left_by_a_rejected_push(self):
        sha = self.released_on_main("0.14.1", ["first entry"])
        self.tag("v0.14.1")
        self.assert_ok(self.release("publish"))
        self.assertEqual(self.tag_commit("v0.14.1"), sha)
        self.assertEqual(self.release_notes("v0.14.1"), "- first entry\n")

    def test_publish_refuses_a_local_tag_that_points_elsewhere(self):
        self.released_on_main("0.14.1", ["first entry"])
        self.tag("v0.14.1", rev="HEAD~1")
        self.assert_refused(self.release("publish"), "git tag -d v0.14.1")
        self.assertNotIn("v0.14.1", self.origin_refs("tags"))

    def test_publish_dry_run_tags_nothing_and_creates_no_release(self):
        self.released_on_main("0.14.1", ["first entry"])
        r = self.release("publish", "--dry-run")
        self.assert_ok(r)
        self.assertIn("- first entry", r.stdout)
        self.assertNotIn("v0.14.1", self.origin_refs("tags"))
        self.assertIsNone(self.release_notes("v0.14.1"))


if __name__ == "__main__":
    unittest.main()
