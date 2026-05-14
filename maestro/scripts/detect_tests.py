#!/usr/bin/env python3
"""Detect the test runner for a project root.

Probes manifests in priority order. Emits JSON {runner, command, prefix} where
`prefix` is `rtk ` when rtk is on PATH (the user's CLAUDE.md mandates rtk for
token savings). When nothing matches, emits {runner: null} so the skill knows
to ask the user.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def has_dep(pkg: dict, name: str) -> bool:
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        if isinstance(pkg.get(key), dict) and name in pkg[key]:
            return True
    return False


def detect_pm(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "bun.lockb").exists():
        return "bun"
    return "npm"


def detect(root: Path) -> dict:
    pkg_path = root / "package.json"
    pkg = load_json(pkg_path) if pkg_path.exists() else None

    if pkg:
        if has_dep(pkg, "vitest"):
            return {"runner": "vitest", "command": "vitest run"}
        if has_dep(pkg, "jest"):
            return {"runner": "jest", "command": "jest --ci"}
        if has_dep(pkg, "@playwright/test") or has_dep(pkg, "playwright"):
            return {"runner": "playwright", "command": "playwright test"}
        scripts = pkg.get("scripts", {}) if isinstance(pkg.get("scripts"), dict) else {}
        if "test" in scripts:
            pm = detect_pm(root)
            return {"runner": f"{pm}-test", "command": f"{pm} test"}

    if (root / "Cargo.toml").exists():
        return {"runner": "cargo", "command": "cargo test"}

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text(encoding="utf-8", errors="ignore")
        if "pytest" in text:
            return {"runner": "pytest", "command": "pytest"}
    if (root / "pytest.ini").exists() or (root / "tox.ini").exists():
        return {"runner": "pytest", "command": "pytest"}

    if (root / "go.mod").exists():
        return {"runner": "go", "command": "go test ./..."}

    if (root / "mix.exs").exists():
        return {"runner": "mix", "command": "mix test"}

    if (root / "Gemfile").exists() or (root / ".rspec").exists():
        return {"runner": "rspec", "command": "bundle exec rspec"}

    return {"runner": None, "command": None}


def main() -> None:
    ap = argparse.ArgumentParser(description="Detect the test runner for a project.")
    ap.add_argument("--root", default=".", help="Project root to probe.")
    ap.add_argument(
        "--no-rtk-prefix",
        action="store_true",
        help="Do not prefix the command with rtk even if rtk is on PATH.",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")

    result = detect(root)

    rtk_available = shutil.which("rtk") is not None
    prefix = ""
    if result.get("command") and rtk_available and not args.no_rtk_prefix:
        prefix = "rtk "
    result["prefix"] = prefix
    result["full_command"] = (prefix + result["command"]) if result.get("command") else None
    result["root"] = str(root).replace("\\", "/")
    result["rtk_available"] = rtk_available

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
