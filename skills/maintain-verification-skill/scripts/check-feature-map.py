#!/usr/bin/env python3
"""Check a verification skill's frontmatter and feature-map headings.

Keep this file identical in create-verification-skill and
maintain-verification-skill. A one-skill install has its own copy.

Stdlib only. Read-only, so there is no --dry-run. Safe to run twice.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HEADINGS = (
    "Sub-features",
    "How to get to it (user POV)",
    "Driving it with <harness>",
    "Gotchas",
)

DRIVING_PREFIX = "Driving it with "
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
H2_RE = re.compile(r"^## ([^#\n].*)$")
DESC_LIMIT = 1024
MAX_FINDINGS = 40

EXIT_CLEAN = 0
EXIT_FOUND = 1
EXIT_USAGE = 2


class Findings(list):
    """A list of findings that records when the cap dropped more."""

    def __init__(self) -> None:
        super().__init__()
        self.truncated = False


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check-feature-map.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Check verification-skill frontmatter and the four feature-file headings, in order. "
            "Reads only. Does not launch or drive the system, and does not write, so there is no --dry-run."
        ),
        epilog=(
            "Headings, in order:\n"
            "  Sub-features\n"
            "  How to get to it (user POV)\n"
            "  Driving it with <harness name>\n"
            "  Gotchas\n"
            "The third heading must name the harness. A leftover <harness> placeholder fails.\n"
            "features/README.md is the index and is not a feature file.\n"
            "\n"
            "exit 0  shape ok\n"
            "exit 1  a frontmatter or heading miss; JSON on stdout, each miss on stderr\n"
            "exit 2  bad invocation, or the path does not exist\n"
            "\n"
            "example:\n"
            "  python3 scripts/check-feature-map.py --skill .cursor/skills/verify-notes\n"
        ),
    )
    parser.add_argument(
        "--skill",
        help="Directory that contains SKILL.md and features/. Checks frontmatter and headings.",
    )
    parser.add_argument(
        "--features",
        help=(
            "A features/ directory. Checks headings only. README.md is the index and is skipped. "
            "When set with --skill, this directory is checked instead of <skill>/features."
        ),
    )
    return parser


def add(findings: Findings, path: Path | None, check: str, message: str) -> None:
    if len(findings) >= MAX_FINDINGS:
        findings.truncated = True
        return
    findings.append(
        {
            "path": str(path) if path is not None else None,
            "check": check,
            "message": message,
        }
    )


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        body = value[1:-1]
        if value[0] == '"':
            body = body.replace(r"\"", '"').replace(r"\n", "\n")
        return body
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str | None]:
    """Return (fields, error). fields has name and description when error is None."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "SKILL.md has no YAML frontmatter. Without name and description the skill never registers."
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return None, "SKILL.md frontmatter has no closing ---. Without it the skill never registers."

    fields: dict[str, str] = {}
    index = 1
    while index < end:
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if line[0].isspace():
            return None, f"Frontmatter line {index + 1} is indented and belongs to no key. Expected name or description."
        if ":" not in line:
            return None, f"Frontmatter line {index + 1} has no key. Expected name or description."
        key, _, raw = line.partition(":")
        key = key.strip()
        raw = raw.strip()
        if raw in {">", ">-", "|", "|-", ">+", "|+"}:
            block: list[str] = []
            index += 1
            while index < end and (lines[index].startswith(" ") or lines[index].startswith("\t") or not lines[index].strip()):
                block.append(lines[index].strip())
                index += 1
            joiner = "\n" if raw.startswith("|") else " "
            fields[key] = joiner.join(part for part in block if part).strip()
            continue
        fields[key] = unquote(raw)
        index += 1
    return fields, None


def check_skill_file(skill_dir: Path, findings: list[dict]) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        add(findings, skill_dir, "frontmatter", "SKILL.md is missing. The skill never registers without it.")
        return
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError as exc:
        add(findings, skill_md, "frontmatter", f"Could not read SKILL.md ({exc}).")
        return
    fields, error = parse_frontmatter(text)
    if error:
        add(findings, skill_md, "frontmatter", error)
        return
    assert fields is not None
    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip()
    if not name:
        add(findings, skill_md, "frontmatter", "name is missing or empty. The skill never registers without it.")
    elif not NAME_RE.fullmatch(name):
        add(
            findings,
            skill_md,
            "frontmatter",
            f'name is "{name}". Use lowercase letters, numbers, and single hyphens. No leading, trailing, or doubled hyphen.',
        )
    elif name != skill_dir.name:
        add(
            findings,
            skill_md,
            "frontmatter",
            f'name is "{name}" and the folder is "{skill_dir.name}". They must match or the skill does not register.',
        )
    if not description:
        add(
            findings,
            skill_md,
            "frontmatter",
            "description is missing or empty. The skill never registers without it.",
        )
    elif len(description) > DESC_LIMIT:
        add(
            findings,
            skill_md,
            "frontmatter",
            f"description is {len(description)} characters. The limit is {DESC_LIMIT}.",
        )


def heading_texts(path: Path) -> tuple[list[str] | None, str | None]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return None, f"Could not read the feature file ({exc})."
    found: list[str] = []
    in_fence = False
    for line in lines:
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = H2_RE.match(line)
        if match:
            found.append(match.group(1).strip())
    return found, None


def driving_ok(text: str) -> bool:
    if not text.startswith(DRIVING_PREFIX):
        return False
    harness = text[len(DRIVING_PREFIX) :].strip()
    if not harness or "<" in harness or ">" in harness:
        return False
    return True


def check_feature_file(path: Path, findings: list[dict]) -> None:
    found, error = heading_texts(path)
    if error:
        add(findings, path, "headings", error)
        return
    assert found is not None
    expected_display = list(HEADINGS)
    problems: list[str] = []
    if len(found) != 4:
        problems.append(
            f"found {len(found)} H2 heading(s) ({', '.join(found) or 'none'}). Expected 4, in order: "
            + "; ".join(expected_display)
            + "."
        )
    else:
        labels = [
            ("exact", "Sub-features", found[0] == "Sub-features"),
            ("exact", "How to get to it (user POV)", found[1] == "How to get to it (user POV)"),
            ("harness", "Driving it with <harness>", driving_ok(found[2])),
            ("exact", "Gotchas", found[3] == "Gotchas"),
        ]
        for index, (_, label, ok) in enumerate(labels, start=1):
            if ok:
                continue
            if index == 3 and found[2].startswith(DRIVING_PREFIX):
                problems.append(
                    f'H2 3 is "{found[2]}". Replace the placeholder with the harness name, '
                    'as in "Driving it with control-notes".'
                )
            else:
                problems.append(f'H2 {index} is "{found[index - 1]}". Expected "{label}".')
    if problems:
        add(findings, path, "headings", " ".join(problems))


def check_features_dir(features_dir: Path, findings: list[dict]) -> int:
    if not features_dir.is_dir():
        add(findings, features_dir, "headings", "features/ is missing. The map has no feature files to check.")
        return 0
    readme = features_dir / "README.md"
    if not readme.is_file():
        add(findings, features_dir, "headings", "features/README.md is missing. The index is part of the map.")
    checked = 0
    for path in sorted(features_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        checked += 1
        check_feature_file(path, findings)
    if checked == 0:
        add(
            findings,
            features_dir,
            "headings",
            "features/ has no feature files. README.md is the index, not a feature.",
        )
    return checked


def emit(payload: dict) -> None:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    for item in payload["findings"]:
        where = item["path"] or item["check"]
        print(f"{where}: {item['message']}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.skill and not args.features:
        print("Error: pass --skill, --features, or both.", file=sys.stderr)
        print(
            "Usage: python3 scripts/check-feature-map.py --skill <verify-target-dir>",
            file=sys.stderr,
        )
        return EXIT_USAGE

    findings = Findings()
    checked = 0
    skill_dir = None
    features_dir = None

    if args.skill:
        skill_dir = Path(args.skill)
        if not skill_dir.is_dir():
            print(
                f"Error: --skill path not found: {args.skill}. Pass the directory that contains SKILL.md.",
                file=sys.stderr,
            )
            return EXIT_USAGE
        check_skill_file(skill_dir, findings)
        features_dir = skill_dir / "features"

    if args.features:
        features_dir = Path(args.features)
        if not features_dir.is_dir():
            print(
                f"Error: --features path not found: {args.features}. Pass a features directory.",
                file=sys.stderr,
            )
            return EXIT_USAGE

    if features_dir is not None:
        checked = check_features_dir(features_dir, findings)

    payload = {
        "ok": not findings,
        "skill": str(skill_dir) if skill_dir else None,
        "features": str(features_dir) if features_dir else None,
        "features_checked": checked,
        "truncated": findings.truncated,
        "findings": findings,
    }
    emit(payload)
    if findings:
        extra = " Stopped early; fix these and run the check again." if payload["truncated"] else ""
        print(
            f"{len(findings)} finding(s).{extra} Fix the files and run the check again.",
            file=sys.stderr,
        )
        return EXIT_FOUND
    print(
        f"Shape ok. Frontmatter checked={bool(skill_dir)} features_checked={checked}.",
        file=sys.stderr,
    )
    return EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
