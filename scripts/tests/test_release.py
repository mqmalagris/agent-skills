#!/usr/bin/env python3
"""Integration tests for scripts/release.py.

Each test builds a throwaway repo with a bare `origin`, copies release.py and
validate_repo.py into it, and runs `release.py` as a subprocess, asserting what
a maintainer would see: exit code, output, branches, tags and files on
`origin`. `gh` is the one external boundary: a fake on PATH records every call
and answers from a state directory. Test names carry the plan's AC ids.

  python3 -m unittest discover -s scripts/tests -v
"""
import json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
DATE = "2026-11-05"

# Logs each call, answers `pr list` and `release view` from $FAKE_GH_STATE, and
# keeps the last --body-file / --notes-file so tests can read what was sent.
FAKE_GH = r"""#!/usr/bin/env bash
printf '%s\n' "$*" >> "$FAKE_GH_STATE/calls.log"
for ((i = 1; i <= $#; i++)); do
  case "${!i}" in
    --body-file) j=$((i + 1)); cp "${!j}" "$FAKE_GH_STATE/body.md" ;;
    --notes-file) j=$((i + 1)); cp "${!j}" "$FAKE_GH_STATE/notes.md" ;;
  esac
done
case "$1 $2" in
  "pr list") cat "$FAKE_GH_STATE/prs.json" 2>/dev/null || echo '[]' ;;
  "pr create") echo "https://github.com/example/agent-skills/pull/99" ;;
  "release view") [ -e "$FAKE_GH_STATE/releases/$3" ] ;;
  "release create") mkdir -p "$FAKE_GH_STATE/releases"; cp "$FAKE_GH_STATE/notes.md" "$FAKE_GH_STATE/releases/$3" ;;
esac
"""

SKILL_MD = '---\nname: demo\ndescription: "A demo skill for release tests."\n---\n\n# demo\n'


def changelog(unreleased, released):
    out = ["# Changelog", "", "## [Unreleased]"] + [f"- {e}" for e in unreleased] + [""]
    for version, entries in released:
        out += [f"## [{version}] - 2026-10-01", ""] + [f"- {e}" for e in entries] + [""]
    return "\n".join(out)


@unittest.skipIf(os.name == "nt", "the fake gh is a POSIX shell script; run under Linux or WSL")
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
        self.env = {**os.environ, **ident, "FAKE_GH_STATE": str(self.state),
                    "PATH": f"{bindir}{os.pathsep}{os.environ['PATH']}"}
        self.env.pop("PYTHONIOENCODING", None)
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(self.origin)], check=True)
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.repo)], check=True)
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
        self.git("tag", "-a", "v0.14.0", "-m", "v0.14.0")
        self.git("push", "-q", "origin", "v0.14.0")
        self.add_release("v0.14.0")

    # --- fixture helpers ---

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, env=self.env, check=True,
                              capture_output=True, text=True).stdout.strip()

    def write_main(self, version, unreleased, released, message, push=False):
        mp = {"name": "agent-skills", "metadata": {"version": version},
              "plugins": [{"name": "demo", "source": "./skills/demo", "version": "0.1.0"}]}
        (self.repo / ".claude-plugin").mkdir(exist_ok=True)
        (self.repo / ".claude-plugin" / "marketplace.json").write_text(json.dumps(mp, indent=2) + "\n")
        (self.repo / "CHANGELOG.md").write_text(changelog(unreleased, released))
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        if push:
            self.git("push", "-q", "origin", "main")

    def release(self, *args, **env):
        return subprocess.run([sys.executable, "scripts/release.py", *args], cwd=self.repo,
                              env={**self.env, **env}, capture_output=True, encoding="utf-8", errors="replace")

    def on_origin(self, *args):
        return subprocess.run(["git", "--git-dir", str(self.origin), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def origin_file(self, ref, path):
        return self.on_origin("show", f"{ref}:{path}")

    def origin_refs(self, kind):
        return set(self.on_origin("for-each-ref", "--format=%(refname:short)", f"refs/{kind}/").split())

    def gh_calls(self):
        log = self.state / "calls.log"
        calls = log.read_text().splitlines() if log.exists() else []
        log.unlink(missing_ok=True)
        return calls

    def set_open_prs(self, *prs):
        (self.state / "prs.json").write_text(json.dumps([{"number": n, "headRefName": h} for n, h in prs]))

    def add_release(self, tag):
        (self.state / "releases").mkdir(exist_ok=True)
        (self.state / "releases" / tag).write_text("notes\n")

    def assert_ok(self, r):
        self.assertEqual(r.returncode, 0, f"exit {r.returncode}\n{r.stdout}{r.stderr}")

    def assert_refused(self, r):
        self.assertNotEqual(r.returncode, 0, f"expected a refusal\n{r.stdout}{r.stderr}")

    # --- prepare ---

    def test_ac_1_prepare_pushes_the_rolled_changelog_to_a_release_branch_and_opens_its_pr(self):
        r = self.release("prepare", "--bump", "patch", "--pr", "--date", DATE)
        self.assert_ok(r)
        self.assertIn("release/v0.14.1", self.origin_refs("heads"))
        mp = json.loads(self.origin_file("release/v0.14.1", ".claude-plugin/marketplace.json"))
        self.assertEqual(mp["metadata"]["version"], "0.14.1")
        cl = self.origin_file("release/v0.14.1", "CHANGELOG.md")
        self.assertIn(f"## [Unreleased]\n\n## [0.14.1] - {DATE}\n\n- first entry\n", cl)
        calls = self.gh_calls()
        self.assertTrue(any(c.startswith("pr create --base main --head release/v0.14.1 --title release v0.14.1")
                            for c in calls), calls)
        self.assertEqual((self.state / "body.md").read_text(), "- first entry\n")

    def test_ac_1b_prepare_refuses_an_empty_unreleased_section(self):
        self.write_main("0.14.0", [], [("0.14.0", ["old entry"])], "nothing new", push=True)
        r = self.release("prepare", "--bump", "patch", "--pr", "--date", DATE)
        self.assert_refused(r)
        self.assertIn("nothing to release", r.stdout + r.stderr)
        self.assertFalse({b for b in self.origin_refs("heads") if b.startswith("release/")})
        self.assertFalse([c for c in self.gh_calls() if c.startswith("pr ")])

    def test_ac_2a_prepare_again_rebuilds_the_branch_and_updates_the_open_pr(self):
        self.assert_ok(self.release("prepare", "--bump", "patch", "--pr", "--date", DATE))
        self.gh_calls()
        self.set_open_prs((12, "release/v0.14.1"))
        self.write_main("0.14.0", ["first entry", "second entry"], [("0.14.0", ["old entry"])], "publish another skill", push=True)
        r = self.release("prepare", "--bump", "patch", "--pr", "--date", DATE)
        self.assert_ok(r)
        cl = self.origin_file("release/v0.14.1", "CHANGELOG.md")
        self.assertIn(f"## [0.14.1] - {DATE}\n\n- first entry\n- second entry\n", cl)
        self.assertEqual(self.on_origin("rev-parse", "release/v0.14.1^"), self.on_origin("rev-parse", "main"))
        calls = self.gh_calls()
        self.assertTrue(any(c.startswith("pr edit 12 --body-file") for c in calls), calls)
        self.assertFalse([c for c in calls if c.startswith("pr create")], calls)
        self.assertEqual((self.state / "body.md").read_text(), "- first entry\n- second entry\n")

    def test_ac_2b_prepare_for_another_version_closes_the_old_release_pr_and_deletes_its_branch(self):
        self.git("push", "-q", "origin", "main:refs/heads/release/v0.15.0")
        self.set_open_prs((7, "release/v0.15.0"))
        r = self.release("prepare", "--bump", "major", "--pr", "--date", DATE)
        self.assert_ok(r)
        heads = self.origin_refs("heads")
        self.assertNotIn("release/v0.15.0", heads)
        self.assertIn("release/v1.0.0", heads)
        calls = self.gh_calls()
        self.assertTrue(any(c.startswith("pr close 7") for c in calls), calls)
        self.assertTrue(any(c.startswith("pr create --base main --head release/v1.0.0") for c in calls), calls)

    def test_ac_5a_prepare_dry_run_prints_non_ascii_notes_on_a_cp1252_console(self):
        self.write_main("0.14.0", ["sentinel: mean/σ bands"], [("0.14.0", ["old entry"])], "sigma", push=True)
        r = self.release("prepare", "--bump", "patch", "--dry-run", PYTHONIOENCODING="cp1252")
        self.assert_ok(r)
        self.assertIn("mean/σ bands", r.stdout)
        self.assertFalse({b for b in self.origin_refs("heads") if b.startswith("release/")})

    # --- publish ---

    def merge_release(self, version, entries):
        """What merging a release PR leaves on main: the bumped version and its section."""
        self.write_main(version, [], [(version, entries), ("0.14.0", ["old entry"])], f"release v{version}", push=True)
        return self.git("rev-parse", "HEAD")

    def test_ac_3_publish_tags_the_release_commit_and_creates_the_release(self):
        sha = self.merge_release("0.14.1", ["first entry"])
        r = self.release("publish")
        self.assert_ok(r)
        self.assertEqual(self.on_origin("rev-parse", "v0.14.1^{commit}"), sha)
        self.assertEqual((self.state / "releases" / "v0.14.1").read_text(), "- first entry\n")

    def test_ac_3b_publish_does_nothing_when_the_tag_and_release_exist(self):
        sha = self.merge_release("0.14.1", ["first entry"])
        self.git("tag", "-a", "v0.14.1", "-m", "v0.14.1")
        self.git("push", "-q", "origin", "v0.14.1")
        self.add_release("v0.14.1")
        r = self.release("publish")
        self.assert_ok(r)
        self.assertIn("nothing to do", r.stdout)
        self.assertFalse([c for c in self.gh_calls() if c.startswith("release create")])
        self.assertEqual(self.on_origin("rev-parse", "v0.14.1^{commit}"), sha)

    def test_ac_3c_publish_creates_the_missing_release_for_an_existing_tag(self):
        sha = self.merge_release("0.14.1", ["first entry"])
        self.git("tag", "-a", "v0.14.1", "-m", "v0.14.1")
        self.git("push", "-q", "origin", "v0.14.1")
        r = self.release("publish")
        self.assert_ok(r)
        self.assertEqual((self.state / "releases" / "v0.14.1").read_text(), "- first entry\n")
        self.assertEqual(self.on_origin("rev-parse", "v0.14.1^{commit}"), sha)

    def test_ac_3d_publish_fails_without_a_changelog_section_and_creates_no_tag(self):
        self.write_main("0.14.2", [], [("0.14.0", ["old entry"])], "bump by hand", push=True)
        r = self.release("publish")
        self.assert_refused(r)
        self.assertIn("[0.14.2]", r.stdout + r.stderr)
        self.assertNotIn("v0.14.2", self.origin_refs("tags"))

    def test_ac_3e_publish_refuses_a_version_below_the_latest_tag(self):
        self.git("tag", "-a", "v0.14.1", "-m", "v0.14.1")
        self.git("push", "-q", "origin", "v0.14.1")
        self.write_main("0.13.5", [], [("0.13.5", ["backport"]), ("0.14.0", ["old entry"])], "downgrade", push=True)
        r = self.release("publish")
        self.assert_refused(r)
        out = r.stdout + r.stderr
        self.assertIn("0.13.5", out)
        self.assertIn("v0.14.1", out)
        self.assertNotIn("v0.13.5", self.origin_refs("tags"))

    # --- no path pushes main ---

    def test_ac_4a_prepare_and_publish_never_move_origin_main(self):
        before = self.on_origin("rev-parse", "main")
        self.assert_ok(self.release("prepare", "--bump", "patch", "--pr", "--date", DATE))
        self.assert_ok(self.release("publish"))
        self.assertEqual(self.on_origin("rev-parse", "main"), before)

    def test_ac_4b_publish_refuses_a_commit_that_is_not_on_origin_main(self):
        self.write_main("0.14.1", [], [("0.14.1", ["first entry"]), ("0.14.0", ["old entry"])], "local only")
        r = self.release("publish")
        self.assert_refused(r)
        self.assertIn("not on origin/main", r.stdout + r.stderr)
        self.assertNotIn("v0.14.1", self.origin_refs("tags"))


if __name__ == "__main__":
    unittest.main()
