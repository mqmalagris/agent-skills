#!/usr/bin/env python3
"""Build a pairwise conflict matrix from extracted plan/PRD/ADR docs.

Calls extract_files.py per input doc, then computes file-overlap and
declared-dep edges. Detects dep cycles before emitting the matrix.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


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


def detect_cycle(nodes: list[str], edges: list[tuple[str, str]]) -> list[str]:
    """Return a cycle path if one exists, else []. Edge (a, b) = a depends on b."""
    graph: dict[str, list[str]] = {n: [] for n in nodes}
    for a, b in edges:
        if a in graph and b in graph:
            graph[a].append(b)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in nodes}
    parent: dict[str, str | None] = {n: None for n in nodes}

    def dfs(start: str) -> list[str]:
        stack: list[tuple[str, int]] = [(start, 0)]
        color[start] = GRAY
        while stack:
            node, idx = stack[-1]
            if idx < len(graph[node]):
                stack[-1] = (node, idx + 1)
                nxt = graph[node][idx]
                if color[nxt] == GRAY:
                    cycle = [nxt, node]
                    while parent[node] and node != nxt:
                        node = parent[node]  # type: ignore[assignment]
                        cycle.append(node)
                    return list(reversed(cycle))
                if color[nxt] == WHITE:
                    parent[nxt] = node
                    color[nxt] = GRAY
                    stack.append((nxt, 0))
            else:
                color[node] = BLACK
                stack.pop()
        return []

    for n in nodes:
        if color[n] == WHITE:
            cyc = dfs(n)
            if cyc:
                return cyc
    return []


def main() -> None:
    ap = argparse.ArgumentParser(description="Build a conflict matrix across docs.")
    ap.add_argument("files", nargs="+", help="Plan/PRD/ADR files to compare.")
    args = ap.parse_args()

    docs = [run_extract(f) for f in args.files]

    name_index: dict[str, str] = {}
    for d in docs:
        path = d["file"]
        name_index[path] = path
        name_index[Path(path).name] = path
        name_index[Path(path).stem] = path

    edges: list[tuple[str, str]] = []
    pair_results: list[dict] = []
    for i, a in enumerate(docs):
        a_deps_resolved = [name_index.get(x, x) for x in a.get("deps", [])]
        for dep in a_deps_resolved:
            edges.append((a["file"], dep))
        for j, b in enumerate(docs):
            if j <= i:
                continue
            overlap = sorted(set(a["files_touched"]) & set(b["files_touched"]))
            declared_dep = (
                b["file"] in a_deps_resolved
                or a["file"] in [name_index.get(x, x) for x in b.get("deps", [])]
            )
            verdict = "serial" if (overlap or declared_dep) else "parallel-ok"
            pair_results.append(
                {
                    "a": a["file"],
                    "b": b["file"],
                    "overlap": overlap,
                    "declared_dep": declared_dep,
                    "verdict": verdict,
                }
            )

    cycle = detect_cycle([d["file"] for d in docs], edges)

    print(
        json.dumps(
            {
                "docs": docs,
                "edges": pair_results,
                "dep_cycle": cycle,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
