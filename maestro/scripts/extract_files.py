#!/usr/bin/env python3
"""Extract files-touched, phase tag, and declared deps from a plan/PRD/ADR.

Heist plans (with a `## Crew` section) parse strict.
Other docs fall back to a whole-doc path scan.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HEIST_CREW_RE = re.compile(r"^##\s+(?:the\s+)?crew\s*$", re.IGNORECASE | re.MULTILINE)
SECTION_RE = re.compile(r"^##\s+", re.MULTILINE)
PATH_RE = re.compile(
    r"`([^`\n]+\.[A-Za-z0-9]+)`"
    r"|(?:^|\s)((?:\.{1,2}/)?[\w][\w./-]*/[\w./-]+\.[A-Za-z0-9]+)"
)
PHASE_RE = re.compile(
    r"^\s*(?:[-*]\s+)?(?:\*\*)?phase(?:\*\*)?\s*[:\-]\s*([^\n]+)",
    re.IGNORECASE | re.MULTILINE,
)
DEPS_RE = re.compile(
    r"(?:^|\n)\s*(?:[-*]\s+)?(?:\*\*)?(?:depends on|after|requires)(?:\*\*)?\s*[:\-]\s*([^\n]+)",
    re.IGNORECASE,
)


def slice_section(text: str, header_re: re.Pattern[str]) -> str | None:
    """Return the body of a `## Header` section up to the next `## ` header."""
    m = header_re.search(text)
    if not m:
        return None
    rest = text[m.end():]
    nxt = SECTION_RE.search(rest)
    return rest[: nxt.start()] if nxt else rest


def extract_paths(text: str) -> list[str]:
    paths: set[str] = set()
    for m in PATH_RE.finditer(text):
        candidate = m.group(1) or m.group(2)
        if not candidate:
            continue
        candidate = candidate.strip().strip(",;:()[]")
        if not candidate or candidate.startswith(("http://", "https://")):
            continue
        paths.add(candidate)
    return sorted(paths)


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract metadata from a planning doc.")
    ap.add_argument("file", help="Path to the plan/PRD/ADR markdown file.")
    args = ap.parse_args()

    path = Path(args.file)
    text = path.read_text(encoding="utf-8")

    crew = slice_section(text, HEIST_CREW_RE)
    if crew:
        files = extract_paths(crew)
        fmt = "heist"
    else:
        files = extract_paths(text)
        fmt = "generic"

    phase_match = PHASE_RE.search(text)
    deps_match = DEPS_RE.search(text)
    deps = (
        [d.strip() for d in deps_match.group(1).split(",") if d.strip()]
        if deps_match
        else []
    )

    print(
        json.dumps(
            {
                "file": str(path).replace("\\", "/"),
                "format": fmt,
                "files_touched": files,
                "phase": phase_match.group(1).strip() if phase_match else None,
                "deps": deps,
                "unparseable": fmt == "generic" and not files,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
