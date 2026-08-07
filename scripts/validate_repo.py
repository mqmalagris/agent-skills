#!/usr/bin/env python3
"""Validate the agent-skills repo: structure, manifests, version consistency,
and SKILL.md YAML frontmatter validity.

Exit 0 = clean, 1 = problems (printed). Used by CI (.github/workflows) and by
release.py as a pre-flight gate. Strict-parses frontmatter with PyYAML when
available (CI installs it); otherwise falls back to a colon-space heuristic so
the common "unquoted ': ' in description" break is still caught locally.
"""
import json, re, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def frontmatter_block(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    return m.group(1) if m else None


def check_frontmatter(text, name, problems):
    fm = frontmatter_block(text)
    if fm is None:
        problems.append(f"{name}: SKILL.md has no YAML frontmatter"); return
    if yaml is not None:
        try:
            data = yaml.safe_load(fm)
        except yaml.YAMLError as e:
            problems.append(f"{name}: SKILL.md frontmatter invalid YAML: {str(e).splitlines()[0]}"); return
        if not isinstance(data, dict):
            problems.append(f"{name}: SKILL.md frontmatter is not a mapping"); return
        if data.get("name", name) != name:
            problems.append(f"{name}: SKILL.md name '{data.get('name')}' != dir")
        if not data.get("description"):
            problems.append(f"{name}: SKILL.md missing frontmatter description")
    else:
        fields = {}
        for line in fm.splitlines():
            mm = re.match(r"^(\w+):\s*(.*)$", line)
            if mm and mm.group(1) not in fields:
                fields[mm.group(1)] = mm.group(2).strip()
        if fields.get("name", name) != name:
            problems.append(f"{name}: SKILL.md name '{fields.get('name')}' != dir")
        dm = re.search(r"^description:[ \t]*(.*)$", fm, re.M)
        dval = dm.group(1).strip() if dm else ""
        if not dm:
            problems.append(f"{name}: SKILL.md missing frontmatter description")
        elif dval[:1] not in ('"', "'") and dval not in ("|", ">", "|-", ">-", "") and ": " in dval:
            problems.append(f"{name}: SKILL.md description has an unquoted ': ' (invalid YAML; quote it or use a '>-' block scalar)")


def main():
    problems, skills_dir = [], ROOT / "skills"
    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.exists() else []
    if not skill_dirs:
        print("FAIL: no skills/ directory or it is empty"); sys.exit(1)
    dir_names = set()

    for d in skill_dirs:
        name = d.name
        dir_names.add(name)
        if not KEBAB.match(name):
            problems.append(f"{name}: dir name not kebab-case")
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            problems.append(f"{name}: missing SKILL.md")
        else:
            check_frontmatter(skill_md.read_text(encoding="utf-8"), name, problems)
        pj = d / ".claude-plugin" / "plugin.json"
        if not pj.exists():
            problems.append(f"{name}: missing .claude-plugin/plugin.json"); continue
        try:
            plugin = json.loads(pj.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"{name}: plugin.json invalid JSON: {e}"); continue
        if plugin.get("name") != name:
            problems.append(f"{name}: plugin.json name '{plugin.get('name')}' != dir")
        if not SEMVER.match(str(plugin.get("version", ""))):
            problems.append(f"{name}: plugin.json version '{plugin.get('version')}' not X.Y.Z")

    mp_path = ROOT / ".claude-plugin" / "marketplace.json"
    try:
        mp = json.loads(mp_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL: marketplace.json invalid JSON: {e}"); sys.exit(1)
    if not SEMVER.match(str(mp.get("metadata", {}).get("version", ""))):
        problems.append("marketplace metadata.version not X.Y.Z")
    entries = {p["name"]: p for p in mp.get("plugins", [])}
    for n in sorted(dir_names - set(entries)):
        problems.append(f"{n}: skill dir has no marketplace entry")
    for n in sorted(set(entries) - dir_names):
        problems.append(f"{n}: marketplace entry has no skill dir")
    for n, e in entries.items():
        if e.get("source") != f"./skills/{n}":
            problems.append(f"{n}: marketplace source '{e.get('source')}' != ./skills/{n}")
        pj = ROOT / "skills" / n / ".claude-plugin" / "plugin.json"
        if pj.exists():
            pv = json.loads(pj.read_text(encoding="utf-8")).get("version")
            if pv != e.get("version"):
                problems.append(f"{n}: version mismatch (plugin.json {pv} vs marketplace {e.get('version')})")

    if problems:
        print(f"FAIL: {len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    engine = "PyYAML strict" if yaml else "heuristic (no PyYAML)"
    print(f"OK: {len(skill_dirs)} skills, marketplace v{mp['metadata']['version']}, manifests + frontmatter consistent [{engine}]")


if __name__ == "__main__":
    main()
