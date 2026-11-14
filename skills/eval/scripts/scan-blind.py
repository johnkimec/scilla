#!/usr/bin/env python3
"""Scan candidate paths for words that reveal an eval.

Stdlib only. Read-only, so there is no --dry-run. Safe to run twice.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Tokens the candidate must not see. Hyphen and underscore separate tokens.
# "testing" and "latest" do not match "test".
TERMS = (
    "arena",
    "benchmark",
    "candidate",
    "compare",
    "eval",
    "experiment",
    "judge",
    "rubric",
    "score",
    "test",
)

# Dependency and VCS trees are not names the parent chose for the experiment.
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}

MAX_FINDINGS_DEFAULT = 40
MAX_BYTES = 2_000_000

EXIT_CLEAN = 0
EXIT_FOUND = 1
EXIT_USAGE = 2

PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:" + "|".join(TERMS) + r")(?![A-Za-z0-9])",
    re.IGNORECASE,
)


def build_parser() -> argparse.ArgumentParser:
    terms = ", ".join(TERMS)
    parser = argparse.ArgumentParser(
        prog="scan-blind.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Report eval words in directory names, file names, and file bodies "
            "a candidate can open. Reads only. Does not write, so there is no --dry-run."
        ),
        epilog=(
            "Words: " + terms + ".\n"
            "A hyphen or underscore separates a token. testing and latest do not match test.\n"
            "Skipped directories: " + ", ".join(sorted(SKIP_DIRS)) + ".\n"
            "\n"
            "exit 0  clean\n"
            "exit 1  one or more hits; JSON on stdout, each path on stderr\n"
            "exit 2  bad invocation, or every path is missing\n"
            "\n"
            "example:\n"
            "  python3 scripts/scan-blind.py ./notes-app ./prompt.txt\n"
        ),
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Candidate directories or prompt files to scan.",
    )
    parser.add_argument(
        "--max-findings",
        type=int,
        default=MAX_FINDINGS_DEFAULT,
        help=f"Stop after this many findings (default {MAX_FINDINGS_DEFAULT}).",
    )
    return parser


def matched_terms(text: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for match in PATTERN.finditer(text):
        term = match.group(0).lower()
        if term not in seen:
            seen.add(term)
            found.append(term)
    return found


def looks_binary(path: Path) -> bool:
    try:
        sample = path.read_bytes()[:8192]
    except OSError:
        return True
    return b"\x00" in sample


def add_finding(findings: list[dict], cap: int, item: dict) -> bool:
    """Append a finding. Return False when the cap is already full."""
    if len(findings) >= cap:
        return False
    findings.append(item)
    return True


def scan_file(path: Path, findings: list[dict], cap: int, stats: dict) -> bool:
    stats["files"] += 1
    for term in matched_terms(path.name):
        if not add_finding(
            findings,
            cap,
            {
                "path": str(path),
                "kind": "file_name",
                "term": term,
                "line": None,
                "message": (
                    f'File name contains "{term}". Rename it before the candidate can open it.'
                ),
            },
        ):
            return False
    if path.is_symlink():
        if not add_finding(
            findings,
            cap,
            {
                "path": str(path),
                "kind": "symlink",
                "term": None,
                "line": None,
                "message": "Symlink left unscanned. Point the scan at the real file.",
            },
        ):
            return False
        return True
    try:
        size = path.stat().st_size
    except OSError as exc:
        add_finding(
            findings,
            cap,
            {
                "path": str(path),
                "kind": "unreadable",
                "term": None,
                "line": None,
                "message": f"Could not stat the file ({exc}). Move it off the candidate path.",
            },
        )
        return len(findings) < cap
    if size > MAX_BYTES:
        add_finding(
            findings,
            cap,
            {
                "path": str(path),
                "kind": "too_large",
                "term": None,
                "line": None,
                "message": (
                    f"File is {size} bytes. The scan reads at most {MAX_BYTES}. "
                    "Move it off the candidate path or split it."
                ),
            },
        )
        return len(findings) < cap
    if looks_binary(path):
        stats["skipped_binary"] += 1
        return True
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        add_finding(
            findings,
            cap,
            {
                "path": str(path),
                "kind": "unreadable",
                "term": None,
                "line": None,
                "message": f"Could not read the file ({exc}). Move it off the candidate path.",
            },
        )
        return len(findings) < cap
    for line_no, line in enumerate(text.splitlines(), start=1):
        for term in matched_terms(line):
            if not add_finding(
                findings,
                cap,
                {
                    "path": str(path),
                    "kind": "body",
                    "term": term,
                    "line": line_no,
                    "message": (
                        f'Line {line_no} contains "{term}". '
                        "Remove it from anything the candidate can read."
                    ),
                },
            ):
                return False
    return True


def scan_tree(root: Path, findings: list[dict], cap: int, stats: dict) -> bool:
    """Return False when the finding cap was hit."""
    if root.is_symlink() and not root.is_dir():
        return scan_file(root, findings, cap, stats)
    if root.is_file():
        return scan_file(root, findings, cap, stats)
    if not root.is_dir():
        raise FileNotFoundError(str(root))

    for term in matched_terms(root.name):
        if not add_finding(
            findings,
            cap,
            {
                "path": str(root),
                "kind": "directory_name",
                "term": term,
                "line": None,
                "message": (
                    f'Directory name contains "{term}". Rename it to a name a user would pick.'
                ),
            },
        ):
            return False

    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        current = Path(dirpath)
        stats["directories"] += 1
        kept: list[str] = []
        for name in list(dirnames):
            if name in SKIP_DIRS:
                continue
            child = current / name
            if child.is_symlink():
                if not add_finding(
                    findings,
                    cap,
                    {
                        "path": str(child),
                        "kind": "symlink",
                        "term": None,
                        "line": None,
                        "message": "Symlink left unscanned. Point the scan at the real directory.",
                    },
                ):
                    return False
                continue
            kept.append(name)
            for term in matched_terms(name):
                if not add_finding(
                    findings,
                    cap,
                    {
                        "path": str(child),
                        "kind": "directory_name",
                        "term": term,
                        "line": None,
                        "message": (
                            f'Directory name contains "{term}". '
                            "Rename it to a name a user would pick."
                        ),
                    },
                ):
                    return False
        dirnames[:] = kept
        for name in filenames:
            if not scan_file(current / name, findings, cap, stats):
                return False
    return True


def emit(payload: dict) -> None:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    for item in payload["findings"]:
        where = item["path"]
        if item.get("line"):
            where = f"{where}:{item['line']}"
        print(f"{where}: {item['message']}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.max_findings < 1:
        print("Error: --max-findings must be at least 1.", file=sys.stderr)
        return EXIT_USAGE
    if not args.paths:
        print("Error: pass at least one candidate directory or prompt file.", file=sys.stderr)
        print("Usage: python3 scripts/scan-blind.py <path> [<path> ...]", file=sys.stderr)
        return EXIT_USAGE

    findings: list[dict] = []
    stats = {"files": 0, "directories": 0, "skipped_binary": 0}
    missing: list[str] = []
    hit_cap = False
    for raw in args.paths:
        path = Path(raw)
        if not path.exists():
            missing.append(raw)
            continue
        if not scan_tree(path, findings, args.max_findings, stats):
            hit_cap = True
            break

    if missing and not findings:
        print(
            "Error: path not found: "
            + ", ".join(missing)
            + ". Pass a directory or file that exists.",
            file=sys.stderr,
        )
        return EXIT_USAGE

    payload = {
        "ok": not findings and not missing,
        "terms": list(TERMS),
        "files": stats["files"],
        "directories": stats["directories"],
        "skipped_binary": stats["skipped_binary"],
        "skipped_dirs": sorted(SKIP_DIRS),
        "truncated": hit_cap,
        "missing": missing,
        "findings": findings,
    }
    emit(payload)
    if missing:
        print(
            "Error: path not found: "
            + ", ".join(missing)
            + ". Pass a directory or file that exists.",
            file=sys.stderr,
        )
        return EXIT_FOUND if findings else EXIT_USAGE
    if findings:
        extra = " Stopped early; fix these and run the scan again." if hit_cap else ""
        print(
            f"{len(findings)} finding(s). A candidate that can open these paths can see the experiment.{extra}",
            file=sys.stderr,
        )
        return EXIT_FOUND
    print("Clean. No eval words in the scanned names or file bodies.", file=sys.stderr)
    return EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
