#!/usr/bin/env python3
"""Publish one local skill to mqmalagris/agent-skills.

Mechanical pipeline: refresh a repo clone -> copy skills/<name> -> mint
.claude-plugin/plugin.json -> upsert marketplace.json entry -> bump the skill's
version -> log a CHANGELOG [Unreleased] entry -> validate JSON -> commit + push.

Idempotent. On UPDATE it preserves the existing category/keywords/description
and bumps the PATCH version by default (--bump minor|major or --version to
override, --no-bump to hold). On a NEW skill it uses --version (default 0.1.0).
Collection releases are cut separately with scripts/release.py in the repo.
"""
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path

REPO = "https://github.com/mqmalagris/agent-skills"
OWNER_NAME = "mqmalagris/agent-skills"
AUTHOR = {"name": "Matheus Malagris", "url": "https://github.com/mqmalagris"}
DEFAULT_LOCAL = Path.home() / ".claude" / "skills"
DEFAULT_REPO_DIR = Path.home() / ".cache" / "agent-skills-publish"
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def run(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and r.returncode != 0:
        sys.exit(f"! `{' '.join(cmd)}` failed:\n{r.stdout}{r.stderr}")
    return r


def bump_semver(v, part):
    m = SEMVER.match(v or "0.0.0")
    M, mi, p = (int(x) for x in m.groups()) if m else (0, 0, 0)
    return {"major": f"{M+1}.0.0", "minor": f"{M}.{mi+1}.0", "patch": f"{M}.{mi}.{p+1}"}[part]


def frontmatter_description(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return ""
    desc, capturing = [], False
    for line in m.group(1).splitlines():
        dm = re.match(r"^description:\s*(.*)$", line)
        if dm:
            val = dm.group(1).strip()
            if val in ("|", ">", "|-", ">-", ""):
                capturing = True
                continue
            desc = [val.strip().strip('"').strip("'")]
            break
        if capturing:
            if re.match(r"^\S", line):
                break
            desc.append(line.strip())
    joined = re.sub(r"\s+", " ", " ".join(desc)).strip()
    first = re.split(r"(?<=[.!?])\s", joined)[0] if joined else ""
    return (first if 20 <= len(first) <= 240 else joined)[:240].strip()


def ensure_repo(repo_dir: Path):
    if (repo_dir / ".git").exists():
        run(["git", "fetch", "origin", "main"], cwd=repo_dir)
        run(["git", "checkout", "main"], cwd=repo_dir)
        run(["git", "reset", "--hard", "origin/main"], cwd=repo_dir)
    else:
        repo_dir.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", REPO + ".git", str(repo_dir)])


def changelog_add(repo_dir: Path, entry: str):
    cl = repo_dir / "CHANGELOG.md"
    if not cl.exists():
        return False
    text = cl.read_text(encoding="utf-8")
    i = text.find("## [Unreleased]")
    if i == -1:
        return False
    j = text.find("\n", i) + 1
    cl.write_text(text[:j] + f"- {entry}\n" + text[j:], encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser(description="Publish a local skill to " + OWNER_NAME)
    ap.add_argument("skill", help="skill name = dir under the local skills dir")
    ap.add_argument("--category", default=None,
                    help="marketplace category (required for a NEW skill; kept from existing on update)")
    ap.add_argument("--keywords", default=None, help="comma-separated keywords (kept from existing on update if omitted)")
    ap.add_argument("--description", default="", help="concise description (kept from existing, else derived from SKILL.md)")
    ap.add_argument("--version", default=None, help="set an explicit version X.Y.Z")
    ap.add_argument("--bump", choices=["major", "minor", "patch"], default=None,
                    help="on update, bump this part (default: patch)")
    ap.add_argument("--no-bump", action="store_true", help="on update, keep the existing version")
    ap.add_argument("--changelog", default=None, help="CHANGELOG [Unreleased] line (default auto)")
    ap.add_argument("--author-name", default=AUTHOR["name"])
    ap.add_argument("--local-skills-dir", type=Path, default=DEFAULT_LOCAL)
    ap.add_argument("--repo-dir", type=Path, default=DEFAULT_REPO_DIR)
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    name = args.skill
    src = args.local_skills_dir / name
    if not (src / "SKILL.md").exists():
        sys.exit(f"! no SKILL.md at {src}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        sys.exit(f"! skill name '{name}' must be kebab-case")

    ensure_repo(args.repo_dir)
    mp_path = args.repo_dir / ".claude-plugin" / "marketplace.json"
    mp = json.loads(mp_path.read_text(encoding="utf-8"))
    existing = next((p for p in mp["plugins"] if p["name"] == name), None)

    category = args.category or (existing or {}).get("category")
    if not category:
        sys.exit("! --category is required for a new skill")
    kw = ([k.strip() for k in args.keywords.split(",") if k.strip()]
          if args.keywords is not None else list((existing or {}).get("keywords", [])))
    desc = (args.description.strip() or (existing or {}).get("description")
            or frontmatter_description(src / "SKILL.md"))
    if not desc:
        sys.exit("! no description given and none parseable from SKILL.md; pass --description")

    # version: explicit > (update: bump/keep) > (new: 0.1.0)
    prev = (existing or {}).get("version")
    if args.version:
        version = args.version
    elif existing and not args.no_bump:
        version = bump_semver(prev, args.bump or "patch")
    else:
        version = prev or "0.1.0"
    if not SEMVER.match(version):
        sys.exit(f"! version '{version}' not X.Y.Z")

    dst = args.repo_dir / "skills" / name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    plugin = {
        "name": name, "version": version, "description": desc,
        "author": {"name": args.author_name, "url": AUTHOR["url"]},
        "homepage": f"{REPO}/tree/main/skills/{name}",
        "repository": REPO, "license": "MIT",
        "keywords": kw + [category],
    }
    (dst / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (dst / ".claude-plugin" / "plugin.json").write_text(json.dumps(plugin, indent=2) + "\n", encoding="utf-8")

    entry = {
        "name": name, "source": f"./skills/{name}", "description": desc,
        "version": version, "author": {"name": args.author_name},
        "category": category, "keywords": kw,
    }
    mp["plugins"] = [p for p in mp["plugins"] if p["name"] != name] + [entry]
    mp_path.write_text(json.dumps(mp, indent=2) + "\n", encoding="utf-8")

    action = "updated" if existing else "added"
    cl_line = args.changelog or f"`{name}` {version} — {'updated' if existing else 'new skill'}"
    logged = changelog_add(args.repo_dir, cl_line)

    # validate every manifest parses
    for p in [mp_path] + list((args.repo_dir / "skills").glob("*/.claude-plugin/plugin.json")):
        json.loads(p.read_text(encoding="utf-8"))

    print(f"{action} skills/{name} v{version} ({len(mp['plugins'])} plugins)" + ("" if logged else "  [no CHANGELOG]"))
    print(f'README row -> | [`{name}`](skills/{name}/) | {desc} |')

    if args.dry_run:
        print("dry-run: no commit/push. Repo prepared at", args.repo_dir)
        return

    run(["git", "add", "-A"], cwd=args.repo_dir)
    if run(["git", "diff", "--cached", "--quiet"], cwd=args.repo_dir, check=False).returncode == 0:
        print("no changes to commit (already in sync)")
        return
    run(["git", "commit", "-m", f"{action} skill: {name} v{version}"], cwd=args.repo_dir)
    local_sha = run(["git", "rev-parse", "HEAD"], cwd=args.repo_dir).stdout.strip()
    if args.no_push:
        print(f"committed {local_sha[:7]} locally (--no-push). Push with: git -C {args.repo_dir} push origin main")
        return
    run(["git", "push", "origin", "HEAD:main"], cwd=args.repo_dir)
    remote_sha = run(["git", "ls-remote", "origin", "-h", "refs/heads/main"], cwd=args.repo_dir).stdout.split()[0]
    ok = local_sha == remote_sha
    print(f"{'OK pushed' if ok else 'MISMATCH'} {local_sha[:7]} -> origin/main ({OWNER_NAME})")
    if not ok:
        sys.exit("! push did not land; check remote")


if __name__ == "__main__":
    main()
