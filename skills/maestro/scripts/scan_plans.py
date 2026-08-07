#!/usr/bin/env python3
"""Scan a repo for plan/PRD/ADR docs.

Outputs JSON list of {type, path} for every match.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PATTERNS: dict[str, list[str]] = {
    "plan": [
        "docs/plans/*.md",
        "plans/*.md",
        ".claude/plans/*.md",
    ],
    "prd": [
        "docs/prds/*.md",
        "docs/PRDs/*.md",
        "prds/*.md",
        "docs/product/*.md",
    ],
    "adr": [
        "docs/adr/*.md",
        "docs/adrs/*.md",
        "docs/ADR/*.md",
        "adrs/*.md",
        "docs/decisions/*.md",
    ],
}


def main() -> None:
    ap = argparse.ArgumentParser(description="Find plan/PRD/ADR docs in a repo.")
    ap.add_argument("--root", default=".", help="Repo root to scan from.")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")

    seen: set[Path] = set()
    found: list[dict[str, str]] = []
    for kind, globs in PATTERNS.items():
        for pattern in globs:
            for path in root.glob(pattern):
                if not path.is_file() or path in seen:
                    continue
                seen.add(path)
                found.append(
                    {
                        "type": kind,
                        "path": str(path.relative_to(root)).replace("\\", "/"),
                    }
                )

    print(json.dumps(found, indent=2))


if __name__ == "__main__":
    main()
