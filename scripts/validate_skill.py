#!/usr/bin/env python3
"""Validate a Codex/Tessl skill folder with only Python's standard library."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024


def error(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter delimited by ---")

    frontmatter: dict[str, str] = {}
    for line_number, line in enumerate(match.group(1).splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "-")):
            continue
        if "\t" in line:
            raise ValueError(f"frontmatter line {line_number} contains a tab")

        key_match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not key_match:
            raise ValueError(f"frontmatter line {line_number} is not a simple key/value pair")

        key, value = key_match.groups()
        frontmatter[key] = (value or "").strip().strip('"').strip("'")

    return frontmatter


def validate_skill(skill_path: Path) -> list[str]:
    failures: list[str] = []
    skill_md = skill_path / "SKILL.md"

    if not skill_md.is_file():
        return [f"{skill_md}: missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8")
    try:
        frontmatter = parse_frontmatter(text)
    except ValueError as exc:
        return [f"{skill_md}: {exc}"]

    unexpected_keys = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if unexpected_keys:
        allowed = ", ".join(sorted(ALLOWED_FRONTMATTER_KEYS))
        failures.append(
            f"{skill_md}: unexpected frontmatter key(s): {', '.join(sorted(unexpected_keys))}; "
            f"allowed keys: {allowed}"
        )

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()

    if not name:
        failures.append(f"{skill_md}: missing required frontmatter key: name")
    elif not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        failures.append(f"{skill_md}: name must be hyphen-case lowercase text")
    elif len(name) > MAX_SKILL_NAME_LENGTH:
        failures.append(
            f"{skill_md}: name is {len(name)} characters; max is {MAX_SKILL_NAME_LENGTH}"
        )

    if not description:
        failures.append(f"{skill_md}: missing required frontmatter key: description")
    elif "<" in description or ">" in description:
        failures.append(f"{skill_md}: description must not contain angle brackets")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        failures.append(
            f"{skill_md}: description is {len(description)} characters; "
            f"max is {MAX_DESCRIPTION_LENGTH}"
        )

    body = re.sub(r"^---\n.*?\n---\n?", "", text, count=1, flags=re.DOTALL).strip()
    if not body:
        failures.append(f"{skill_md}: missing body content after frontmatter")

    for link in re.findall(r"\]\((references/[^)]+)\)", text):
        target = skill_path / link
        if not target.is_file():
            failures.append(f"{skill_md}: missing referenced file {link}")

    return failures


def main() -> int:
    if len(sys.argv) != 2:
        return error("usage: validate_skill.py <skill-directory>")

    failures = validate_skill(Path(sys.argv[1]))
    if failures:
        for failure in failures:
            print(f"error: {failure}", file=sys.stderr)
        return 1

    print("Skill is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
