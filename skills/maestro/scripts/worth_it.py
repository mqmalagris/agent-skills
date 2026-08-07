#!/usr/bin/env python3
"""Decide whether parallelizing a single plan/PRD/ADR is worth the coordination cost.

Verdicts:
  - worth-it
  - not-worth-it           (too small)
  - review-needed          (scattered dirs, unclear isolation)
  - serial-recommended     (touches migration/schema or shared types)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

MIGRATION_HINTS = re.compile(
    r"\b(migration|migrations|schema\.prisma|drizzle|sqlx|alembic|knex|liquibase|flyway)\b",
    re.IGNORECASE,
)
SHARED_HINTS = re.compile(
    r"\b(generated\s+types|openapi|graphql\s+schema|protobuf|proto\b|api\s+types|"
    r"shared\s+types|public\s+api|exported\s+contract)\b",
    re.IGNORECASE,
)


def run_extract(path: str) -> dict:
    script = Path(__file__).with_name("extract_files.py")
    res = subprocess.run(
        [sys.executable, str(script), path],
        capture_output=True,
        text=True,
        check=False,
    )
    if res.returncode != 0:
        raise SystemExit(f"extract_files.py failed for {path}:\n{res.stderr}")
    return json.loads(res.stdout)


def main() -> None:
    ap = argparse.ArgumentParser(description="Worth-it heuristic for one doc.")
    ap.add_argument("file", help="Plan/PRD/ADR markdown file.")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    info = run_extract(args.file)
    files: list[str] = info["files_touched"]

    size_score = min(len(text) / 2000, 5)
    file_count = len(files)
    dirs = {f.rsplit("/", 1)[0] for f in files if "/" in f}
    isolation = 1.0 / max(len(dirs), 1)
    has_migration = bool(MIGRATION_HINTS.search(text))
    has_shared = bool(SHARED_HINTS.search(text))

    SIZE_FLOOR = 0.75       # < 1.5 KB doc -> too small
    ISOLATION_FLOOR = 0.2   # 5+ distinct dirs -> scattered
    MIN_FILES = 2           # < 2 files touched -> not worth orchestrating

    flags: list[str] = []
    if has_migration:
        flags.append("touches-migration-or-schema")
    if has_shared:
        flags.append("touches-shared-types")
    if size_score < SIZE_FLOOR:
        flags.append("too-small")
    if file_count < MIN_FILES:
        flags.append("too-few-files")
    if isolation < ISOLATION_FLOOR and file_count > 0:
        flags.append("scattered-dirs")
    if info.get("unparseable"):
        flags.append("unparseable-file-list")

    if has_migration or has_shared:
        verdict = "serial-recommended"
    elif info.get("unparseable"):
        verdict = "review-needed"
    elif size_score < SIZE_FLOOR or file_count < MIN_FILES:
        verdict = "not-worth-it"
    elif isolation < ISOLATION_FLOOR and file_count > 0:
        verdict = "review-needed"
    else:
        verdict = "worth-it"

    print(
        json.dumps(
            {
                "file": info["file"],
                "verdict": verdict,
                "flags": flags,
                "metrics": {
                    "size_score": round(size_score, 2),
                    "file_count": file_count,
                    "distinct_dirs": len(dirs),
                    "isolation": round(isolation, 2),
                    "has_migration": has_migration,
                    "has_shared": has_shared,
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
